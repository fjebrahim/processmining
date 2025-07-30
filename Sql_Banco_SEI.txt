-- Definição da View (ou consulta para extração de metadados de processos)
-- CREATE OR REPLACE FORCE EDITIONABLE VIEW "ADMSEI"."VW_SEI_PROCESS_MINING" ("PROTOCOLO_PROC_EM_TRAMITACAO", "PROTOCOLO_FORMATADO_PESQUISA", "ID_PROTOCOLO", "PROTOCOLO_DESCRICAO", "PROTOCOLO_DTA_GERACAO", "TIPO_PROCEDIMENTO_NOME", "UF_SIGLA_NOME", "UNIDADE_SIGLA", "ID_PROCEDIMENTO", "DTH_ABERTURA") AS
-- set role dba; -- 
SELECT
    p.protocolo_formatado AS protocolo_proc_em_tramitacao, -- Protocolo formatado do processo
    p.protocolo_formatado_pesquisa AS protocolo_formatado_pesquisa, -- Protocolo formatado para pesquisa
    p.id_protocolo AS id_protocolo, -- Identificador único do processo (potencial CASE_ID)
    p.descricao AS protocolo_descricao, -- Descrição do processo
    to_char(p.dta_geracao, 'DD-MM-YYYY HH24:MI') AS protocolo_dta_geracao, -- Data e hora de geração do processo
    tp.nome AS tipo_procedimento_nome, -- Nome do tipo de procedimento
    concat(concat(uf.sigla, ' - '), uf.nome) AS uf_sigla_nome, -- Sigla e nome da UF
    uno.sigla AS unidade_sigla, -- Sigla da unidade
    pc.id_procedimento AS id_procedimento, -- ID do procedimento
    to_char(atv.dth_abertura, 'DD-MM-YYYY HH24:MI') AS dth_abertura, -- Data e hora de abertura da atividade (ID_TAREFA = 5)
    to_clob(dc.conteudo) AS conteudo, -- Conteúdo do documento (CLOB)
    dc.id_documento AS id_documento, -- ID do documento
    usu.nome AS nome_usuario_gerador -- Nome do usuário que gerou o processo
FROM
    admsei.protocolo p,
    admsei.orgao o,
    admsei.unidade uno,
    (SELECT * FROM admsei.uf WHERE id_uf = 7) uf, -- Filtra para a UF específica (Tocantins, id=7)
    admsei.procedimento pc,
    admsei.tipo_procedimento tp,
    admsei.documento doc,
    admsei.documento_conteudo dc,
    (SELECT * FROM admsei.atividade atva
     WHERE 1 = 1
       AND atva.DTH_CONCLUSAO = (
           SELECT max(atvi.DTH_CONCLUSAO) FROM admsei.atividade atvi
           WHERE atvi.id_protocolo = atva.id_protocolo
             AND atvi.ID_TAREFA = atva.ID_TAREFA
             AND rownum < 2
     )
  ) atv, -- Subconsulta para selecionar a última conclusão de uma atividade específica
  admsei.usuario usu
WHERE
    1 = 1
    AND p.sta_protocolo = 'P' -- Status do protocolo 'P' (Provavelmente "Processo")
    AND p.sta_estado IN ('0', '4') -- Status do estado (0 e 4)
    AND (p.sta_nivel_acesso_global <> 2 OR p.sta_nivel_acesso_local <> 2) -- Nível de acesso
    AND o.id_unidade = uno.id_unidade
    AND uno.id_orgao = o.id_orgao
    AND uno.sigla <> 'TESTE' -- Exclui unidades de teste
    AND uno.sin_ativo = 'S' -- Unidades ativas
    AND pc.id_procedimento = p.id_protocolo
    AND tp.id_tipo_procedimento = pc.id_tipo_procedimento
    AND p.id_protocolo = pc.id_procedimento
    AND pc.id_procedimento = doc.id_documento
    AND doc.id_documento = dc.id_documento
    AND pc.id_procedimento = atv.id_protocolo
    AND atv.ID_TAREFA = 5 -- Filtra por uma tarefa específica (ID 5)
    AND (p.descricao LIKE '%DESLOCAMENTO%' OR p.descricao LIKE '%VIAGEM%' OR p.descricao LIKE '%EVENTO%' OR p.descricao LIKE '%PARTICIPAÇÃO%') -- Filtra processos relacionados a viagens
    AND p.id_usuario_gerador = usu.id_usuario
;
