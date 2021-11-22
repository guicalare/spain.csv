from pandas import read_fwf
from geopandas import read_file
import matplotlib.pyplot as plt

colspecs = [(0, 10), (42, 47)]
header = ['seccion_censal', 'cod_pos']
converters={'seccion_censal' : str, 'cod_pos' : str}

datos = read_fwf("data/TRAMOS_NAL_F210630",
    colspecs=colspecs,
    names=header,
    converters=converters,
    encoding = 'iso-8859-1'
)

datos.drop_duplicates(inplace=True)
datos.reset_index(inplace=True, drop=True)

datos["cod_ine"] = list(map(lambda x: x[:5], datos["seccion_censal"]))

datos_reducidos = datos[["cod_ine", "cod_pos"]].copy(deep=True)
datos_reducidos.drop_duplicates(inplace=True)
datos_reducidos.reset_index(inplace=True, drop=True)

secciones = read_file("shp/Secciones/SECC_CE_20210101.shp")

secciones.rename(columns = {'CUSEC':'seccion_censal'}, inplace = True)

codigos_postales = secciones.merge(datos, how='left', on='seccion_censal')

fig, ax = plt.subplots(figsize = (20,16))

codigos_postales.geometry.boundary.plot(color="blue",edgecolor='k',linewidth = 1,ax=ax)

plt.savefig("img/limites.png")

codigos_postales.to_file("shp/codigos postales/codigos_postales.shp")
datos.to_csv("data/codigos_postales.csv", sep=";", index=False)
datos_reducidos.to_csv("data/codigos_postales_simplificados.csv", sep=";", index=False)
