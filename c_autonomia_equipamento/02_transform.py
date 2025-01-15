#####################################################################################################################
# Manipulação do output da query_sap_zt438 encontrada no 04_autonomia_modelo (código original)                      #
# Comentários do Mateus:                                                                                            #
# - Crio uma lista com todos os centros que são utilizados como origem do material                                  #
# - Uso essa lista somente para filtrar os centros que serão utilizados do estoque do CD                            #
# - Faço isso somente para reduzir o tamanho da base, e faço a mesma operação para os materiais e para os depósitos #
#####################################################################################################################


df_estoque_cd["COD_DEPOSITO"] = np.where(
    df_estoque_cd["COD_DEPOSITO"] == df_estoque_cd["COD_CENTRO"],
    "NOVO",
    df_estoque_cd["COD_DEPOSITO"],
)
df_estoque_cd["NUM_MATERIAL"] = df_estoque_cd["NUM_MATERIAL"].str.lstrip("0")

# Reduzo os registros de estoque disponivel para economizar memória
df_estoque_cd = df_estoque_cd[
    (df_estoque_cd["NUM_MATERIAL"].isin(materiais))
    & (df_estoque_cd["COD_DEPOSITO"].isin(depositos))
    & (df_estoque_cd["COD_CENTRO"].isin(centros))
    & (df_estoque_cd["QTD_ESTOQUE_DISPONIVEL"] > 0)
].reset_index(drop=True)

df_estoque_cd = (
    df_estoque_cd.groupby(["NUM_MATERIAL", "COD_CENTRO", "COD_DEPOSITO"])
    .sum("QTD_ESTOQUE_DISPONIVEL")
    .reset_index()
)
