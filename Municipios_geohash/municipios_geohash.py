from geopandas import read_file
from pandas import merge, read_csv, concat
from numpy import array_split
import multiprocessing
from datetime import datetime
from os import listdir
from polygeohasher import polygeohasher

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

def shp2geohash(data, mingeohash, maxgeohash, output_dir, id_process):
    data.reset_index(inplace=True)
    del(data["index"])
    for i in range(data.shape[0]):
        archivos = listdir(output_dir)
        data_slice = data[i:i+1]
        try:
            if data_slice.shape[0] >= 1:
                id = data_slice["cod_ine"][i]
                if f"{id}.csv" not in archivos:
                    print(f"{id_process} {i} {id}")
                    primary_df = polygeohasher.create_geohash_list(data_slice, maxgeohash, inner=False)
                    secondary_df = polygeohasher.geohash_optimizer(primary_df, mingeohash, maxgeohash, maxgeohash)
                    secondary_df.to_csv(f"{output_dir}{id}.csv", sep="#")
                else:
                    print(f"EXISTE {i} -- {id}.csv")
        except Exception as e:
            print(e)

def shp2geohash_multiprocessing(num_process, data, mingeohash, maxgeohash, output_dir):
    splits = array_split(data, num_process)
    threads = []
    for index in range(num_process):
        x = multiprocessing.Process(target=shp2geohash, args=(splits[index], mingeohash, maxgeohash, output_dir, index, ))
        threads.append(x)
        x.start()
    start = datetime.now()
    for index, thread in enumerate(threads):
        thread.join()
    end = datetime.now()
    print("Tiempo de ejecucion: ", end-start)

shp2geohash_multiprocessing(10, municipios, 3, 8, "/home/guillermo/Descargas/shp/prueba/")
