"""Verificação documental exploratória; não equivale a auditoria jurídica.
Executar com PM4Py 2.7.23.12. Fontes preservadas em fontes/.
"""
from pathlib import Path
import csv,json,copy,datetime as dt,collections,statistics as st,hashlib,random,sys,platform,zipfile
import xml.etree.ElementTree as ET
import pm4py
from pm4py.objects.log.obj import EventLog,Trace,Event
from pm4py.algo.conformance.alignments.petri_net import algorithm as align
from pm4py.objects.petri_net import semantics

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PACKAGED=(HERE/'fontes/casos_analisados.csv').exists() and (HERE/'fontes/modelos_v04').exists()
OUT=HERE if PACKAGED else ROOT/'outputs/verificacoes_pm4py_20261125'
for folder in ['modelos','resultados','fontes']: (OUT/folder).mkdir(parents=True,exist_ok=True)
B='http://www.omg.org/spec/BPMN/20100524/MODEL'
tag=lambda s:'{'+B+'}'+s
ET.register_namespace('bpmn',B)
sources=HERE/'fontes/modelos_v04' if PACKAGED else ROOT/'analise_bpmn/modelo_funcional_v04'
rawpath=HERE/'fontes/dataset_original.csv' if PACKAGED else ROOT/'analise_bpmn/fontes/dataset_original.csv'
casepath=HERE/'fontes/casos_analisados.csv' if PACKAGED else ROOT/'tmp/dados_conferencia_20261124/casos_analisados.csv'
raw=list(csv.DictReader(rawpath.open(encoding='utf-8-sig')))
cases=list(csv.DictReader(casepath.open(encoding='utf-8-sig')))
assert len(cases)==len({x['processo'] for x in cases})==63
eligible=[x for x in cases if x['rito']=='Pregão' and x['instrumento'] in ('Ata RP','Termo contratual','Nota de empenho substitutiva')]
assert len(eligible)==32
DOCMAP={'Documento de Oficialização da Demanda - DOD':'DOD','Estudos Técnicos Preliminares - ETP':'ETP','Termo de Referência - TR':'TR','Pesquisa de Preços':'PRECOS','Edital':'EDITAL','Nota de Empenho':'EMPENHO','Contrato':'CONTRATO','Ata de Registro de Preços':'ATA_RP'}
TASKMAP={'A01':'DOD','A02a':'ETP','A02b':'TR','A17':'PRECOS','A21a':'EDITAL','A19':'EMPENHO','A23':'CONTRATO','A25':'ATA_RP'}

