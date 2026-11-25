# Achados da verificação no PM4Py

Resultados de 25/11/2026 para a tese de Fernando Ebrahim sobre contratações no TRE-TO.

## Relatório para a tese

- [Texto acadêmico](Resultados_PM4Py_Para_Tese.md)
- [Documento Word](Resultados_PM4Py_Para_Tese.docx)

## Resultados

Foram concluídos 192 alinhamentos para 32 pregões, com duas referências e três ordenações. O fitness médio passou de 0,4972 para 0,5474 na ordem crescente. Os mesmos 28 casos melhoraram e quatro reduziram o fitness nas três ordenações. Nenhum caso foi integralmente aderente. A análise é documental e não comprova regularidade jurídica.

- [Resumo agregado](resultados/resumo_comparacao.csv)
- [Verificações estruturais](resultados/verificacao_estrutural.csv)
- [Controles sintéticos](resultados/controles_semanticos.csv)
- [Mapeamento das atividades](resultados/mapeamento_atividades.csv)
- [Modelos](modelos/)

## Dados tratados e reprodução completa

O [pacote de dados tratados](dados_tratados/) reúne a base de entrada, a classificação dos 63 casos codificados e os resultados individuais. Foram removidos nomes, descrições livres, unidades, links SEI e identificadores originais. As datas foram convertidas em tempo relativo por caso. Os 192 alinhamentos foram reexecutados e mantiveram os mesmos resultados individuais e agregados.

Para reproduzir integralmente, utilizar fontes, requirements.txt e verificar_pm4py_20261125.py dentro de dados_tratados. O script da raiz desta pasta foi mantido como registro da versão inicial; a versão que preserva a ordem alternativa com identificadores codificados é a do pacote tratado.

A documentação metodológica e os controles de publicação estão no README e em verificacao_publicacao.json do pacote. Os modelos são referências experimentais, sem presunção de homologação institucional.
