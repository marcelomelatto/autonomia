def query_hist_eqpmnt():
    return """
    select 
        Trunc(t1.DH_HISTORICO_EQUIPAMENTO) as dh_historico_equipamento,
        t1.ID_MODELO_EQUIPAMENTO,
        t4.CD_IBGE,
        t1.ID_LOCAL_ANTERIOR,
        t1.ID_LOCAL_ANTERIOR_2,
        t3.CD_OPERADORA,
        t4.NM_PRODUTO_ATUAL,
        Sum(1) as qtde 
    from 
        (
        select 
            /*+ paralel (8) */ t1.*,
            lag(t1.ID_LOCAL) over (partition by t1.ID_EQUIPAMENTO order by t1.DH_HISTORICO_EQUIPAMENTO) as id_local_anterior,
            lag(t1.ID_ESTADO_EQUIPAMENTO) over (partition by t1.ID_EQUIPAMENTO order by t1.DH_HISTORICO_EQUIPAMENTO) as id_estado_equipamento_anterior,
            lag(t1.ID_LOCAL, 2) over (partition by t1.ID_EQUIPAMENTO order by t1.DH_HISTORICO_EQUIPAMENTO) as id_local_anterior_2
        from PRD_BI_DW.DW_ATLP_HISTORICO_EQPMNT_NET t1 
        where 
            t1.DH_HISTORICO_EQUIPAMENTO >= TO_DATE('01/01/2021', 'DD/MM/YYYY')
            and t1.DH_HISTORICO_EQUIPAMENTO <= (SysDate) - interval '3' hour
            and t1.FL_STATUS_BI = 'A'
        ) t1 
    inner join PRD_BI_DW.DW_ATLP_LOCAL_NET t2 
        on t1.ID_LOCAL = t2.ID_LOCAL 
        and t2.FL_STATUS_BI = 'A' 
        and t2.ID_TIPO_LOCAL = 6 
    inner join PRD_BI_DW.DW_ATLP_OPERACAO_NET t3 
        on t1.ID_OPERACAO = t3.ID_OPERACAO 
        and t3.FL_STATUS_BI = 'A' 
    inner join inn.dw_itg_ordem_servico_net t4 
        on t1.CD_OS = t4.NR_ORDEM_SERVICO 
        and t3.CD_OPERADORA = case when t4.CD_BASE_SISTEMA = 'CTV' then 21 else t4.CD_OPERADORA end
    where 
        t1.ID_ESTADO_EQUIPAMENTO = 2
        and t1.DH_HISTORICO_EQUIPAMENTO >= TO_DATE('01/01/2024', 'DD/MM/YYYY')
    group by 
        Trunc(t1.DH_HISTORICO_EQUIPAMENTO),
        t1.ID_MODELO_EQUIPAMENTO,
        t4.CD_IBGE,
        t1.ID_LOCAL_ANTERIOR,
        t1.ID_LOCAL_ANTERIOR_2,
        t3.CD_OPERADORA,
        t4.NM_PRODUTO_ATUAL
    """


def query_mov_mtrl():
    return """
    select 
        num_conta_fornecedor,
        dat_lancamento_documento,
        sum(cast(regexp_replace(translate(qtd_unidade_medida, '.', ''), ',', '.') as decimal(10,2))) as qtd_unidade_medida,
        cod_centro_contrato_nacional,
        num_material,
        dsc_barra_status,
        cod_tipo_movimento,
        num_documento_material,
        cod_empresa
    from db_mgd_corp_parceiro.v_sap_mb51_documento_material
    where 
        dat_ref >= 20240101
        and cod_tipo_movimento in ('Y51', 'Y52')
        and dsc_barra_status in ('CAPEX', 'OPEX')
        and num_conta_fornecedor NOT LIKE 'CBT%'
    group by 
        num_conta_fornecedor,
        dat_lancamento_documento,
        cod_centro_contrato_nacional,
        num_material,
        dsc_barra_status,
        cod_tipo_movimento,
        num_documento_material,
        cod_empresa
    """


