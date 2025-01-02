import pandas as pd
import pytest

#########################
# df_dim_familia        #
# testes automatizados  #
#########################

# df_dim_familia
# 1. Testar se a base contém as colunas necessárias
def test_colunas_existentes(df_dim_familia):
    expected_columns = {"dsc_familia", "status_familia"}
    assert expected_columns.issubset(df_dim_familia.columns), "Colunas faltando na base!"

# df_dim_familia
# 2. Testar se não há valores nulos em "status_familia"
def test_status_familia_sem_nulos(df_dim_familia):
    assert df_dim_familia["status_familia"].notnull().all(), "Coluna 'status_familia' contém valores nulos!"

# df_dim_familia
# 3. Testar se não há valores duplicados na coluna "dsc_familia"
def test_dsc_familia_sem_duplicatas(df_dim_familia):
    assert df_dim_familia["dsc_familia"].is_unique, "Coluna 'dsc_familia' contém valores duplicados!"

# df_dim_familia
# 4. Testar se todos os valores de "status_familia" são "ativo" ou "inativo"
def test_status_familia_valores_validos(df_dim_familia):
    valid_status = {"ATIVO", "INATIVO"}
    assert set(df_dim_familia["status_familia"].dropna().unique()).issubset(valid_status), \
        "Coluna 'status_familia' contém valores inválidos!"

# df_dim_familia
# 5. Testar se há pelo menos uma linha com "status_familia" como "ativo"
def test_pelo_menos_um_ativo(df_dim_familia):
    assert (df_dim_familia["status_familia"] == "ATIVO").any(), \
        "Nenhuma família está com o status 'ativo'!"

# df_dim_familia
# 6. Testar se não há valores nulos em "dsc_familia"
def test_dsc_familia_sem_nulos(df_dim_familia):
    assert df_dim_familia["dsc_familia"].notnull().all(), "Coluna 'dsc_familia' contém valores nulos!"

# df_dim_familia
# 7. Testar se o dataframe tem ao menos uma linha
def test_dataframe_nao_vazio(df_dim_familia):
    assert not df_dim_familia.empty, "O DataFrame está vazio!"
