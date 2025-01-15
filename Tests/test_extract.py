import os
import sys
import numpy as np
import pandas as pd
import openpyxl

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
# sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../../ETL")))

from ETL.Extract import Extract
from unittest.mock import MagicMock


print(sys.path)

def test_execute_query(mocker):
    # Mockar dependências
    mock_oracle_conn = mocker.MagicMock()
    mock_logger = mocker.MagicMock()
    
    # Criar um DataFrame fictício
    mock_df = pd.DataFrame({'col1': [1, 2], 'col2': ['A', 'B']})
    mock_oracle_conn.run_query_to_dataframe.return_value = mock_df
    
    # Instanciar a classe
    extract = Extract(
        oracle_conn=mock_oracle_conn,
        logger=mock_logger,
        query="SELECT * FROM test_table"
    )
    
    # Testar o método
    result = extract._execute_query(step="TestStep")
    
    # Asserções
    mock_logger.info.assert_called()  # Verificar se o log foi chamado
    mock_oracle_conn.run_query_to_dataframe.assert_called_with("SELECT * FROM test_table")
    assert result.equals(mock_df)  # Verificar se o resultado é o esperado
    
def test_convert_dataframe_types(mocker):
    mock_logger = mocker.MagicMock()

    # Criar um DataFrame fictício com tipos errados
    input_df = pd.DataFrame({
        'col1': ['1', '2', '3'],
        'col2': ['2023-01-01', '2023-02-01', 'invalid_date'],
    })
    
    expected_df = pd.DataFrame({
        'col1': [1.0, 2.0, 3.0],
        'col2': pd.to_datetime(['2023-01-01', '2023-02-01', 'NaT']),
    })

    # Mockar o esquema de tipos
    mock_dtypes_dict = {'col1': 'float64', 'col2': 'datetime64[ns]'}
    
    # Instanciar a classe
    extract = Extract(
        oracle_conn=None,  # Não necessário para este teste
        logger=mock_logger,
        dtypes_dict=mock_dtypes_dict
    )
    
    # Testar o método
    result = extract._convert_dataframe_types(input_df, step="TestStep")
    
    # Asserções
    pd.testing.assert_frame_equal(result, expected_df)
    mock_logger.info.assert_called_with("DataFrame conversion complete.", "TestStep")

def test_extract_familia_logis(mocker):
    mock_logger = mocker.MagicMock()

    # Mockar pd.read_excel
    mocker.patch('pandas.read_excel', return_value=pd.DataFrame({'FAMILIA': ['A', 'B']}))

    # Instanciar a classe
    extract = Extract(
        oracle_conn=None,
        logger=mock_logger
    )
    
    # Testar o método
    result = extract.extract_familia_logis()

    # Verificar renomeação
    expected_df = pd.DataFrame({'FAMILIA_AJUST': ['A', 'B']})
    pd.testing.assert_frame_equal(result, expected_df)
    mock_logger.info.assert_called_with("depara_familia_logistica_autonomia extraction complete", "DEPARA_FAMILIA_LOGISTICA_AUTONOMIA")