def query_mtrl_sap_cons():
    return """
    select distinct 
        t1.num_documento_material
    from db_mgd_corp_parceiro.v_consolidado_revisado t1
    inner join db_mgd_corp_parceiro.v_relatorio_ordem_servico t2
        on t1.cod_work_order = t2.cod_work_order
    where 
        t1.cod_material_sap in ('22024226', '22024259', '22024369', '22024663', '22024711', '22024759', '22024783', '22026248', '22026249', '22026251', '22056499', '22058535', '22061603', '22060422', '22063244', '22063252')
        and t1.dat_ref >= date_format(date_sub(current_date,90),'yyyyMMdd')
        and t2.dsc_tipo_work_order like '%ENTREGA DE CONTROLE REMOTO VOZ%'
    """


def query_mdl_eqpmnt():
    return """
    SELECT *
    FROM DB_MGD_EXPER_TERMINAL.V_MODELO_EQUIPAMENTO
    WHERE FL_STATUS_BI = 'A'
    """


def query_loc_eqpmnt():
    return """
    SELECT *
    FROM DB_MGD_EXPER_TERMINAL.V_LOCAL 
    WHERE ID_TIPO_LOCAL <> 6
        AND FL_STATUS_BI = 'A'
    """


def query_mtrl_campo():
    return """
    SELECT 
        M.DAT_MOVIMENTO,
        M.NUM_CONTA,
        M.COD_BASE,
        M.DW_TIPO_MATERIAL_CLASSE,
        M.COD_TIPO_MATERIAL_CAMPO,
        M.QTD_MATERIAL,
        M.COD_LOGIN,
        M.DSC_NUM_SERIAL 
    FROM DWH.BI_FP_MATERIAL_CAMPO M 
    WHERE 
        M.DAT_MOVIMENTO >= SysDate - 112
        AND M.QTD_MATERIAL < 1000
        AND M.COD_LOGIN not Like 'T%'
        AND M.COD_LOGIN not Like 'Z%'
        AND M.COD_POOL = 'install'
    """


def query_hist_eqpmnt_dtl():
    return """
    with HISTORICO_EQPMNT as 
    (
        select 
            LAG(T1.ID_LOCAL) over (partition by T1.ID_EQUIPAMENTO order by T1.DH_HISTORICO_EQUIPAMENTO) as ID_LOCAL_ANTERIOR,
            T1.ID_HISTORICO_EQUIPAMENTO 
        from PRD_BI_DW.DW_ATLP_HISTORICO_EQPMNT_NET T1 
        where 
            T1.FL_STATUS_BI = 'A' 
            and T1.DH_HISTORICO_EQUIPAMENTO < SysDate 
            and T1.DH_HISTORICO_EQUIPAMENTO > SysDate - 3 * 365
    ) 
    select 
        T1.NR_SERIE,
        T2.CD_ENDERECAVEL,
        T2.CD_OPERADORA,
        T2.CD_CONTRATO_NETSMS,
        T2.DH_HISTORICO_EQUIPAMENTO,
        t4.ID_LOCAL_ANTERIOR 
    from INN.FA_ATLP_MOV_TERM_OS T1 
    left join INN.FT_ATLP_MOV_TERM_OS T2 
        on T1.ID_HISTORICO_EQUIPAMENTO = T2.ID_HISTORICO_EQUIPAMENTO 
        and T1.ID_HISTORICO_EQUIPAMENTO > 3 
    left join HISTORICO_EQPMNT t4 
        on T1.ID_HISTORICO_EQUIPAMENTO = t4.ID_HISTORICO_EQUIPAMENTO 
    where 
        T1.PERIODO >= To_Char(Trunc(SysDate - 112, 'MM'), 'YYYYMM')
    """


