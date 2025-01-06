import unittest
from unittest.mock import Mock
from extract_01 import df_dim_local_atlas, df_dim_familia



class Test01Extract(unittest.TestCase):

    def setUp(self):
        self.df_dim_local_atlas = df_dim_local_atlas
        self.df_dim_familia = df_dim_familia

    def test_if_columns_exist(self):

        expected_columns = {
            'cod_local_sap', 
            'cod_centro_abastecimento_2', 
            'tipo_local', 
            'cod_centro_abastecimento_1', 
            'id_local', 
            'tipo_atendimento', 
            'status_abastecimento', 
            'empresa'}
        
        columns_names = set(self.df_dim_local_atlas.columns)

        self.assertTrue(expected_columns.issubset(columns_names))

    def test_if_id_tipo_local_wihtout_null(self):

        self.assertTrue(self.df_dim_local_atlas["id_local"].notnull().all())
        self.assertTrue(self.df_dim_local_atlas["cod_local_sap"].notnull().all())

    def test_if_id_local_is_without_duplicates(self):

        self.assertTrue(self.df_dim_local_atlas["id_local"].is_unique)

    def test_if_tipo_local_valid_values(self):
        valid_status = {"AGENTE", "BASE", "EPO", "LOJA", "TECNICO"}

        dimension_set = set(df_dim_local_atlas["tipo_local"].dropna().unique())

        self.assertEqual(dimension_set, valid_status)

    def test_if_valid_centro_abastecimento(self):
        centro_pattern = r"^(0|[A-Z]{2}[0-9]{2}|N[0-9]{2}[A-Z]|N[0-9]{3})$"
        
        self.assertTrue(
            self.df_dim_local_atlas["cod_centro_abastecimento_1"]
            .astype(str)
            .str.match(centro_pattern)
            .all())
        
        self.assertTrue(
            self.df_dim_local_atlas["cod_centro_abastecimento_2"]
            .astype(str)
            .str.match(centro_pattern)
            .all())
        
    def test_dataframe_min_linhas(self):

        self.assertGreater(len(self.df_dim_local_atlas), 3000)

    def test_valid_empresa_values(self):
        valid_status = {"CLARO TV", "NET"}

        self.assertTrue(valid_status.issubset(set(self.df_dim_local_atlas["empresa"].dropna().unique())))

    def test_valid_status_abastecimento_values(self):
        valid_status = {"INATIVO", "ATIVO"}

        self.assertTrue(valid_status.issubset(set(self.df_dim_local_atlas["status_abastecimento"].dropna().unique())))


#########################
# df_dim_familia        #
# testes automatizados  #
#########################


    def test_if_columns_exist(self):
        expected_columns = {"dsc_familia", "status_familia"}

        self.assertTrue(expected_columns.issubset(self.df_dim_familia.columns))

    def test_status_familia_sem_nulos(self):

        self.assertTrue (self.df_dim_familia["status_familia"].notnull().all())

    def test_if_dsc_familia_is_without_duplicates(self):

        self.assertTrue(self.df_dim_familia["dsc_familia"].is_unique)

    def test_valid_status_familia_values(self):
        valid_status = {"ATIVO", "INATIVO"}

        self.assertTrue(set(df_dim_familia["status_familia"].dropna().unique()).issubset(valid_status))

    def test_if_one_is_active(self):

        self.assertTrue((self.df_dim_familia["status_familia"] == "ATIVO"
        ).any())

    def test_if_dsc_familia_is_without_null(self):

        self.assertTrue(self.df_dim_familia["dsc_familia"].notnull().all())

    def test_dataframe_min_linhas(self):

        self.assertGreater(len(df_dim_familia), 90)



if __name__=="__main__":
    unittest.main(verbosity=2)
