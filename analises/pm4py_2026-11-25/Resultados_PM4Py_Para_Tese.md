# Análise da aderência documental aos perfis de contratação

A comparação entre uma referência uniforme e referências ajustadas ao instrumento e ao objetivo administrativo apresentou maior fitness médio nos pregões examinados. O resultado foi acompanhado de redução dos movimentos exclusivos do modelo, embora quatro processos tenham apresentado diminuição do fitness e nenhum tenha alcançado aderência integral. Esta seção descreve os procedimentos e os resultados, delimitando sua interpretação às atividades representadas documentalmente no log.

## Procedimentos de verificação

As verificações foram executadas no PM4Py 2.7.23.12, com Python 3.12.14. A base continha 3.641 registros relativos a 63 processos do TRE-TO. A deduplicação pela chave composta por processo e documento resultou em 3.334 documentos distintos. Os tipos e as datas de geração foram preservados, sem criação de eventos a partir dos marcos de encerramento informados na conferência documental.

Foram selecionados 32 processos de pregão com perfil identificado: 14 associados à ata de registro de preços, 12 classificados com termo contratual e seis com nota de empenho substitutiva. Os dois pregões sem instrumento localizado não receberam perfil presumido. As 24 contratações diretas e os cinco casos classificados em outro rito ou com rito não localizado foram mantidos fora dessa comparação, evitando a aplicação da referência de pregão a procedimentos de natureza distinta.

O critério institucional de encerramento considerou suficiente o contrato ou a nota de empenho, conforme o instrumento informado para cada caso. Nos processos destinados ao registro de preços, adotou-se a emissão da ata como atendimento do objetivo. Assim, a comparação não exigiu entrega posterior para execução, pagamentos ou execução contratual.

Foram preparadas três referências por perfil. A referência contratual admitiu contrato sem empenho no mesmo fluxo e preservou o paralelismo quando ambos foram representados. A referência de NE substitutiva terminou na emissão da nota, sem exigir termo contratual. A referência de registro de preços terminou na emissão da ata após o trecho licitatório. Como contraste uniforme, utilizou-se o modelo funcional v04 com contrato e empenho obrigatórios. Essa referência foi distinta do modelo legado empregado na auditoria documental anterior.

A observabilidade foi delimitada por um vocabulário comum às referências e aos traços: DOD, ETP, TR, pesquisa de preços, edital, nota de empenho, contrato e ata de registro de preços. As atividades sem correspondência documental unívoca foram representadas por transições silenciosas. Documentos genericamente classificados como Decisão, Parecer, Informação ou Publicação não foram associados automaticamente a aprovações, homologações ou tramitações. Desse modo, os alinhamentos avaliaram a projeção documental das referências, sem verificar a execução das atividades tornadas silenciosas.

Nos 32 pregões, o recorte temporal reuniu 1.876 documentos, dos quais 427 pertenceram ao vocabulário observável. Cada documento foi mantido como um evento. Os traços foram limitados ao marco informado quando disponível; nos demais casos, preservou-se a sequência existente na extração. Os desfechos posteriores à referência de 03/06/2026 foram mantidos como acompanhamento, sem inserção retroativa de eventos no log. Também foi descrito separadamente um subconjunto de 21 processos com marco datado até o corte e tipo documental terminal presente na extração.

Os alinhamentos utilizaram Dijkstra sem heurística e os custos padrão do PM4Py: zero para movimento síncrono, 10.000 para movimento exclusivo do log ou do modelo visível e um para transição silenciosa. Estabeleceu-se limite de 15 segundos por traço. Foram examinadas três ordenações para os documentos com o mesmo horário: identificador crescente, identificador decrescente e uma alternativa determinística reprodutível. Essas ordenações constituíram ensaios de sensibilidade, sem pressupor a cronologia real dos documentos empatados. No total, foram concluídos 192 alinhamentos, correspondentes a 32 processos, duas referências e três ordenações.

## Consistência das referências

O modelo uniforme e as três referências por perfil passaram no teste de soundness do PM4Py. A exploração exaustiva das marcações confirmou, em todos os modelos, a possibilidade de alcançar o estado final a partir de qualquer estado alcançável, a ausência de transições mortas e a existência de um único estado terminal correspondente ao encerramento. As propriedades foram verificadas nas versões funcionais e nas projeções documentais.

Tabela 1 — Verificação estrutural das referências

| Referência | Estados alcançáveis | Atividades funcionais visíveis | Atividades na projeção |
| --- | --- | --- | --- |
| Uniforme v04 | 34 | 28 | 7 |
| Contrato | 33 | 26 | 7 |
| NE substitutiva | 28 | 23 | 6 |
| ATA RP | 26 | 21 | 6 |

Fonte: elaboração própria a partir das verificações no PM4Py.

Oito controles sintéticos confirmaram as regras de término e a sensibilidade a divergências. Foram aceitos contrato sem NE, contrato com NE anterior ou posterior, NE sem contrato e ATA RP sem formalização contratual posterior. A inversão da ordem de ETP e TR e a ausência do instrumento terminal produziram divergências. A consistência estrutural demonstrou o funcionamento computacional dessas referências; seu significado permaneceu condicionado à adequação funcional e ao mapeamento dos eventos.

## Resultados dos alinhamentos

O fitness médio foi calculado como média aritmética do fitness dos traços. Na ordenação crescente, a referência uniforme apresentou média de 0,4972, e as referências por perfil, 0,5474. A diferença de 0,0502 na escala de zero a um foi acompanhada de melhoria média nas outras duas ordenações, conforme a Tabela 2.

