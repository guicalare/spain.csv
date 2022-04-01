from geopandas import read_file
from pandas import merge, read_csv, concat
from polygeohasher import polygeohasher
from os import listdir

municipios1 = read_file("/home/guillermo/Descargas/shp/recintos_municipales_inspire_peninbal_etrs89/recintos_municipales_inspire_peninbal_etrs89.shp")
municipios2 = read_file("/home/guillermo/Descargas/shp/recintos_municipales_inspire_canarias_wgs84/recintos_municipales_inspire_canarias_wgs84.shp")

municipios = concat([municipios1, municipios2], ignore_index=True)

municipios = municipios[["NAMEUNIT", "NATCODE", "geometry"]]
municipios["cod_ine"] = list(map(lambda x: x[-5:], municipios.NATCODE))
municipios["provincia"] = list(map(lambda x: int(x[:2]), municipios.cod_ine))
municipios = municipios[municipios["provincia"] <= 52]
municipios.reset_index(inplace=True)

del(municipios["NATCODE"])
del(municipios["index"])

del(municipios1)
del(municipios2)

for i in range(8131, -1, -1):
    archivos = listdir("/home/guillermo/Descargas/shp/geohash_shp")
    data_slice = municipios[i-1:i]
    try:
        if data_slice.shape[0] >= 1:
            id = data_slice["cod_ine"][i-1]
            if f"{id}.csv" not in archivos:
                print(f"{i} {id}")
                primary_df = polygeohasher.create_geohash_list(data_slice, 8, inner=False)
                secondary_df = polygeohasher.geohash_optimizer(primary_df, 3, 8, 8)
                secondary_df.to_csv(f"/home/guillermo/Descargas/shp/geohash_shp/{id}.csv", sep="#")
            else:
                print(f"EXISTE {i} -- {id}.csv")
    except Exception as e:
        print(e)



f = pd.concat(map(pd.read_csv, glob.glob(os.path.join('/home/guillermo/Descargas/shp/geohash_shp', "*.csv"))))