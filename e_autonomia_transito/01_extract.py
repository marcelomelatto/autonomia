query_true = """

WITH 
janela_reserva_query AS (
    SELECT t1.*,
    CASE 
        WHEN ind_status_reserva = 'ATENDIDA' THEN '   X'
        ELSE NULL
    END AS Atendida,
    CASE 
        WHEN ind_status_reserva = 'LIBERADA' THEN '   X'
        ELSE NULL
    END AS Liberada,
    CASE 
        WHEN ind_status_reserva = 'ELIMINADA' THEN '   X'
        ELSE NULL
    END AS Eliminada
    FROM db_mgd_corp_parceiro.v_sap_ztc360_reserva_log t1
    WHERE from_unixtime(unix_timestamp(t1.dat_reserva_material, 'dd.MM.yyyy')) >= date_sub(current_date, 90)
),

ztc360 AS (
    SELECT * 
    FROM janela_reserva_query 
),

janela_reserva AS (
    SELECT *
    FROM (
        SELECT  t1.*,
                row_number() over ( 
                    PARTITION BY 
                        t1.num_reserva,
                        t1.num_item_reserva_transferencia
                    ORDER BY
                        t1.dat_ref DESC
                ) AS rank_
        FROM ztc360 t1
        WHERE t1.cod_tipo_material IN ('EMIS','ETER')
        AND t1.cod_tipo_movimento IN ('X33','X41','X43','X51')
    ) AS subquery
    WHERE rank_ = 1
),

eficiencia_entrega AS (
    SELECT *
    FROM (
        SELECT  
                t1.*,
                ROW_NUMBER() OVER(
                    PARTITION BY num_pedido 
                    ORDER BY UNIX_TIMESTAMP(dat_baixa_evento, 'dd/MM/yyyy') ASC
                ) AS linha
        FROM db_mgd_corp_parceiro.v_tms_eficiencia_entrega t1
        WHERE t1.dat_ref >= year(date_sub(current_date, 120)) * 10000 + month(date_sub(current_date, 120)) * 100 + day(date_sub(current_date, 120))
        AND dsc_nome_empresa IN ('CLARO TV', 'NET', "CLARO NXT")
        AND CAST(num_pedido AS INT) >= 1000000
    ) AS subquery
    WHERE linha = 1
),

monitoramento_entrega AS (
    SELECT  
            t1.num_pedido,
            t1.sgl_uf_unidade,
            t1.sgl_uf_entrega,
            t1.num_nota_fiscal,
            t1.num_protocolo_tms,
            t1.dsc_transportadora,
            t1.dsc_cidade_unidade,
            t1.dsc_cidade_entrega,
            t1.ind_entrega_urgente,
            t1.num_serie_nota_fiscal,
            t1.dsc_ultima_ocorr_transporte
    FROM db_mgd_corp_parceiro.v_tms_monitoramento_entrega t1
    WHERE t1.dat_ref = (SELECT MAX(dat_ref) FROM db_mgd_corp_parceiro.v_tms_monitoramento_entrega)
),

nota_cancelada AS (
    SELECT DISTINCT
            t1.num_pedido,
            t1.num_centro_sap,
            t1.num_nota_fiscal,
            t1.num_serie_nota_fiscal
    FROM db_mgd_corp_parceiro.v_tms_nota_fiscal_cancelada t1 
    WHERE t1.dat_ref = (SELECT MAX(dat_ref) FROM db_mgd_corp_parceiro.v_tms_nota_fiscal_cancelada)
)

SELECT
        t01.*,
        COALESCE(t02.num_reserva, t03.num_reserva, t04.num_reserva) AS num_reserva_2,
        COALESCE(t02.ind_status_reserva, t03.ind_status_reserva, t04.ind_status_reserva) AS ind_status_reserva_2,
        COALESCE(t02.num_nota_fiscal, t03.num_nota_fiscal, t04.num_nota_fiscal) AS num_nota_fiscal_2,
        COALESCE(t02.num_serie_nota_fiscal, t03.num_serie_nota_fiscal, t04.num_serie_nota_fiscal) AS num_serie_nota_fiscal_2,
        
        COALESCE(t05.num_protocolo_tms, t06.num_protocolo_tms, t07.num_protocolo_tms, t08.num_protocolo_tms) AS num_protocolo_tms,
        COALESCE(t05.num_romaneio_carga, t06.num_romaneio_carga) AS num_romaneio_carga,
        COALESCE(t05.sgl_uf_entrega, t06.sgl_uf_entrega, t07.sgl_uf_entrega, t08.sgl_uf_entrega) AS sgl_uf_entrega,
        COALESCE(t05.dsc_cidade_entrega, t06.dsc_cidade_entrega, t07.dsc_cidade_entrega, t08.dsc_cidade_entrega) AS dsc_cidade_entrega,
        COALESCE(t05.dsc_transportadora, t06.dsc_transportadora, t07.dsc_transportadora, t08.dsc_transportadora) AS dsc_transportadora,
        COALESCE(t05.dat_prazo_entrega_original, t06.dat_prazo_entrega_original) AS dat_prazo_entrega_original,
        COALESCE(t05.dat_prazo_entrega_atual, t06.dat_prazo_entrega_atual) AS dat_prazo_entrega_atual,
        COALESCE(t05.dat_baixa_evento, t06.dat_baixa_evento) AS dat_baixa_evento,
        COALESCE(t05.sgl_uf_unidade, t06.sgl_uf_unidade, t07.sgl_uf_unidade, t08.sgl_uf_unidade) AS sgl_uf_unidade,
        COALESCE(t05.dsc_cidade_unidade, t06.dsc_cidade_unidade, t07.dsc_cidade_unidade, t08.dsc_cidade_unidade) AS dsc_cidade_unidade,
        COALESCE(t05.ind_tipo_baixa_evento, t06.ind_tipo_baixa_evento) AS ind_tipo_baixa_evento,
        COALESCE(t05.ind_entrega_urg_canal_vermelho, t06.ind_entrega_urg_canal_vermelho, t07.ind_entrega_urgente, t08.ind_entrega_urgente) AS ind_entrega_urg_canal_vermelho,
        COALESCE(t07.dsc_ultima_ocorr_transporte, t08.dsc_ultima_ocorr_transporte) AS dsc_ultima_ocorr_transporte,
        CASE 
            WHEN t09.num_pedido IS NULL THEN 'N' 
            ELSE 'S' 
        END AS ind_nota_cancelada

FROM janela_reserva t01
LEFT JOIN (
    SELECT *
    FROM janela_reserva
    WHERE cod_tipo_movimento IN ('X41', 'X43', 'X51')
) t02 ON t01.cod_tipo_movimento = 'X33'
    AND CAST(t01.num_reserva AS INT) + 1 = CAST(t02.num_reserva AS INT)
    AND t01.num_item_reserva_transferencia = t02.num_item_reserva_transferencia
    AND t01.cod_material = t02.cod_material
    AND t01.qtd_reservada = t02.qtd_reservada
    AND t01.dat_reserva_material = t02.dat_reserva_material
    AND t01.cod_centro_receptor = t02.cod_centro_protocolo
    
LEFT JOIN (
    SELECT *
    FROM janela_reserva
    WHERE cod_tipo_movimento IN ('X41', 'X43', 'X51')
) t03 ON t01.cod_tipo_movimento = 'X33'
    AND t02.num_reserva IS NULL
    AND CAST(t01.num_reserva AS INT) + 2 = CAST(t03.num_reserva AS INT)
    AND t01.num_item_reserva_transferencia = t03.num_item_reserva_transferencia
    AND t01.cod_material = t03.cod_material
    AND t01.qtd_reservada = t03.qtd_reservada
    AND t01.dat_reserva_material = t03.dat_reserva_material
    AND t01.cod_centro_receptor = t03.cod_centro_protocolo

LEFT JOIN (
    SELECT *
    FROM janela_reserva
    WHERE cod_tipo_movimento IN ('X41', 'X43', 'X51')
) t04 ON t01.cod_tipo_movimento = 'X33'
    AND t02.num_reserva IS NULL
    AND t03.num_reserva IS NULL
    AND t01.num_item_reserva_transferencia = t04.num_item_reserva_transferencia
    AND t01.cod_material = t04.cod_material
    AND t01.qtd_reservada = t04.qtd_reservada
    AND t01.dat_reserva_material = t04.dat_reserva_material
    AND t01.cod_centro_receptor = t04.cod_centro_protocolo
    
LEFT JOIN eficiencia_entrega t05 ON CAST(t01.num_reserva AS INT) = CAST(t05.num_pedido AS INT)

LEFT JOIN eficiencia_entrega t06 ON t05.num_pedido IS NULL
    AND t01.cod_centro_protocolo = t06.cod_centro_sap
    AND CAST(t01.num_nota_fiscal AS INT) = CAST(t06.num_nota_fiscal AS INT)
    AND CAST(t01.num_serie_nota_fiscal AS INT) = CAST(t06.num_serie_nota_fiscal AS INT)

LEFT JOIN monitoramento_entrega t07 ON t05.num_pedido IS NULL
    AND t06.num_pedido IS NULL
    AND CAST(t01.num_reserva AS INT) = CAST(t07.num_pedido AS INT)

LEFT JOIN monitoramento_entrega t08 ON t05.num_pedido IS NULL
    AND t06.num_pedido IS NULL
    AND t07.num_pedido IS NULL
    AND t01.cod_centro_protocolo = (
        CASE
            WHEN t08.dsc_cidade_unidade = 'CONTAGEM' THEN 'N390'
            WHEN t08.dsc_cidade_unidade = 'SAO PAULO' THEN 'N191'
            WHEN t08.dsc_cidade_unidade = 'JABOATAO DOS GUARARAPES' THEN 'N890'
            WHEN t08.dsc_cidade_unidade = 'RECIFE' THEN 'N890'
            WHEN t08.dsc_cidade_unidade = 'BRASILIA' THEN 'N690'
            WHEN t08.dsc_cidade_unidade = 'PAVUNA' THEN '21YC'
            WHEN t08.dsc_cidade_unidade = 'RIO DE JANEIRO' THEN 'N290'
            WHEN t08.dsc_cidade_unidade = 'CAMPINAS' THEN 'N190'
            WHEN t08.dsc_cidade_unidade = 'DIADEMA' THEN 'N191'
            WHEN t08.dsc_cidade_unidade = 'MANAUS' THEN 'N990'
            WHEN t08.dsc_cidade_unidade = 'SAO JOSE' THEN 'N491'
            WHEN t08.dsc_cidade_unidade = 'PALHOCA' THEN 'N491'
            WHEN t08.dsc_cidade_unidade = 'BARUERI' THEN 'N192'
        END)
    AND CAST(t01.num_nota_fiscal AS INT) = CAST(t08.num_nota_fiscal AS INT)
    AND CAST(t01.num_serie_nota_fiscal AS INT) = CAST(t08.num_serie_nota_fiscal AS INT)

LEFT JOIN nota_cancelada t09 ON CAST(t01.num_reserva AS INT) = CAST(t09.num_pedido AS INT)
    OR (t01.cod_centro_protocolo = t09.num_centro_sap
    AND CAST(t01.num_nota_fiscal AS INT) = CAST(t09.num_nota_fiscal AS INT)
    AND CAST(t01.num_serie_nota_fiscal AS INT) = CAST(t09.num_serie_nota_fiscal AS INT))

"""