#####################
# TESTE TESTE TESTE #
#####################
def query_eqpmnt_combined():
    return """
    with HISTORICO_EQPMNT as 
    (
        select 
            T1.ID_EQUIPAMENTO,
            T1.DH_HISTORICO_EQUIPAMENTO,
            T1.ID_MODELO_EQUIPAMENTO,
            T1.ID_OPERACAO,
            T1.ID_LOCAL,
            T1.ID_ESTADO_EQUIPAMENTO,
            LAG(T1.ID_LOCAL) over (partition by T1.ID_EQUIPAMENTO order by T1.DH_HISTORICO_EQUIPAMENTO) as ID_LOCAL_ANTERIOR,
            LAG(T1.ID_LOCAL, 2) over (partition by T1.ID_EQUIPAMENTO order by T1.DH_HISTORICO_EQUIPAMENTO) as ID_LOCAL_ANTERIOR_2,
            ROW_NUMBER() over (partition by T1.ID_EQUIPAMENTO order by T1.DH_HISTORICO_EQUIPAMENTO Desc, T1.ID_HISTORICO_EQUIPAMENTO Desc) as ROWNUMBER
        from PRD_BI_DW.DW_ATLP_HISTORICO_EQPMNT_NET T1
        where T1.DH_HISTORICO_EQUIPAMENTO >= (SysDate - 365 * 3)
          and T1.DH_HISTORICO_EQUIPAMENTO < SysDate
          and T1.FL_STATUS_BI = 'A'
          and T1.NR_SERIE not Like 'ANT%'
    ),
    ENDERECAVEL AS 
    (
        select 
            T3.ID_EQUIPAMENTO,
            T3.CD_ENDERECAVEL,
            T3.CD_OPERADORA,
            T3.CD_CONTRATO_NETSMS
        from PRD_BI_DW.DW_ATLP_ENDERECAVEL_NET T3
        where T3.FL_STATUS_BI = 'A'
    ),
    LOCAL_NET AS 
    (
        select 
            T5.ID_LOCAL,
            T5.CD_IBGE,
            T6.CD_OPERADORA,
            T6.NM_PRODUTO_ATUAL
        from PRD_BI_DW.DW_ATLP_LOCAL_NET T5
        inner join PRD_BI_DW.DW_ATLP_OPERACAO_NET T6 
            on T5.ID_OPERACAO = T6.ID_OPERACAO
        where T5.FL_STATUS_BI = 'A' and T6.FL_STATUS_BI = 'A'
    )
    select 
        T2.ID_ESTADO_EQUIPAMENTO,
        T2.ID_MODELO_EQUIPAMENTO,
        T2.ID_OPERACAO,
        T2.ID_LOCAL,
        Sum(1) as QTDE,
        T3.CD_ENDERECAVEL,
        T3.CD_OPERADORA,
        T3.CD_CONTRATO_NETSMS,
        T4.CD_IBGE,
        T4.NM_PRODUTO_ATUAL,
        T2.ID_LOCAL_ANTERIOR,
        T2.ID_LOCAL_ANTERIOR_2
    from HISTORICO_EQPMNT T2
    left join ENDERECAVEL T3 on T2.ID_EQUIPAMENTO = T3.ID_EQUIPAMENTO
    left join LOCAL_NET T4 on T2.ID_LOCAL = T4.ID_LOCAL
    where T2.ROWNUMBER = 1
      and T2.ID_ESTADO_EQUIPAMENTO = 2
    group by 
        T2.ID_ESTADO_EQUIPAMENTO, 
        T2.ID_MODELO_EQUIPAMENTO, 
        T2.ID_OPERACAO, 
        T2.ID_LOCAL, 
        T3.CD_ENDERECAVEL,
        T3.CD_OPERADORA,
        T3.CD_CONTRATO_NETSMS,
        T4.CD_IBGE,
        T4.NM_PRODUTO_ATUAL,
        T2.ID_LOCAL_ANTERIOR,
        T2.ID_LOCAL_ANTERIOR_2
    """
