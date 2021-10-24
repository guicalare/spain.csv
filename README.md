# spain.csv

Spain.csv is a repository of all usefull data that I have been able to gather and save it in a friendly csv format.

## Residential streets

![](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.fastly.com%2Fcimages%2F6pk8mg3yh2ee%2F1sCSmqPwnee48yomOMS66k%2Fc8f2760ef964c72bac1cfc0d0eb71a25%2Fopenstreetmap-2.png%3Fauto%3Dwebp%26width%3D300%26height%3D155%26fit%3Dbounds&f=1&nofb=1)

Data file: https://www.kaggle.com/mordulv/spanish-streets

**How it was done**

1. Download shp zip files and unzip:

- https://download.geofabrik.de/europe/spain-latest-free.shp.zip
- https://download.geofabrik.de/africa/canary-islands-latest-free.shp.zip

Using linux command line:

```
wget https://download.geofabrik.de/europe/spain-latest-free.shp.zip & wget https://download.geofabrik.de/africa/canary-islands-latest-free.shp.zip
unzip canary-islands-latest-free.shp.zip -d ./canarias & unzip spain-latest-free.shp.zip -d ./peninsula
```
2. Get the streets data and save it in a csv

```python
from geopandas import read_file
from pandas import concat

canarias = read_file("./canarias/gis_osm_roads_free_1.shp")
peninsula = read_file("./peninsula/gis_osm_roads_free_1.shp")

residential_streets = concat([canarias[(canarias.code >= 5121) & (canarias.code <= 5124)], peninsula[(peninsula.code >= 5121) & (peninsula.code <= 5124)]])
residential_streets = residential_streets[residential_streets.name.notnull()]
residential_streets["x"] = list(map(lambda x: x.centroid.x, residential_streets["geometry"]))
residential_streets["y"] = list(map(lambda x: x.centroid.y, residential_streets["geometry"]))
residential_streets["way_id"] = list(map(lambda x: "W"+str(x), residential_streets["osm_id"]))
residential_streets = residential_streets[["osm_id", "way_id","name", "x", "y"]]

residential_streets.to_csv("streets.csv", index=False, sep=";")
```

3. Add extra data to the streets

Now we need to get some extra data from the osm_id with reverse geocoding. To do this, we can use:

- **Oficial openstreetmaps Nominatim request API**: https://nominatim.org/release-docs/develop/api/Lookup/

```python
from numpy import arange
from requests import get
from pandas import read_csv, concat, DataFrame
from tqdm import tqdm
from time import sleep

datos = read_csv("streets.csv", sep=";")
url = "https://nominatim.openstreetmap.org/lookup?osm_ids=#&format=json"

valor_inicio = arange(0,datos.shape[0],50)
valor_final = arange(50,datos.shape[0],50)
iterar = list(zip(valor_inicio, valor_final))
iterar.append((valor_final[-1], valor_final[-1] + datos.shape[0]%50))
final_data = DataFrame()

for i in tqdm(iterar):
    response = get(url.replace("#", ",".join(datos.way_id[i[0]:i[1]]))).json()
    get_values = lambda x: x["address"]
    values = DataFrame.from_dict(list(map(get_values, response)))
    final_data = concat([final_data, values]).reset_index(drop=True)
    sleep(1)

```

Then you just need to merge both DataFrames (datos and final_data) by the way_id (way_id = "W" + osm_id)

- **Self-host the Nominatim request API**: https://github.com/mediagis/nominatim-docker/tree/master/3.7

