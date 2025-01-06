import os
import pandas as pd
import numpy as np
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Definir constantes para caminhos de arquivos
# BASE_DIR = os.getenv(
#    "BASE_DIR",
#    "/mnt/shared/ANALYTICS_LOGISTICAS/00.Bases de Dados/7.SHAREPOINT/Cadastros"
# )
#
# BASE_CDSW = os.getenv(
#   "BASE_CDSW",
#   "/home/cdsw/autonomia/notebooks/"
# )

BASE_DIR = os.getenv("BASE_DIR", "00_autonomia_arquivos")
BASE_CDSW = os.getenv("BASE_CDSW", "00_autonomia_arquivos")


# Paths para os arquivos
DIM_CALENDARIZACAO_PATH = os.path.join(BASE_DIR, "CADASTRO_CALENDARIZACAO.xlsx")
DIM_CENTRO_DEPOSITO_PATH = os.path.join(BASE_DIR, "DIMENSAO_CENTRO_DEPOSITO.xlsx")
# DIM_CENTROS_MANTER_PATH = os.path.join(BASE_CDSW, "CENTROS_MANTER_v20-12.xlsx")            #Faltante
DIM_COMPATIBILIDADE_PATH = os.path.join(BASE_DIR, "CADASTRO_COMPATIBILIDADE_FAMILIA.xlsx")
# DIM_DEPOSITOS_EXCLUIR_PATH = os.path.join(BASE_CDSW, "CENTROS_MANTER_v20-12.xlsx")         #Faltante
DIM_FAMILIA_PATH = os.path.join(BASE_DIR, "DIMENSAO_FAMILIA.xlsx")
DIM_LOCAL_ATLAS_PATH = os.path.join(BASE_DIR, "DIMENSAO_LOCAL_ATLAS.xlsx")
DIM_LOCAL_SAP_PATH = os.path.join(BASE_CDSW, "DIMENSAO_LOCAL_SAP.xlsx")
DIM_MATERIAL_PATH = os.path.join(BASE_DIR, "DIMENSAO_MATERIAL.xlsx")
DIM_RESPONSAVEL_PATH = os.path.join(BASE_DIR, "DIMENSAO_RESPONSAVEL.xlsx")
# DIM_SAZONALIDADE_PATH = os.path.join(BASE_DIR, "sazonalidade_decomposta.xlsx")             #Faltante


# Função genérica para ler arquivos Excel
def load_excel(file_path, sheet_name=None, dtype=None):
    """Carrega um arquivo Excel e retorna um DataFrame.

    Args:
        file_path (str): Caminho do arquivo Excel.
        sheet_name (str, optional): Nome da aba a ser carregada. Padrão é None (primeira aba).
        dtype (dict, optional): Dicionário com os tipos de dados das colunas.

    Returns:
        pd.DataFrame: DataFrame carregado.
    """
    if not os.path.exists(file_path):
        logging.error(f"Arquivo não encontrado: {file_path}")
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    logging.info(f"Carregando arquivo: {file_path}")
    return pd.read_excel(file_path, sheet_name=sheet_name, dtype=dtype)


# Carregar DataFrames

#############################################################################
# Carga fria    = DIMENSAO_LOCAL_ATLAS.xlsx                                 #
# Contém        =                                                           #
# Objetivo      =                                                           #
# Output        = df_dim_local_atlas                                        #
#############################################################################
df_dim_local_atlas = load_excel(
    file_path=DIM_LOCAL_ATLAS_PATH,
    sheet_name="in",
    dtype={"ID_LOCAL": np.int32, "COD_LOCAL_SAP": np.str_},
)

# Padronizar colunas para minúsculas
df_dim_local_atlas.columns = df_dim_local_atlas.columns.str.lower()