def writecsv(name,rows):
    if not rows:return
    with (OUT/'resultados'/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def source_model(profile):
    name='NE_Substitutiva' if profile in ('NE','ARP') else 'Com_Termo_Contratual'
    return ET.parse(sources/f'BPMN_PM4Py_v04_{name}.bpmn').getroot()

def save_model(root,name):
    p=OUT/'modelos'/f'{name}.bpmn'
    ET.indent(root,space='  ');ET.ElementTree(root).write(p,encoding='utf-8',xml_declaration=True)
    return p

def make_reference(profile):
    root=source_model(profile);proc=root.find(tag('process'))
    nodes={x.get('id'):copy.deepcopy(x) for x in proc if x.tag in {tag(k) for k in ['task','startEvent','endEvent','parallelGateway','exclusiveGateway']}}
    edges=[(x.get('sourceRef'),x.get('targetRef')) for x in proc.findall(tag('sequenceFlow'))]
    if profile=='ARP':
        keep={'A15b'}
        while True:
            expanded=keep|{a for a,b in edges if b in keep}
            if expanded==keep:break
            keep=expanded
        nodes={k:v for k,v in nodes.items() if k in keep}
        edges=[(a,b) for a,b in edges if a in keep and b in keep]
        nodes['A25']=ET.Element(tag('task'),{'id':'A25','name':'Emitir ata de registro de preços'})
        nodes['end']=ET.Element(tag('endEvent'),{'id':'end','name':'Registro de preços concluído'})
        edges += [('A15b','A25'),('A25','end')]
    else:
        remove={'A10','A11'}
        nodes={k:v for k,v in nodes.items() if k not in remove}
        edges=[(a,b) for a,b in edges if a not in remove and b not in remove]
        edges.append(('A19' if profile=='NE' else 'G04','end'))
        if profile=='CONTRATO':
            # No perfil contratual, contrato encerra; NE paralela é opcional.
            edges.remove(('G03','A19'))
            edges.remove(('A19','G04'))
            nodes['G_NE_OPCIONAL']=ET.Element(tag('exclusiveGateway'),{'id':'G_NE_OPCIONAL','name':'Empenho registrado no mesmo fluxo?'})
            nodes['G_NE_MERGE']=ET.Element(tag('exclusiveGateway'),{'id':'G_NE_MERGE','name':'Junção do ramo de empenho'})
            edges += [('G03','G_NE_OPCIONAL'),('G_NE_OPCIONAL','A19'),('G_NE_OPCIONAL','G_NE_MERGE'),('A19','G_NE_MERGE'),('G_NE_MERGE','G04')]
        nodes['end'].set('name','Contratação encerrada no instrumento')
    newroot=ET.Element(tag('definitions'),{'id':'defs_v05_'+profile,'targetNamespace':'https://tre-to.tese/modelos/v05'})
    newproc=ET.SubElement(newroot,tag('process'),{'id':'Process_v05_'+profile,'name':'Referência documental '+profile,'isExecutable':'false'})
    for node in nodes.values():
        for child in list(node):
            if child.tag in (tag('incoming'),tag('outgoing')):node.remove(child)
        newproc.append(node)
    for i,(a,b) in enumerate(edges):
        key='Flow_'+str(i);ET.SubElement(newproc,tag('sequenceFlow'),{'id':key,'sourceRef':a,'targetRef':b})
        ET.SubElement(nodes[a],tag('outgoing')).text=key;ET.SubElement(nodes[b],tag('incoming')).text=key
    return newroot

def structural(net,im,fm):
    sound,diag=pm4py.check_soundness(net,im,fm,print_diagnostics=False)
    places=sorted(net.places,key=lambda p:p.name)
    key=lambda m:tuple(int(m.get(p,0)) for p in places)
    marks={key(im):im};queue=collections.deque([key(im)]);adj=collections.defaultdict(set);fired=set();terminal=[]
    while queue:
        s=queue.popleft();enabled=semantics.enabled_transitions(net,marks[s])
        if not enabled:terminal.append(s)
        for t in enabled:
            fired.add(t.name);m=semantics.execute(t,net,marks[s]);k=key(m);adj[s].add(k)
            if k not in marks:marks[k]=m;queue.append(k)
        if len(marks)>10000:raise RuntimeError('Limite de estados excedido')
    final=key(fm);back={final}
    while True:
        more=back|{k for k,v in adj.items() if v&back}
        if more==back:break
        back=more
    result={'soundness_pm4py':bool(sound),'estados_alcancaveis':len(marks),'final_alcancavel':final in marks,'todos_estados_alcancam_final':set(marks)<=back,'terminais_apenas_final':set(terminal)=={final},'sem_transicoes_mortas':len(fired)==len(net.transitions),'transicoes_visiveis':sum(t.label is not None for t in net.transitions)}
    assert all(result[k] for k in ['soundness_pm4py','final_alcancavel','todos_estados_alcancam_final','terminais_apenas_final','sem_transicoes_mortas'])
    return result

models={};checks=[];mapping=[]
for name in ['BASE_V04','CONTRATO','NE','ARP']:
    root=source_model('CONTRATO') if name=='BASE_V04' else make_reference(name)
    path=save_model(root,name)
    model=pm4py.read_bpmn(str(path));net,im,fm=pm4py.convert_to_petri_net(model)
    checks.append({'modelo':name,'camada':'funcional',**structural(net,im,fm)})
    labels={x.get('name'):TASKMAP[x.get('id')] for x in root.findall('.//'+tag('task')) if x.get('id') in TASKMAP}
    for t in net.transitions:
        if t.label is not None:
            before=t.label;t.label=labels.get(before)
            mapping.append({'modelo':name,'atividade_bpmn':before,'rotulo_observavel':t.label or '[silenciosa: sem correspondência unívoca]'})
    checks.append({'modelo':name,'camada':'projecao_documental',**structural(net,im,fm)})
    pm4py.write_pnml(net,im,fm,str(OUT/'modelos'/f'{name}_projecao.pnml'))
    models[name]=(net,im,fm)
    print('ESTRUTURA',name,checks[-1],flush=True)
writecsv('verificacao_estrutural.csv',checks);writecsv('mapeamento_atividades.csv',mapping)
writecsv('mapeamento_documental.csv',[{'tipo_documental':a,'atividade_observavel':b} for a,b in DOCMAP.items()])

# Controles semânticos sintéticos: testar o término sem entrega posterior.
controls=[]
for name,sequence,expected in [
    ('CONTRATO',['DOD','ETP','TR','PRECOS','EDITAL','CONTRATO'],True),
    ('CONTRATO',['DOD','ETP','TR','PRECOS','EDITAL','EMPENHO','CONTRATO'],True),
    ('CONTRATO',['DOD','ETP','TR','PRECOS','EDITAL','CONTRATO','EMPENHO'],True),
    ('NE',['DOD','ETP','TR','PRECOS','EDITAL','EMPENHO'],True),
    ('ARP',['DOD','ETP','TR','PRECOS','EDITAL','ATA_RP'],True),
    ('ARP',['DOD','TR','ETP','PRECOS','EDITAL','ATA_RP'],False),
    ('NE',['DOD','ETP','TR','PRECOS','EDITAL'],False),
    ('ARP',['DOD','ETP','TR','PRECOS','EDITAL'],False)]:
    tr=Trace([Event({'concept:name':x}) for x in sequence])
    ans=align.apply_trace(tr,*models[name],parameters={'show_progress_bar':False},variant=align.Variants.VERSION_DIJKSTRA_NO_HEURISTICS)
    fits=not any(a=='>>' and b is not None or b=='>>' for a,b in ans['alignment'])
    assert fits==expected,(name,sequence,ans)
    controls.append({'modelo':name,'sequencia':' > '.join(sequence),'aderencia_integral_esperada':expected,'aderencia_integral_obtida':fits,'fitness':ans['fitness']})
writecsv('controles_semanticos.csv',controls)

by=collections.defaultdict(list);seen={};conflicts=0
for r in raw:
    k=(r['PROTOCOLO_PROC_EM_TRAMITACAO'],r['ID_DOCUMENTO'])
    if k in seen:
        assert (r['SERIE_NOME'],r['DTH_DOCUMENTO'])==(seen[k]['SERIE_NOME'],seen[k]['DTH_DOCUMENTO'])
        continue
    seen[k]=r
    d={**r,'timestamp':dt.datetime.strptime(r['DTH_DOCUMENTO'],'%d-%m-%Y %H:%M')}
    by[k[0]].append(d)
assert len(seen)==3334
traceinfo={};coverage=[];projected_events=[]
for c in cases:
    proc=c['processo'];end=dt.datetime.fromisoformat(c['marco_informado']) if c['marco_informado'] else None
    scope=[d for d in by[proc] if end is None or d['timestamp']<=end]
    projected=[{**d,'activity':DOCMAP[d['SERIE_NOME']]} for d in scope if d['SERIE_NOME'] in DOCMAP]
    expected={'Ata RP':'ATA_RP','Termo contratual':'CONTRATO','Nota de empenho substitutiva':'EMPENHO'}.get(c['instrumento'])
    hasend=any(d['activity']==expected for d in projected)
    accepted=c in eligible
    complete=accepted and c['janela']=='Até 03/06/2026' and hasend
    traceinfo[proc]={'events':projected,'complete':complete}
    coverage.append({'processo':proc,'rito':c['rito'],'instrumento':c['instrumento'],'marco':c['marco_informado'],'janela':c['janela'],'documentos_unicos_log':len(by[proc]),'documentos_ate_marco':len(scope),'eventos_projetados':len(projected),'documentos_fora_vocabulario':len(scope)-len(projected),'marco_documental_presente':hasend,'comparacao_pregao':accepted,'subconjunto_com_marco_no_corte':complete,'tratamento':'Comparação pareada' if accepted else 'Rito/perfil fora das referências executadas'})
    for d in projected:
        if accepted:projected_events.append({'processo':proc,'id_documento':d['ID_DOCUMENTO'],'tipo_documental':d['SERIE_NOME'],'atividade':d['activity'],'timestamp':d['timestamp'].isoformat()})
writecsv('cobertura_63_processos.csv',coverage);writecsv('eventos_projetados_32_pregoes.csv',projected_events)

results=[];moves=[]
params={align.Parameters.PARAM_MAX_ALIGN_TIME_TRACE:15,'show_progress_bar':False}
for order in ['id_crescente','id_decrescente','alternativa_reprodutivel']:
    for c in eligible:
        proc=c['processo'];events=traceinfo[proc]['events']
        if order=='id_crescente':events=sorted(events,key=lambda d:(d['timestamp'],int(d['ID_DOCUMENTO'])))
        elif order=='id_decrescente':events=sorted(events,key=lambda d:(d['timestamp'],-int(d['ID_DOCUMENTO'])))
        else:events=sorted(events,key=lambda d:(d['timestamp'],int(d['ORDEM_EMPATE_ALTERNATIVA']) if d.get('ORDEM_EMPATE_ALTERNATIVA') else hashlib.sha256(('ebrahim-v05|'+d['ID_DOCUMENTO']).encode()).hexdigest()))
        trace=Trace([Event({'concept:name':d['activity'],'time:timestamp':d['timestamp'],'doc:id':d['ID_DOCUMENTO']}) for d in events],attributes={'concept:name':proc})
        assigned={'Ata RP':'ARP','Termo contratual':'CONTRATO','Nota de empenho substitutiva':'NE'}[c['instrumento']]
        for mode,modelname in [('agregado','BASE_V04'),('estratificado',assigned)]:
            answer=align.apply_trace(trace,*models[modelname],parameters=params,variant=align.Variants.VERSION_DIJKSTRA_NO_HEURISTICS)
            row={'processo':proc,'instrumento':c['instrumento'],'ordem':order,'modo':mode,'modelo':modelname,'eventos':len(trace),'marco_no_corte':traceinfo[proc]['complete'],'calculado':answer is not None,'fitness':None,'custo':None,'sincronos':None,'somente_log':None,'somente_modelo_visivel':None}
            if answer is not None:
                sync=lm=mm=0
                for left,right in answer['alignment']:
                    if left==right and left not in ('>>',None):sync+=1;kind='sincrono'
                    elif right=='>>':lm+=1;kind='somente_log'
                    elif left=='>>' and right is not None:mm+=1;kind='somente_modelo'
                    else:continue
                    moves.append({'processo':proc,'ordem':order,'modo':mode,'tipo':kind,'log':left,'modelo':right})
                row.update(fitness=float(answer['fitness']),custo=int(answer['cost']),sincronos=sync,somente_log=lm,somente_modelo_visivel=mm)
            results.append(row)
    print('ALINHAMENTOS',order,len(results),flush=True)
    writecsv('alinhamentos_por_processo.csv',results)
writecsv('movimentos_alinhamento.csv',moves)
summary=[]
for subset in ['32_pregoes_observados','com_marco_observado_ate_corte']:
    for order in ['id_crescente','id_decrescente','alternativa_reprodutivel']:
        for mode in ['agregado','estratificado']:
            a=[r for r in results if r['ordem']==order and r['modo']==mode and (subset=='32_pregoes_observados' or r['marco_no_corte'])]
            good=[r for r in a if r['calculado']]
            summary.append({'subconjunto':subset,'ordem':order,'modo':mode,'n':len(a),'calculados':len(good),'fitness_medio':st.mean(r['fitness'] for r in good) if good else None,'fitness_mediano':st.median(r['fitness'] for r in good) if good else None,'aderencia_integral':sum(r['somente_log']==r['somente_modelo_visivel']==0 for r in good),'movimentos_log':sum(r['somente_log'] for r in good),'movimentos_modelo':sum(r['somente_modelo_visivel'] for r in good)})
writecsv('resumo_comparacao.csv',summary)
paired=[]
for c in eligible:
    proc=c['processo'];a=[r for r in results if r['processo']==proc]
    deltas=[]
    for order in ['id_crescente','id_decrescente','alternativa_reprodutivel']:
        v={r['modo']:r for r in a if r['ordem']==order}
        if all(r['calculado'] for r in v.values()):deltas.append(v['estratificado']['fitness']-v['agregado']['fitness'])
    strat=[r['fitness'] for r in a if r['modo']=='estratificado' and r['calculado']]
    paired.append({'processo':proc,'instrumento':c['instrumento'],'marco_no_corte':traceinfo[proc]['complete'],'delta_minimo':min(deltas) if deltas else None,'delta_maximo':max(deltas) if deltas else None,'sensibilidade_fitness_estratificado':max(strat)-min(strat) if strat else None})
writecsv('sensibilidade_pareada.csv',paired)

meta={'data':'2026-11-25','python':platform.python_version(),'pm4py':pm4py.__version__,'base_sha256':hashlib.sha256(rawpath.read_bytes()).hexdigest(),'conferencia_sha256':hashlib.sha256(casepath.read_bytes()).hexdigest(),'n_processos':63,'n_pregoes_comparados':32,'n_subconjunto_marco_no_corte':sum(x['complete'] for x in traceinfo.values()),'alinhamentos_calculados':sum(r['calculado'] for r in results),'alinhamentos_previstos':len(results),'eventos_projetados':len(projected_events),'eventos_unicos_log':len(seen),'custos':'PM4Py padrão: movimento log/modelo visível 10000; invisível 1; síncrono 0','algoritmo':'Dijkstra sem heurística; 15 segundos por traço','critério_institucional':'Contrato ou NE encerra conforme perfil; ATA RP encerra registro de preços; sem exigir entrega posterior','limitacao':'Projeção documental, não verificação de aprovações, legalidade ou tramitações; referências v05 derivadas e ainda sem validação externa por especialistas.'}
meta['base_sha256_normalizada_lf']=hashlib.sha256((rawpath.read_text().rstrip('\n')+'\n').encode()).hexdigest()
(OUT/'resultados/metadados.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
for src in [rawpath,casepath]: (OUT/'fontes'/src.name).write_bytes(src.read_bytes())
(OUT/'fontes/modelos_v04').mkdir(exist_ok=True)
for src in sources.glob('BPMN_PM4Py_v04_*.bpmn'):(OUT/'fontes/modelos_v04'/src.name).write_bytes(src.read_bytes())
(OUT/'verificar_pm4py_20261125.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps({'metadados':meta,'resumos':summary,'sensibilidade_casos':sum((x['sensibilidade_fitness_estratificado'] or 0)>1e-9 for x in paired)},ensure_ascii=False,indent=2),flush=True)
