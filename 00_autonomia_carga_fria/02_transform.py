# TRANSFORMAR 001 = df_dim_local_atlas

# CÓDIGO DO MATEUS
df_dim_local_atlas["COD_LOCAL_SAP"] = df_dim_local_atlas["COD_LOCAL_SAP"].str.lstrip(
    "0"
)

centros1 = df_dim_local_atlas["COD_CENTRO_ABASTECIMENTO_1"].unique().tolist()
centros2 = df_dim_local_atlas["COD_CENTRO_ABASTECIMENTO_2"].unique().tolist()
centros = list(set(centros1 + centros2))

# TRANSFORMAR 002 = TIRAR DUPLICIDADE DF_DIM_FAMILIA POR DSC_FAMILIA

# CÓDIGO DO MATEUS:
# Depara de status das familias, indica se a familia é considerada como ATIVA ou INATIVA,
# Caso a familia não esteja cadastrada no depara, considero por default o status ATIVO
df_pontos_4 = df_pontos_4.merge(
    df_dim_familia.drop_duplicates(["DSC_FAMILIA"]), on="DSC_FAMILIA", how="left"
)[df_pontos_4.columns.tolist() + ["STATUS_FAMILIA"]]


# CÓDIGO DO MATEUS:
materiais1 = df_compatibilidade["MATERIAL_ACESSORIO"].unique().tolist()
materiais2 = df_compatibilidade["MATERIAL_TERMINAL"].unique().tolist()
materiais3 = df_dim_material["NUM_MATERIAL"].unique().tolist()
materiais = list(set(materiais1 + materiais2 + materiais3))

# CÓDIGO DO MATEUS:
depositos1 = df_compatibilidade["OPCAO_DEPOSITO_ORIGEM"].apply(lambda x: x.split("|"))
depositos1 = depositos1.explode().unique().tolist()

# CÓDIGO DO MATEUS:
depositos_considerar_a_mais = ["USAD", "UCTV", "UDEI", "NOVO"]

# CÓDIGO DO MATEUS:
depositos = list(set(depositos1 + depositos_considerar_a_mais))