In case you are using the **Self-hosted** option, you need to [install docker](https://docs.docker.com/engine/install/) and [osmium](https://osmcode.org/osmium-tool/manual.html)

- Osmium command line install (Ubuntu/Debian)

```
sudo apt install osmium-tool
```
Next, we need to build the Nominatim database:

```
wget https://download.geofabrik.de/europe/spain-latest.osm.pbf & wget https://download.geofabrik.de/africa/canary-islands-latest.osm.pbf
osmium merge spain-latest.osm.pbf canary-islands-latest.osm.pbf -o spain.osm.pbf
```

Then open a new terminal, copy the directory path where the spain.osm.pbf was created and pasted into <YOUR_DIRECTORY> from the next command. Then run it and wait until the docker istance is done (take a cup of coffee, because this instance build can take while, 30 mins to 1 h depending of your computer):

```
sudo docker run -it --rm \
  -e PBF_PATH=/nominatim/data/spain.osm.pbf \
  -e REPLICATION_URL=https://download.geofabrik.de/ \
  -p 8080:8080 \
  -v <YOUR_DIRECTORY>:/nominatim/data \
  --name nominatim \
  mediagis/nominatim:3.7
```

Then use the next code:

```python
from numpy import arange
from requests import get
from pandas import read_csv, concat, DataFrame
from tqdm import tqdm

datos = read_csv("streets.csv", sep=";")
url = "http://localhost:8080/lookup?osm_ids=#&format=json"

valor_inicio = arange(0,datos.shape[0],50)
valor_final = arange(50,datos.shape[0],50)
iterar = list(zip(valor_inicio, valor_final))
iterar.append((valor_final[-1], valor_final[-1] + datos.shape[0]%50))
final_data = DataFrame()

for i in tqdm(iterar):
    response = get(url.replace("#", ",".join(datos.way_id[i[0]:i[1]]))).json()
    get_values = lambda x: x["address"]
    values = DataFrame.from_dict(list(map(get_values, response)))
    final_data = concat([final_data, values]).reset_index(drop=True)
```

Then you just need to merge both DataFrames (datos and final_data) by the way_id (way_id = "W" + osm_id)

4. Add elevation to the streets

<img src="https://www.open-elevation.com/images/logo.svg" alt="drawing" width="80"/>

To add the elevation to each street you will need to use [open elevation](https://www.open-elevation.com/) using the public API or the self-hosted option. I recomend using the self-host option becausa as the [author said](https://stackoverflow.com/a/68697220) the server is not as powerfull as other services (by the way, you can support the author with [donations](https://www.open-elevation.com/#donate))

Follow the [instructions](https://github.com/Jorl17/open-elevation/blob/master/docs/host-your-own.md) for deploying the self-host solution and then use the following code:

```python
from pandas import read_csv, DataFrame, concat
from requests import get
from numpy import arange
from tqdm import tqdm

data = read_csv("streets.csv", sep=";")

s = lambda x, y: str(x) + "," + str(y)

data["f"] = list(map(s, data["y"], data["x"]))

valor_inicio = arange(0,data.shape[0],100)
valor_final = arange(100,data.shape[0],100)
iterar = list(zip(valor_inicio, valor_final))
iterar.append((valor_final[-1], valor_final[-1] + data.shape[0]%100))

url = "http://localhost/api/v1/lookup?locations=#"

final_data = DataFrame()

for i in tqdm(iterar):

    response = get(url.replace("#","|".join(data.f[i[0]:i[1]]))).json()
    values = DataFrame.from_dict(response["results"])
    final_data = concat([final_data, values]).reset_index(drop=True)
    
df = concat([data, final_data[["elevation"]]], axis=1)
df.to_csv("elevation_streets.csv", index=False, sep=";")
```
# Municipalities data

You can download some municipalities data from [INE](ine.es) by running the next code:

## Postal codes

```python
from pandas import read_table

cod_municipios = read_table("https://raw.githubusercontent.com/inigoflores/ds-codigos-postales-ine-es/master/data/codigos_postales_municipios.csv", sep=",", dtype=str)
cod_municipios.to_csv("codigos_municipios.csv", sep=";", index=False)
```

## Population of municipalities [DATA](https://www.ine.es/jaxiT3/Tabla.htm?t=33571)

```python
from pandas import read_table

def ine_num_str2int(valor):
    try:
        if valor[-2:] == ".0":
            return int(valor[:-2].replace(".",""))
        else:
            return int(valor.replace(".",""))
    except Exception as e:
        return 0


padron = read_table("https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/33571.csv?nocab=1", sep=";", dtype=str)
last_year = padron.loc[0]["Periodo"].split(" ")[-1]
padron = padron[padron["Periodo"] == padron.loc[0]["Periodo"]]
padron = padron[padron["Municipios"] != "Total Nacional"]
padron = padron.sort_values(by=['Municipios'])
padron["Municipios"] = list(map(lambda x: x.split(" ")[0], padron["Municipios"]))
_01001 = padron[padron["Municipios"] == "01001"]
padron["Total_2"] = list(map(ine_num_str2int, padron["Total"]))
padron = padron.pivot_table(index="Municipios", columns=["Sexo", "Nacionalidad", "Edad (grandes grupos)"], values="Total_2")
padron.columns = list(map(lambda x: x[0].replace(" ","_") + "_" + x[1].replace(" ","_") + "_" + x[2].replace(" ","_"), padron.columns))
padron.reset_index(inplace=True)
padron["Ultimo_periodo"] = last_year
padron.to_csv("padron.csv", sep=";", index=False)
```

## Businesses by municipalities [DATA](https://www.ine.es/jaxiT3/Tabla.htm?t=4721)

```python
from pandas import read_table

def ine_num_str2int(valor):
    try:
        if valor[-2:] == ".0":
            return int(valor[:-2].replace(".",""))
        else:
            return int(valor.replace(".",""))
    except Exception as e:
        return 0

empresas_cnae = read_table("https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/4721.csv?nocab=1", sep=";", dtype=str)
last_year = empresas_cnae.loc[0]["Periodo"].split(" ")[-1]
empresas_cnae = empresas_cnae[empresas_cnae["Periodo"] == empresas_cnae.loc[0]["Periodo"]]
empresas_cnae = empresas_cnae[empresas_cnae["Municipios"] != "Total Nacional"]
empresas_cnae = empresas_cnae.sort_values(by=['Municipios'])
empresas_cnae["Municipios"] = list(map(lambda x: x.split(" ")[0], empresas_cnae["Municipios"]))
_01001 = empresas_cnae[empresas_cnae["Municipios"] == "01001"]
empresas_cnae["Total_2"] = list(map(ine_num_str2int, empresas_cnae["Total"]))
empresas_cnae = empresas_cnae.pivot_table(index="Municipios", columns=["Grupos CNAE"], values="Total_2")
empresas_cnae.columns = list(map(lambda x: x.replace(" ","_"), empresas_cnae.columns))
empresas_cnae.reset_index(inplace=True)
empresas_cnae["Ultimo_periodo"] = last_year
empresas_cnae.to_csv("empresas_cnae.csv", sep=";", index=False)
```

## % Tourist housing [DATA](https://www.ine.es/jaxiT3/Tabla.htm?t=39366)

```python
from pandas import read_table

def ine_num_str2float(valor):
    try:
        return float(valor.replace(".","").replace(",","."))
    except Exception as e:
        return 0

pct_viviendas = read_table("https://www.ine.es/jaxiT3/files/t/en/csv_bdsc/39366.csv?nocab=1", sep=";", dtype=str)
pct_viviendas = pct_viviendas[pct_viviendas["Periodo"] == pct_viviendas.loc[0]["Periodo"]]
pct_viviendas = pct_viviendas[pct_viviendas["Municipalities"] != "National Total"]
pct_viviendas = pct_viviendas.sort_values(by=['Municipalities'])
pct_viviendas["Municipalities"] = list(map(lambda x: x.split(" ")[0], pct_viviendas["Municipalities"]))
_01001 = pct_viviendas[pct_viviendas["Municipalities"] == "01001"]
pct_viviendas["Total"] = list(map(ine_num_str2float, pct_viviendas["Total"]))
pct_viviendas.columns = ["Municipios", "Periodo", "Total"]
pct_viviendas.to_csv("pct_viviendas.csv", sep=";", index=False)
```

## Tourist housing [DATA](https://www.ine.es/jaxiT3/Tabla.htm?t=39363)

```python
from pandas import read_table

def ine_num_str2float(valor):
    try:
        return float(valor.replace(".","").replace(",","."))
    except Exception as e:
        return 0
        
viviendas_turisticas = read_table("https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/39363.csv?nocab=1", sep=";", dtype=str)
last_year = viviendas_turisticas.loc[0]["Periodo"].split(" ")[-1]
viviendas_turisticas = viviendas_turisticas[viviendas_turisticas["Periodo"] == viviendas_turisticas.loc[0]["Periodo"]]
viviendas_turisticas = viviendas_turisticas[viviendas_turisticas["Municipios"] != "Total Nacional"]
viviendas_turisticas = viviendas_turisticas.sort_values(by=['Municipios'])
viviendas_turisticas["Municipios"] = list(map(lambda x: x.split(" ")[0], viviendas_turisticas["Municipios"]))
_01001 = viviendas_turisticas[viviendas_turisticas["Municipios"] == "01001"]
viviendas_turisticas["Total_2"] = list(map(ine_num_str2float, viviendas_turisticas["Total"]))
viviendas_turisticas = viviendas_turisticas.pivot_table(index="Municipios", columns=["Viviendas y plazas"], values="Total_2")
viviendas_turisticas.columns = list(map(lambda x: x.replace(" ","_"), viviendas_turisticas.columns))
viviendas_turisticas.reset_index(inplace=True)
viviendas_turisticas["Ultimo_periodo"] = last_year
viviendas_turisticas.to_csv("viviendas_turisticas.csv", sep=";", index=False)
```
