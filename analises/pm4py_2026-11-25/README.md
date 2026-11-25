# Achados da verificação no PM4Py

Resultados de 25/11/2026 para a tese de Fernando Ebrahim sobre contratações no TRE-TO.

## Relatório para a tese

- [Texto acadêmico](Resultados_PM4Py_Para_Tese.md)
- [Documento Word](Resultados_PM4Py_Para_Tese.docx)

## Resultados publicados

Foram concluídos 192 alinhamentos para 32 pregões, com duas referências e três ordenações de eventos empatados. O fitness médio passou de 0,4972 para 0,5474 na ordenação crescente. Em todas as ordenações, os mesmos 28 casos melhoraram e quatro apresentaram redução. Nenhum caso foi integralmente aderente. A verificação é documental e não comprova regularidade jurídica.

- [Comparações agregadas](resultados/resumo_comparacao.csv)
- [Verificações estruturais](resultados/verificacao_estrutural.csv)
- [Controles sintéticos](resultados/controles_semanticos.csv)
- [Mapeamento de atividades](resultados/mapeamento_atividades.csv)
- [Mapeamento documental](resultados/mapeamento_documental.csv)
- [Modelos e projeções](modelos/)

Esta pasta reúne resultados agregados, referências computacionais e código. O dataset bruto, a classificação individual e os registros detalhados de eventos e alinhamentos não integram esta publicação.

## Reprodução local

A execução utilizou Python 3.12.14 e PM4Py 2.7.23.12. O código é fornecido para reprodução em ambiente que disponha das entradas de análise.

1. Instalar as dependências de requirements.txt.
2. Preparar localmente fontes/dataset_original.csv e fontes/casos_analisados.csv, a partir das entradas autorizadas da pesquisa.
3. Executar python verificar_pm4py_20261125.py nesta pasta.

O schema da classificação usada pelo código requer processo, rito, instrumento, marco_informado (ISO 8601 ou vazio) e janela. Os valores de janela para a seleção até o corte são Até 03/06/2026. O dataset e a classificação devem corresponder aos mesmos 63 processos do experimento. As fontes v04 estão em fontes/modelos_v04. A reprodução gera saídas individuais localmente; elas não são publicadas pelo script.

As três referências v05 incorporam o critério de encerramento informado pelo pesquisador: contrato ou NE no perfil correspondente e ATA RP para registro de preços. São derivações experimentais, sem presunção de homologação institucional. A comparação modifica conjuntamente perfil, término e opcionalidade do empenho, conforme discutido no relatório.
