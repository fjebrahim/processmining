# Dados públicos tratados para reprodução do PM4Py

Esta pasta contém os dados de entrada e os resultados individuais tratados para divulgação acadêmica. O tratamento dos dados e a disponibilização pública foram autorizados pelo pesquisador, com remoção dos dados pessoais.

## Tratamento aplicado

Foram excluídos os campos de nomes de pessoas, descrição livre do objeto, unidades, números reais dos processos, identificadores SEI e links documentais. Os casos foram identificados por códigos CASO_001 a CASO_063 e os documentos por números técnicos novos. Não acompanha esta publicação uma chave que relacione esses códigos aos identificadores originais.

As datas foram transformadas por caso: a origem foi deslocada para 01/01/2000 e os demais instantes conservaram seus intervalos em relação a essa origem. Portanto, as datas desta pasta são sintéticas e não representam o calendário administrativo. A classificação Até 03/06/2026 refere-se à janela de observação da pesquisa original. A coluna ORDEM_EMPATE_ALTERNATIVA preserva apenas a ordenação técnica dos documentos no ensaio alternativo, sem expor o identificador utilizado na execução original.

O conjunto manteve 3.641 registros, 3.334 documentos distintos e 63 casos. As categorias documentais, os intervalos, os empates temporais e os instrumentos informados foram preservados. A transformação remove identificadores e reduz a possibilidade de associação direta, mas não constitui garantia absoluta de impossibilidade de reidentificação por padrões raros ou fontes externas. Esta pasta não contém textos de documentos, nomes, links SEI ou a chave de correspondência.

## Resultados e reprodução

Os 192 alinhamentos foram reexecutados com os dados tratados. Fitness, custos, contagens de movimentos e indicadores individuais permaneceram idênticos nas três ordenações. A verificação preservou a média de 0,4972 para a referência uniforme e 0,5474 para os perfis na ordem crescente.

```bash
python -m pip install -r requirements.txt
python verificar_pm4py_20261125.py
```

- fontes/dataset_original.csv: entrada tratada, com nome mantido para compatibilidade do código.
- fontes/casos_analisados.csv: classificação dos casos codificados e marcos relativos.
- fontes/modelos_v04 e modelos: referências e projeções.
- resultados: alinhamentos por caso, movimentos, cobertura dos 63 casos, eventos projetados, sensibilidade e resumos.
- verificacao_publicacao.json: controles de proteção e preservação dos resultados.

O relatório acadêmico e os resultados agregados também se encontram na pasta superior. Os resultados permanecem limitados à aderência documental dos 32 pregões comparados. As contratações diretas não foram avaliadas contra a referência de pregão.
