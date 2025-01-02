centros1 = df_dim_local_atlas["COD_CENTRO_ABASTECIMENTO_1"].unique().tolist()
centros2 = df_dim_local_atlas["COD_CENTRO_ABASTECIMENTO_2"].unique().tolist()
centros = list(set(centros1 + centros2))

materiais1 = df_compatibilidade["MATERIAL_ACESSORIO"].unique().tolist()
materiais2 = df_compatibilidade["MATERIAL_TERMINAL"].unique().tolist()
materiais3 = df_dim_material["NUM_MATERIAL"].unique().tolist()
materiais = list(set(materiais1 + materiais2 + materiais3))

depositos1 = df_compatibilidade["OPCAO_DEPOSITO_ORIGEM"].apply(lambda x: x.split("|"))
depositos1 = depositos1.explode().unique().tolist()

depositos_considerar_a_mais = ["USAD", "UCTV", "UDEI", "NOVO"]

depositos = list(set(depositos1 + depositos_considerar_a_mais))
