import pandas as pd
import pytest


#########################
# df_dim_local_atlas    #
# testes automatizados  #
#########################


# df_dim_local_atlas
# t001. Testar se a base contém as colunas necessárias
def test_colunas_existentes(df_dim_local_atlas):
    expected_columns = {
        "cod_local",
        "dsc_local",
        "cod_centro_abastecimento_1",
        "cod_centro_abastecimento_2",
        "tipo_local",
        "empresa",
    }
    assert expected_columns.issubset(
        df_dim_local_atlas.columns
    ), "t001 = [df_dim_local_atlas] = colunas faltando na base"


# df_dim_local_atlas
# t002. Testar se não há valores nulos em "id_local" e "cod_local_sap"
def test_id_tipo_local_sem_nulos(df_dim_local_atlas):
    assert (
        df_dim_local_atlas["id_local"].notnull().all()
    ), "t002 = [df_dim_local_atlas] = coluna 'id_local' contém valores nulos"
    assert (
        df_dim_local_atlas["cod_local_sap"].notnull().all()
    ), "t002 = [df_dim_local_atlas] = coluna 'cod_local_sap' contém valores nulos"


# df_dim_local_atlas
# t003. Testar se não há valores duplicados na coluna 'id_local'
def test_id_local_sem_duplicatas(df_dim_local_atlas):
    assert df_dim_local_atlas[
        "id_local"
    ].is_unique, (
        "t003 = [df_dim_local_atlas] = coluna 'id_local' contém valores duplicados"
    )


# df_dim_local_atlas
# t004. Testar se todos os valores de 'tipo_local' são válidos
def test_tipo_local_valores_validos(df_dim_local_atlas):
    valid_status = {"AGENTE", "BASE", "EPO", "LOJA", "TECNICO"}
    assert set(df_dim_local_atlas["tipo_local"].dropna().unique()).issubset(
        valid_status
    ), "t004 = [df_dim_local_atlas] = coluna 'tipo_local' contém valores inválidos"


# df_dim_local_atlas
# t005. Testar se não há valores inválidos nos centros de abastecimento
def test_centros_abastecimento_validos(df_dim_local_atlas):
    # Padrões identificados:
    # 1. "0" → Apenas o número zero como string.
    # 2. "21YC" → Dois caracteres alfabéticos seguidos por dois dígitos numéricos.
    # 3. "N190", "N191", ..., "N990" → Letra 'N' seguida de três dígitos numéricos.
    # 4. "N67A" → Letra 'N', dois dígitos e uma letra.
    centro_pattern = r"^(0|[A-Z]{2}[0-9]{2}|N[0-9]{2}[A-Z]|N[0-9]{3})$"
    assert (
        df_dim_local_atlas["cod_centro_abastecimento_1"]
        .astype(str)
        .str.match(centro_pattern)
        .all()
    ), "t005 = [df_dim_local_atlas] = 'cod_centro_abastecimento_1' contém valores inválidos"
    assert (
        df_dim_local_atlas["cod_centro_abastecimento_2"]
        .astype(str)
        .str.match(centro_pattern)
        .all()
    ), "t005 = [df_dim_local_atlas] = 'cod_centro_abastecimento_2' contém valores inválidos"


# df_dim_local_atlas
# t006. Testar se o dataframe tem ao menos 30.000 linhas
def test_dataframe_min_linhas(df_dim_local_atlas):
    assert (
        len(df_dim_local_atlas) >= 30000
    ), "t006 = [df_dim_local_atlas] = dataframe com menos de 30.000 linhas"


# df_dim_local_atlas
# t007. Testar se todos os valores de 'empresa' são válidos
def test_empresa_valores_validos(df_dim_local_atlas):
    valid_status = {"CLARO TV", "NET"}
    assert set(df_dim_local_atlas["empresa"].dropna().unique()).issubset(
        valid_status
    ), "t007 = [df_dim_local_atlas] = coluna 'empresa' contém valores inválidos"


# df_dim_local_atlas
# t008. Testar se todos os valores de "status_abastecimento" são válidos
def test_status_abastecimento_valores_validos(df_dim_local_atlas):
    valid_status = {"INATIVO", "ATIVO"}
    assert set(df_dim_local_atlas["status_abastecimento"].dropna().unique()).issubset(
        valid_status
    ), "t008 = [df_dim_local_atlas] = coluna 'status_abastecimento' contém valores inválidos"


#########################
# df_dim_familia        #
# testes automatizados  #
#########################


# df_dim_familia
# t001. Testar se a base contém as colunas necessárias
def test_colunas_existentes(df_dim_familia):
    expected_columns = {"dsc_familia", "status_familia"}
    assert expected_columns.issubset(
        df_dim_familia.columns
    ), "t001 = [df_dim_familia] = colunas faltando na base"


# df_dim_familia
# t002. Testar se não há valores nulos em "status_familia"
def test_status_familia_sem_nulos(df_dim_familia):
    assert (
        df_dim_familia["status_familia"].notnull().all()
    ), "t002 = [df_dim_familia] = coluna 'status_familia' contem valores nulos"


# df_dim_familia
# t003. Testar se não há valores duplicados na coluna "dsc_familia"
def test_dsc_familia_sem_duplicatas(df_dim_familia):
    assert df_dim_familia[
        "dsc_familia"
    ].is_unique, (
        "t003 = [df_dim_familia] = coluna 'dsc_familia' contem valores duplicados"
    )


# df_dim_familia
# t004. Testar se todos os valores de "status_familia" são "ativo" ou "inativo"
def test_status_familia_valores_validos(df_dim_familia):
    valid_status = {"ATIVO", "INATIVO"}
    assert set(df_dim_familia["status_familia"].dropna().unique()).issubset(
        valid_status
    ), "t004 = [df_dim_familia] = coluna 'status_familia' contem valores invalidos"


# df_dim_familia
# t005. Testar se há pelo menos uma linha com "status_familia" como "ativo"
def test_pelo_menos_um_ativo(df_dim_familia):
    assert (
        df_dim_familia["status_familia"] == "ATIVO"
    ).any(), "t005 = [df_dim_familia] = nenhuma familia com  status 'ativo'"


# df_dim_familia
# t006. Testar se não há valores nulos em "dsc_familia"
def test_dsc_familia_sem_nulos(df_dim_familia):
    assert (
        df_dim_familia["dsc_familia"].notnull().all()
    ), "t006 = [df_dim_familia] = coluna 'dsc_familia' contem valores nulos"


# df_dim_familia
# t007. Testar se o dataframe tem ao menos 90 linhas
def test_dataframe_min_linhas(df_dim_familia):
    assert (
        len(df_dim_familia) >= 90
    ), "t007 = [df_dim_familia] = dataframe com menos de 90 linhas_"
