def query_sap_zt438():
    return """
    select * 
    from db_mgd_corp_parceiro.v_sap_zt438_estoque_claro_mov
    where dat_ref = (select max(dat_ref) from db_mgd_corp_parceiro.v_sap_zt438_estoque_claro_mov)
    """


##########################################################################################
# Busca os registros dos últimos 3 anos da tabela PRD_BI_DW.DW_ATLP_HISTORICO_EQPMNT_NET #
# Mantém movimentação mais recente do ID_EQUIPAMENTO.                                    #
# Identifica estado, modelo, operação e local MAIS RECENTE do equipamento.               #
# Retorna informação AGREGADA.                                                           #
##########################################################################################
def query_eqpmnt_agg_status():
    return """
    SELECT t2.id_estado_equipamento,
           t2.id_modelo_equipamento,
           t2.id_operacao,
           t2.id_local,
           SUM(1) AS qtde
    FROM 
        (
        SELECT t1.*,
               ROW_NUMBER() 
               OVER 
                   (
                   PARTITION BY t1.id_equipamento 
                   ORDER BY t1.dh_historico_equipamento DESC, t1.id_historico_equipamento DESC
                   ) AS rownumber
        FROM prd_bi_dw.dw_atlp_historico_eqpmnt_net t1
        WHERE t1.dh_historico_equipamento >= (SYSDATE - 365 * 3)
              AND t1.dh_historico_equipamento < SYSDATE
              AND t1.fl_status_bi = 'A'
              AND t1.nr_serie NOT LIKE 'ANT%'
        ) t2
    INNER JOIN prd_bi_dw.dw_atlp_enderecavel_net t3 
        ON t2.id_equipamento = t3.id_equipamento 
        AND t3.fl_status_bi = 'A'
    INNER JOIN prd_bi_dw.dw_atlp_mod_equip_tp_ender_net t4 
        ON t3.id_mod_equip_tipo_ender = t4.id_mod_equip_tipo_ender 
        AND t4.fl_status_bi = 'A' 
        AND t4.fc_enderecavel_principal = 'S'
    INNER JOIN prd_bi_dw.dw_atlp_local_net t5 
        ON t2.id_local = t5.id_local 
        AND t5.fl_status_bi = 'A'
    INNER JOIN prd_bi_dw.dw_atlp_tipo_local_net t6 
        ON t5.id_tipo_local = t6.id_tipo_local 
        AND t6.id_tipo_local <> 6 
        AND t6.fl_status_bi = 'A'
    WHERE t2.id_estado_equipamento = 2
          AND t2.rownumber = 1
    GROUP BY t2.id_estado_equipamento, 
             t2.id_modelo_equipamento, 
             t2.id_operacao, 
             t2.id_local
    """


def query_sap_mblb():
    return """
    select
        num_conta_fornecedor as COD_SAP_LOCAL,
        num_material  as COD_MATERIAL,
        cod_empresa as COD_EMPRESA,
        num_utilizacao_livre as ESTOQ_MBLB,
        dat_ref
    from db_mgd_corp_parceiro.v_extr_sap_mblb_estoq_subcontr
    where dat_ref = (select max(dat_ref) from db_mgd_corp_parceiro.v_extr_sap_mblb_estoq_subcontr)
    """


def query_local():
    return """
    SELECT *
    FROM DB_MGD_EXPER_TERMINAL.V_LOCAL 
    WHERE ID_TIPO_LOCAL <> 6
    """


def query_modelo_equipamento():
    return """
    SELECT *
    FROM DB_MGD_EXPER_TERMINAL.V_MODELO_EQUIPAMENTO
    """


def query_sap_mb51():
    return """
    select * from db_mgd_corp_parceiro.v_sap_mb51_documento_material
    where num_conta_fornecedor like 'CBT%' 
    and dat_ref >= 20240101
    and num_material like '00000000002%'
    and dsc_visao_mestre_deposito = ''
    and cod_tipo_movimento <> 'Y51'
    """


def query_material_campo():
    return """
    SELECT  M.DAT_MOVIMENTO,
            M.NUM_CONTA,
            M.COD_BASE,
            M.DW_TIPO_MATERIAL_CLASSE,
            M.COD_TIPO_MATERIAL_CAMPO,
            M.QTD_MATERIAL,
            M.COD_LOGIN,
            M.DSC_NUM_SERIAL 
    FROM DWH.BI_FP_MATERIAL_CAMPO M 
    WHERE M.DAT_MOVIMENTO >= SysDate - 112 
    AND M.QTD_MATERIAL < 1000 
    AND M.COD_LOGIN not Like 'T%' 
    AND M.COD_LOGIN not Like 'Z%' 
    AND M.COD_POOL = 'install'
    """


###############################################################################################
# Cria uma CTE (HISTORICO_EQPMNT) para determinar o LOCAL ANTERIOR de cada ID_EQUIPAMENTO     #
# utilizando a função LAG na tabela PRD_BI_DW.DW_ATLP_HISTORICO_EQPMNT_NET para os registros  #
# ativos (FL_STATUS_BI) dos últimos 3 anos da tabela acima.                                   #
# Combina dados de movimentação e histórico das tabelas INN.FA_ATLP_MOV_TERM_OS e             #
# INN.FT_ATLP_MOV_TERM_OS com as informações calculadas na CTE.                               #
# Retorna informações DETALHADAS sobre movimentações recentes dos últimos 112 dias,           #
# incluindo: número de série, endereçável, operadora, contrato, e local anterior.             #
###############################################################################################
def query_eqpmnt_mov_hist():
    return """
    with HISTORICO_EQPMNT as 
    (
    select LAG(T1.ID_LOCAL) 
    over 
        (
        partition by T1.ID_EQUIPAMENTO 
        order by T1.DH_HISTORICO_EQUIPAMENTO
        ) as ID_LOCAL_ANTERIOR,
        T1.ID_HISTORICO_EQUIPAMENTO 
    from PRD_BI_DW.DW_ATLP_HISTORICO_EQPMNT_NET T1 
    where T1.FL_STATUS_BI = 'A' 
        and T1.DH_HISTORICO_EQUIPAMENTO < SysDate 
        and T1.DH_HISTORICO_EQUIPAMENTO > SysDate - 3 * 365
    ) 

    select  T1.NR_SERIE,
            T2.CD_ENDERECAVEL,
            T2.CD_OPERADORA,
            T2.CD_CONTRATO_NETSMS,
            T2.DH_HISTORICO_EQUIPAMENTO,
            t4.ID_LOCAL_ANTERIOR 
    from INN.FA_ATLP_MOV_TERM_OS T1 
    left join INN.FT_ATLP_MOV_TERM_OS T2 on T1.ID_HISTORICO_EQUIPAMENTO = T2.ID_HISTORICO_EQUIPAMENTO and T1.ID_HISTORICO_EQUIPAMENTO > 3 
    left join HISTORICO_EQPMNT t4 on T1.ID_HISTORICO_EQUIPAMENTO = t4.ID_HISTORICO_EQUIPAMENTO 
    where T1.PERIODO >= To_Char(Trunc(SysDate - 112, 'MM'), 'YYYYMM')
    """