Tabela 2 — Fitness médio segundo a referência e a ordenação dos documentos empatados

| Ordenação | Uniforme | Por perfil | Diferença |
| --- | --- | --- | --- |
| ID crescente | 0,4972 | 0,5474 | 0,0502 |
| ID decrescente | 0,4878 | 0,5377 | 0,0499 |
| Alternativa reprodutível | 0,4939 | 0,5441 | 0,0502 |

Fonte: elaboração própria. Valores calculados para os mesmos 32 traços em cada ordenação.

Na ordenação crescente, os movimentos exclusivos do modelo visível diminuíram de 70 para 31, enquanto os movimentos exclusivos do log passaram de 273 para 264. A soma passou de 343 para 295. Essas contagens descrevem as diferenças entre traços e referências, sem equivaler a uma contagem de irregularidades ou de falsos positivos jurídicos.

Tabela 3 — Fitness médio por instrumento ou objetivo administrativo

| Perfil | Processos | Uniforme | Por perfil |
| --- | --- | --- | --- |
| ATA RP | 14 | 0,4438 | 0,5410 |
| Termo contratual | 12 | 0,5159 | 0,5393 |
| NE substitutiva | 6 | 0,5844 | 0,5785 |

Fonte: elaboração própria. Ordenação por identificador crescente.

O resultado não foi homogêneo. Em cada uma das três ordenações, 28 processos apresentaram aumento e quatro apresentaram redução do fitness. No conjunto de NE substitutiva, a média diminuiu ligeiramente, embora a soma dos movimentos visíveis tenha caído de 65 para 63. Essa diferença foi compatível com o caráter normalizado do fitness e com a mudança do tamanho da referência, razão pela qual sua interpretação foi acompanhada das contagens de movimentos.

Em dois dos quatro casos com redução, a quantidade de movimentos visíveis permaneceu igual, mas a normalização mudou. Nos outros dois, classificados como NE substitutiva, o log continha um documento do tipo Contrato. A retirada da atividade contratual da referência fez esse documento contar como movimento exclusivo do log. A classificação da conferência foi preservada, sem atribuição de função ao documento apenas a partir de seu tipo.

No subconjunto de 21 casos com data até o corte e tipo terminal presente, a média passou de 0,5214 para 0,5909 na ordem crescente; de 0,4991 para 0,5675 na decrescente; e de 0,5084 para 0,5773 na alternativa reprodutível. O critério desse subconjunto verificou a presença do tipo terminal, sem pressupor identidade entre sua data de geração e o marco informado. Suas médias não foram generalizadas aos demais casos.

Seis processos apresentaram variação do fitness por perfil entre as ordenações, com amplitude máxima de 0,1818. Ainda assim, a direção do efeito individual permaneceu: os mesmos 28 processos melhoraram e os mesmos quatro apresentaram redução nas três ordenações. Nenhum dos 32 traços alcançou aderência integral, mesmo após a projeção documental.

## Discussão dos achados

Os resultados forneceram apoio exploratório à pertinência de considerar instrumento e objetivo administrativo na escolha da referência de conformidade. A redução dos movimentos exclusivos do modelo e o aumento médio do fitness indicaram que parte das diferenças observadas dependia dos requisitos impostos pela referência. A coexistência de ATA RP, termo contratual e NE substitutiva mostrou que um encerramento uniforme não descreveu igualmente os perfis analisados.

A comparação incorporou, conjuntamente, a escolha do perfil, a alteração do marco de término e a opcionalidade do empenho no perfil contratual. Consequentemente, o ganho médio não foi atribuído exclusivamente à estratificação, nem demonstrou superioridade sobre qualquer referência agregada possível. O achado incidiu sobre as referências construídas e o conjunto observado.

A cobertura documental também delimitou a interpretação. Aprovações e tramitações sem correspondência unívoca não foram verificadas. Documentos de mesmo tipo permaneceram separados, de modo que versões de TR, pesquisas sucessivas ou atas relacionadas a itens distintos puderam gerar movimentos exclusivos do log. Essas ocorrências não foram classificadas automaticamente como retrabalho. A inclusão de traços sem encerramento representado na janela original também impediu interpretar todo movimento exclusivo do modelo como omissão de atividade concluída.

O critério administrativo de sucesso e a aderência do fluxo foram tratados como medidas distintas. A emissão do instrumento pôde atender ao objetivo do processo sem que toda a sequência documental coincidisse com a referência. A ausência de aderência integral, as reduções individuais e a sensibilidade temporal integraram os resultados, preservando o caráter analítico da comparação. Os achados sustentaram a utilidade da adequação contextual das referências, dentro do alcance documental e dos perfis efetivamente examinados.

## Referência técnica e material de reprodução

PROCESS INTELLIGENCE SOLUTIONS. PM4Py: módulo de alinhamentos de redes de Petri. Código-fonte. Disponível em: https://github.com/process-intelligence-solutions/pm4py/blob/release/pm4py/algo/conformance/alignments/petri_net/algorithm.py. Acesso em: 25 nov. 2026. Versão executada: 2.7.23.12.

Os modelos, os mapeamentos, os resultados agregados e o código de reprodução foram organizados no repositório da pesquisa: https://github.com/fjebrahim/processmining/tree/main/analises/pm4py_2026-11-25.
