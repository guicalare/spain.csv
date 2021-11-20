from geopandas import read_file
from pandas import merge, read_csv, concat

municipios1 = read_file("/home/guillermo/SHP/SIGLIM_Publico_INSPIRE/SHP_ETRS89/recintos_municipales_inspire_peninbal_etrs89/recintos_municipales_inspire_peninbal_etrs89.shp")
municipios2 = read_file("/home/guillermo/SHP/SIGLIM_Publico_INSPIRE/SHP_WGS84/recintos_municipales_inspire_canarias_wgs84/recintos_municipales_inspire_canarias_wgs84.shp")

municipios = concat([municipios1, municipios2], ignore_index=True)

municipios = municipios[["NAMEUNIT", "NATCODE", "geometry"]]
municipios["cod_ine"] = list(map(lambda x: x[-5:], municipios.NATCODE))
municipios["provincia"] = list(map(lambda x: int(x[:2]), municipios.cod_ine))
municipios = municipios[municipios["provincia"] <= 52]
municipios.reset_index(inplace=True)

del(municipios["NATCODE"])
del(municipios["index"])

municipios.to_file("shp/municipios final/municipios_espanna.shp")
municipios[["NAMEUNIT", "cod_ine"]].to_csv("data/municipios.csv")

