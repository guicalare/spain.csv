# spain.csv

Spain.csv is a repository of all usefull data that I can gather and save it in a friendly csv format.

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
residential_streets["osm_id_api"] = list(map(lambda x: "W"+str(x), residential_streets["osm_id"]))
residential_streets = residential_streets[["osm_id", "osm_id_api","name", "x", "y"]]

residential_streets.to_csv("streets.csv", index=False, sep=";")
```

3. Add extra data to the streets

Now we need to get some extra data from the osm_id with reverse geocoding. To do this, we can use:

- **Oficial openstreetmaps Nominatim request API**: https://nominatim.org/release-docs/develop/api/Lookup/
- **Self-host the Nominatim request API**: https://github.com/mediagis/nominatim-docker/tree/master/3.7

In case you are using the **Self-hosted** option, you need to [install docker](https://docs.docker.com/engine/install/) 

![](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fdeveloper.ibm.com%2Fbluemix%2Fwp-content%2Fuploads%2Fsites%2F20%2F2015%2F06%2Fdocker-logo-300.png&f=1&nofb=1)

Then open a new termiinal and create a docker instance (you must repeat this 2 times):

Docker instance for the Iberian Peninsula

```
sudo docker run -it --rm \
  -e PBF_URL=https://download.geofabrik.de/europe/spain-latest.osm.pbf \
  -e REPLICATION_URL=https://download.geofabrik.de/europe/spain-updates/ \
  -p 8080:8080 \
  --name nominatim \
  mediagis/nominatim:3.7
```

Docker instance for the Canary Island

```
sudo docker run -it --rm \
  -e PBF_URL=https://download.geofabrik.de/africa/canary-islands-latest.osm.pbf \
  -e REPLICATION_URL=https://download.geofabrik.de/africa/canary-islands-updates/ \
  -p 8080:8080 \
  --name nominatim \
  mediagis/nominatim:3.7
```

Then use the next code (WORK IN PROGRESS):

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