query = """
WITH 
janela_reserva_query AS (
    SELECT t1.*,
    CASE 
        WHEN ind_status_reserva = 'ATENDIDA' THEN "   X"
        ELSE NULL
    END AS Atendida,
    CASE 
        WHEN ind_status_reserva = 'LIBERADA' THEN "   X"
        ELSE NULL
    END AS Liberada,
    CASE 
        WHEN ind_status_reserva = 'ELIMINADA' THEN "   X"
        ELSE NULL
    END AS Eliminada
    FROM db_mgd_corp_parceiro.v_sap_ztc360_reserva_log t1
    WHERE from_unixtime(unix_timestamp(t1.dat_reserva_material, 'dd.MM.yyyy')) >= date_sub(current_date, 90)
),

ztc360 AS (
    SELECT * 
    FROM janela_reserva_query 
),

janela_reserva AS (
    SELECT *
    FROM (
        SELECT t1.*,
               row_number() over ( 
                   PARTITION BY t1.num_reserva, t1.num_item_reserva_transferencia
                   ORDER BY t1.dat_ref desc
               ) as rank_
        FROM ztc360 t1
        WHERE t1.cod_tipo_material IN ('EMIS','ETER')
        AND t1.cod_tipo_movimento IN ('X33','X41','X43','X51')
    )
    WHERE rank_ = 1
),

eficiencia_entrega AS (
    SELECT *
    FROM (
        SELECT t1.*, ROW_NUMBER() OVER(
            PARTITION BY num_pedido 
            ORDER BY UNIX_TIMESTAMP(dat_baixa_evento, 'dd/MM/yyyy') ASC
        ) AS linha
        FROM db_mgd_corp_parceiro.v_tms_eficiencia_entrega t1
        WHERE t1.dat_ref >= year(date_sub(current_date, 120)) * 10000 + month(date_sub(current_date, 120)) * 100 + day(date_sub(current_date, 120))
        AND dsc_nome_empresa IN ('CLARO TV', 'NET', "CLARO NXT")
        AND CAST(num_pedido AS INT) >= 1000000
    )
    WHERE linha = 1
), 

monitoramento_entrega AS (
    SELECT t1.num_pedido,
           t1.sgl_uf_unidade,
           t1.sgl_uf_entrega,
           t1.num_nota_fiscal,
           t1.num_protocolo_tms,
           t1.dsc_transportadora,
           t1.dsc_cidade_unidade,
           t1.dsc_cidade_entrega,
           t1.ind_entrega_urgente,
           t1.num_serie_nota_fiscal,
           t1.dsc_ultima_ocorr_transporte
    FROM db_mgd_corp_parceiro.v_tms_monitoramento_entrega t1
    WHERE t1.dat_ref = (SELECT max(dat_ref) FROM db_mgd_corp_parceiro.v_tms_monitoramento_entrega)
),

nota_cancelada AS (
    SELECT DISTINCT t1.num_pedido,
           t1.num_centro_sap,
           t1.num_nota_fiscal,
           t1.num_serie_nota_fiscal
    FROM db_mgd_corp_parceiro.v_tms_nota_fiscal_cancelada t1
    WHERE t1.dat_ref = (SELECT max(dat_ref) FROM db_mgd_corp_parceiro.v_tms_nota_fiscal_cancelada)
)

SELECT t01.*,
       COALESCE(t02.num_reserva, t03.num_reserva, t04.num_reserva) AS num_reserva_2,
       COALESCE(t02.ind_status_reserva, t03.ind_status_reserva, t04.ind_status_reserva) AS ind_status_reserva_2,
       COALESCE(t02.num_nota_fiscal, t03.num_nota_fiscal, t04.num_nota_fiscal) AS num_nota_fiscal_2,
       COALESCE(t02.num_serie_nota_fiscal, t03.num_serie_nota_fiscal, t04.num_serie_nota_fiscal) AS num_serie_nota_fiscal_2,
       COALESCE(t05.num_protocolo_tms, t06.num_protocolo_tms, t07.num_protocolo_tms, t08.num_protocolo_tms) AS num_protocolo_tms,
       COALESCE(t05.num_romaneio_carga, t06.num_romaneio_carga) AS num_romaneio_carga,
       COALESCE(t05.sgl_uf_entrega, t06.sgl_uf_entrega, t07.sgl_uf_entrega, t08.sgl_uf_entrega) AS sgl_uf_entrega,
       COALESCE(t05.dsc_cidade_entrega, t06.dsc_cidade_entrega, t07.dsc_cidade_entrega, t08.dsc_cidade_entrega) AS dsc_cidade_entrega,
       COALESCE(t05.dsc_transportadora, t06.dsc_transportadora, t07.dsc_transportadora, t08.dsc_transportadora) AS dsc_transportadora,
       COALESCE(t05.dat_prazo_entrega_original, t06.dat_prazo_entrega_original) AS dat_prazo_entrega_original,
       COALESCE(t05.dat_prazo_entrega_atual, t06.dat_prazo_entrega_atual) AS dat_prazo_entrega_atual,
       COALESCE(t05.dat_baixa_evento, t06.dat_baixa_evento) AS dat_baixa_evento,
       COALESCE(t05.sgl_uf_unidade, t06.sgl_uf_unidade, t07.sgl_uf_unidade, t08.sgl_uf_unidade) AS sgl_uf_unidade,
       COALESCE(t05.dsc_cidade_unidade, t06.dsc_cidade_unidade, t07.dsc_cidade_unidade, t08.dsc_cidade_unidade) AS dsc_cidade_unidade,
       COALESCE(t05.ind_tipo_baixa_evento, t06.ind_tipo_baixa_evento) AS ind_tipo_baixa_evento,
       COALESCE(t05.ind_entrega_urg_canal_vermelho, t06.ind_entrega_urg_canal_vermelho, t07.ind_entrega_urgente, t08.ind_entrega_urgente) AS ind_entrega_urg_canal_vermelho,
       COALESCE(t07.dsc_ultima_ocorr_transporte, t08.dsc_ultima_ocorr_transporte) AS dsc_ultima_ocorr_transporte,
       CASE WHEN t09.num_pedido IS NULL THEN 'N' ELSE 'S' END AS ind_nota_cancelada
FROM janela_reserva t01
LEFT JOIN (
    SELECT *
    FROM janela_reserva
    WHERE cod_tipo_movimento IN ('X41','X43','X51') AND rank_ = 1
) t02
    ON t01.cod_tipo_movimento = 'X33'
    AND CAST(t01.num_reserva AS INT) + 1 = CAST(t02.num_reserva AS INT)
    AND t01.num_item_reserva_transferencia = t02.num_item_reserva_transferencia
    AND t01.cod_material = t02.cod_material
    AND t01.qtd_reservada = t02.qtd_reservada
    AND t01.dat_reserva_material = t02.dat_reserva_material
    AND t01.cod_centro_receptor = t02.cod_centro_protocolo

LEFT JOIN (
    SELECT *
    FROM janela_reserva
    WHERE cod_tipo_movimento IN ('X41','X43','X51') AND rank_ = 1
) t03
    ON t01.cod_tipo_movimento = 'X33'
    AND t02.num_reserva IS NULL
    AND CAST(t01.num_reserva AS INT) + 2 = CAST(t03.num_reserva AS INT)
    AND t01.num_item_reserva_transferencia = t03.num_item_reserva_transferencia
    AND t01.cod_material = t03.cod_material
    AND t01.qtd_reservada = t03.qtd_reservada
    AND t01.dat_reserva_material = t03.dat_reserva_material
    AND t01.cod_centro_receptor = t03.cod_centro_protocolo

LEFT JOIN (
    SELECT *
    FROM janela_reserva
    WHERE cod_tipo_movimento IN ('X41','X43','X51') AND rank_ = 1
) t04
    ON t01.cod_tipo_movimento = 'X33'
    AND t02.num_reserva IS NULL
    AND t03.num_reserva IS NULL
    AND t01.num_item_reserva_transferencia = t04.num_item_reserva_transferencia
    AND t01.cod_material = t04.cod_material
    AND t01.qtd_reservada = t04.qtd_reservada
    AND t01.dat_reserva_material = t04.dat_reserva_material
    AND t01.cod_centro_receptor = t04.cod_centro_protocolo

LEFT JOIN eficiencia_entrega t05
    ON CAST(t01.num_reserva AS INT) = CAST(t05.num_pedido AS INT)

LEFT JOIN eficiencia_entrega t06
    ON t05.num_pedido IS NULL
    AND t01.cod_centro_protocolo = t06.cod_centro_sap
    AND CAST(t01.num_nota_fiscal AS INT) = CAST(t06.num_nota_fiscal AS INT)
    AND CAST(t01.num_serie_nota_fiscal AS INT) = CAST(t06.num_serie_nota_fiscal AS INT)

LEFT JOIN monitoramento_entrega t07
    ON t05.num_pedido IS NULL
    AND t06.num_pedido IS NULL
    AND CAST(t01.num_reserva AS INT) = CAST(t07.num_pedido AS INT)

LEFT JOIN monitoramento_entrega t08
    ON t05.num_pedido IS NULL
    AND t06.num_pedido IS NULL
    AND t07.num_pedido IS NULL
    AND t01.cod_centro_protocolo = CASE
                                        WHEN t08.dsc_cidade_unidade = 'CONTAGEM' THEN 'N390'
                                        WHEN t08.dsc_cidade_unidade = 'SAO PAULO' THEN 'N191'
                                        WHEN t08.dsc_cidade_unidade = 'JABOATAO DOS GUARARAPES' THEN 'N890'
                                        WHEN t08.dsc_cidade_unidade = 'RECIFE' THEN 'N890'
                                        WHEN t08.dsc_cidade_unidade = 'BRASILIA' THEN 'N690'
                                        WHEN t08.dsc_cidade_unidade = 'SANTO ANDRE' THEN 'N021'
                                    END

LEFT JOIN nota_cancelada t09
    ON CAST(t01.num_reserva AS INT) = CAST(t09.num_pedido AS INT)

"""

query_MB51 = """
    select distinct
        t1.dat_lancamento_documento as mb51_dat_lancamento_documento,
        t1.num_conta_fornecedor     as mb51_num_conta_fornecedor,
        t1.num_reserva_dependentes  as mb51_num_reserva_dependentes,
        t1.num_material             as mb51_num_material
    from  db_mgd_corp_parceiro.v_sap_mb51_documento_material t1
    where t1.cod_tipo_movimento in ('X33', 'X41', 'X43', 'X51') 
    and t1.cod_empresa in ('001', '701', '881') 
    and t1.dat_ref >= '20220101' 
    and t1.dat_referencia >= '202201'
    and t1.num_reserva_dependentes <> ''
"""

vlocal = """
    SELECT cd_local_sap,
           id_local,
           sg_empresa_relacionamento
    FROM DB_MGD_EXPER_TERMINAL.V_LOCAL
    WHERE ID_TIPO_LOCAL<>6
    AND cd_local_sap IS NOT NULL
    AND sg_empresa_relacionamento IS NOT NULL
"""
