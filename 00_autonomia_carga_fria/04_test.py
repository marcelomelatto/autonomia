import pandas as pd
import pytest

#########################
# df_dim_familia        #
# testes automatizados  #
#########################

# df_dim_familia
# t001. Testar se a base contém as colunas necessárias
def test_colunas_existentes(df_dim_familia):
    expected_columns = {"dsc_familia", "status_familia"}
    assert expected_columns.issubset(df_dim_familia.columns), "t001 = [df_dim_familia] = colunas faltando na base"

# df_dim_familia
# t002. Testar se não há valores nulos em "status_familia"
def test_status_familia_sem_nulos(df_dim_familia):
    assert df_dim_familia["status_familia"].notnull().all(), "t002 = [df_dim_familia] = coluna 'status_familia' contem valores nulos"

# df_dim_familia
# t003. Testar se não há valores duplicados na coluna "dsc_familia"
def test_dsc_familia_sem_duplicatas(df_dim_familia):
    assert df_dim_familia["dsc_familia"].is_unique, "t003 = [df_dim_familia] = coluna 'dsc_familia' contem valores duplicados"

# df_dim_familia
# t004. Testar se todos os valores de "status_familia" são "ativo" ou "inativo"
def test_status_familia_valores_validos(df_dim_familia):
    valid_status = {"ATIVO", "INATIVO"}
    assert set(df_dim_familia["status_familia"].dropna().unique()).issubset(valid_status), \
        "t004 = [df_dim_familia] = coluna 'status_familia' contem valores invalidos"

# df_dim_familia
# t005. Testar se há pelo menos uma linha com "status_familia" como "ativo"
def test_pelo_menos_um_ativo(df_dim_familia):
    assert (df_dim_familia["status_familia"] == "ATIVO").any(), \
        "t005 = [df_dim_familia] = nenhuma familia com  status 'ativo'"

# df_dim_familia
# t006. Testar se não há valores nulos em "dsc_familia"
def test_dsc_familia_sem_nulos(df_dim_familia):
    assert df_dim_familia["dsc_familia"].notnull().all(), "t006 = [df_dim_familia] = coluna 'dsc_familia' contem valores nulos"

# df_dim_familia
# t007. Testar se o dataframe tem ao menos 99 linhas
def test_dataframe_min_linhas(df_dim_familia):
    assert len(df_dim_familia) >= 99, "t007 = [df_dim_familia] = dataframe com menos de 99 linhas"