#############################################################################
# Carga fria    = CADASTRO_COMPATIBILIDADE_FAMILIA.xlsx                     #
# Contém        =                                                           #
# Objetivo      =                                                           #
# Output        = df_compatibilidade                                        #
#############################################################################
df_compatibilidade = load_excel(
    file_path=DIM_COMPATIBILIDADE_PATH,
    sheet_name="in",
    dtype={
        "TIPO_LOCAL": np.str_,
        "TIPO_ATENDIMENTO": np.str_,
        "FAMILIA": np.str_,
        "MATERIAL_TERMINAL": np.str_,
        "OPCAO_DEPOSITO_ORIGEM": np.str_,
        "MONTAGEM_KIT": np.str_,
        "FAMILIA_COMPOSICAO_KIT": np.str_,
        "MATERIAL_ACESSORIO": np.str_,
        "PCT_VOLUME": np.float64,
    },
)

# Padronizar colunas para minúsculas
df_compatibilidade.columns = df_compatibilidade.columns.str.lower()


#############################################################################
# Carga fria    = DIMENSAO_MATERIAL.xlsx                                    #
# Contém        =                                                           #
# Objetivo      =                                                           #
# Output        = df_dim_material                                           #
#############################################################################
df_dim_material = load_excel(
    file_path=DIM_MATERIAL_PATH,
    sheet_name="in",
    dtype={
        "NUM_MATERIAL": np.str_,
        "NUM_MATERIAL_PAI": np.str_,
        "qtde_multiplo_envio": np.float64,
        "qtde_multiplo_consumo": np.float64,
    },
)

# Padronizar colunas para minúsculas
df_dim_material.columns = df_dim_material.columns.str.lower()


#############################################################################
# Carga fria    = DIMENSAO_LOCAL_SAP.xlsx                                   #
# Contém        =                                                           #
# Objetivo      =                                                           #
# Output        = df_dim_local_sap                                          #
#############################################################################
df_dim_local_sap = load_excel(file_path=DIM_LOCAL_SAP_PATH, sheet_name="in")

# Padronizar colunas para minúsculas
df_dim_local_sap.columns = df_dim_local_sap.columns.str.lower()

#############################################################################
# Carga fria    = DIMENSAO_FAMILIA.xlsx                                     #
# Contém        = DSC_FAMILIA e STATUS_FAMILIA                              #
# Objetivo      = Indicar ATIVO ou INATIVO de acordo com a família          #
# Output        = df_dim_familia                                            #
#############################################################################
df_dim_familia = load_excel(
    file_path=DIM_FAMILIA_PATH,
    sheet_name="in",
    dtype={"DSC_FAMILIA": np.str_, "STATUS_FAMILIA": np.str_},
)

# Padronizar colunas para minúsculas
df_dim_familia.columns = df_dim_familia.columns.str.lower()


#############################################################################
# Carga fria    = DIMENSAO_CENTRO_DEPOSITO.xlsx                             #
# Contém        =                                                           #
# Objetivo      =                                                           #
# Output        = df_dim_centro_deposito                                    #
#############################################################################
df_dim_centro_deposito = load_excel(file_path=DIM_CENTRO_DEPOSITO_PATH, sheet_name="in")

# Padronizar colunas para minúsculas
df_dim_centro_deposito.columns = df_dim_centro_deposito.columns.str.lower()


#############################################################################
# Carga fria    = DIMENSAO_RESPONSAVEL.xlsx                                 #
# Contém        =                                                           #
# Objetivo      =                                                           #
# Output        = df_dim_responsavel                                        #
#############################################################################
df_dim_responsavel = load_excel(
    file_path=DIM_RESPONSAVEL_PATH,
    sheet_name="IN",
    dtype={
        "UF": np.str_,
        "RESPONSAVEL": np.str_,
        "TIPO_MATERIAL": np.str_,
        "qtde_multiplo_envio": np.datetime64,
        "qtde_multiplo_consumo": np.datetime64,
    },
)

# Padronizar colunas para minúsculas
df_dim_responsavel.columns = df_dim_responsavel.columns.str.lower()


#############################################################################
# Carga fria    = CADASTRO_CALENDARIZACAO.xlsx                              #
# Contém        =                                                           #
# Objetivo      =                                                           #
# Output        = df_calendarizacao                                         #
#############################################################################
df_calendarizacao = load_excel(file_path=DIM_CALENDARIZACAO_PATH, sheet_name="in")

# Padronizar colunas para minúsculas
df_calendarizacao.columns = df_calendarizacao.columns.str.lower()
