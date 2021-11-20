from geopandas import read_file
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

# Límites municipales, provinciales y autonómicos 2021 CC-BY 4.0 https://www.ign.es
municipios = read_file("shp/municipios/municipios_espanna.shp")
# Fuente: © Ministerio de Agricultura, Pesca y Alimentación (Comarcas Agrarias)
comarcas = read_file("shp/comarcas/ComarcasAgrarias.shp")

fig, ax = plt.subplots(figsize = (20,16))

municipios.geometry.boundary.plot(color="blue",edgecolor='k',linewidth = 1,ax=ax)
comarcas.geometry.boundary.plot(color="red",edgecolor='k',linewidth = 2,ax=ax)

plt.savefig("img/limites.png")

municipios["area_comun"] = 0
municipios["CO_COMARCA"] = "-9999"
municipios["DS_COMARCA"] = "--NAN--"

mun_list, com_list, area_com = [], [], []

for idx_mun, row_mun in municipios.iterrows():
    municipio_area = row_mun["geometry"].area
    comarcas_querry = comarcas[comarcas["CO_PROVINC"] == int(row_mun["cod_ine"][:2])]
    for idx_com, row_com in comarcas_querry.iterrows():
        area_comun = row_mun["geometry"].intersection(row_com["geometry"]).area/municipio_area
        if area_comun >= 0.55:
            municipios["area_comun"].loc[idx_mun] = area_comun
            municipios["CO_COMARCA"].loc[idx_mun] = row_com["CO_COMARCA"]
            municipios["DS_COMARCA"].loc[idx_mun] = row_com["DS_COMARCA"]
            mun_list.append(row_mun["cod_ine"])
            com_list.append(row_com["CO_COMARCA"])
            area_com.append(area_comun)
            break

municipios.to_file("shp/municipios relacionados/municipios_comarcas.shp")
municipios[["cod_ine", 'CO_COMARCA', 'DS_COMARCA']].to_csv("data/relacion_municipios_comarcas.csv", index=False, sep=";")

municipios_solitarios = list(set(list(municipios["cod_ine"])) - set(mun_list

print(f"Municipios que no han sido asignados a una comarca: {municipios_solitarios}")

fig, ax = plt.subplots(figsize = (20,16))

municipios.plot(column='area_comun', legend=True, ax=ax, edgecolor='k', linewidth = 1)
comarcas.geometry.boundary.plot(color="red",edgecolor='k',linewidth = 2,ax=ax)

plt.savefig("img/areas.png")
