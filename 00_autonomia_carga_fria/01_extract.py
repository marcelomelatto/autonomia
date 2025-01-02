import os
import pandas as pd
import numpy as np
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Definir constantes para caminhos de arquivos
BASE_PATH = r"\\cllgpdw8551.corp.clarobr\ANALYTICS_LOGISTICAS\00.Bases de Dados\7.SHAREPOINT\Cadastros"
FILE_DIM_LOCAL = os.path.join(BASE_PATH, "DIMENSAO_LOCAL_ATLAS.xlsx")
FILE_COMPATIBILIDADE = os.path.join(BASE_PATH, "CADASTRO_COMPATIBILIDADE_FAMILIA.xlsx")
FILE_DIM_MATERIAL = os.path.join(BASE_PATH, "DIMENSAO_MATERIAL.xlsx")

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

########################
# dimensao_local_atlas #
########################
df_dim_local_atlas = load_excel(
    file_path=FILE_DIM_LOCAL,
    sheet_name="in",
    dtype={
        "ID_LOCAL": np.int32,
        "COD_LOCAL_SAP": np.str_
    }
)

# Padronizar colunas para minúsculas
df_dim_local_atlas.columns = df_dim_local_atlas.columns.str.lower()

####################################
# cadastro_compatibilidade_familia #
####################################
df_compatibilidade = load_excel(
    file_path=FILE_COMPATIBILIDADE,
    dtype={
        "TIPO_LOCAL": np.str_,
        "TIPO_ATENDIMENTO": np.str_,
        "FAMILIA": np.str_,
        "MATERIAL_TERMINAL": np.str_,
        "OPCAO_DEPOSITO_ORIGEM": np.str_,
        "MONTAGEM_KIT": np.str_,
        "FAMILIA_COMPOSICAO_KIT": np.str_,
        "MATERIAL_ACESSORIO": np.str_,
        "PCT_VOLUME": np.float64
    }
)

# Padronizar colunas para minúsculas
df_compatibilidade.columns = df_compatibilidade.columns.str.lower()

#####################
# dimensao_material #
#####################
df_dim_material = load_excel(
    file_path=FILE_DIM_MATERIAL,
    sheet_name="in",
    dtype={
        "NUM_MATERIAL": np.str_,
        "NUM_MATERIAL_PAI": np.str_,
        "qtde_multiplo_envio": np.float64,
        "qtde_multiplo_consumo": np.float64
    }
)

# Padronizar colunas para minúsculas
df_dim_material.columns = df_dim_material.columns.str.lower()