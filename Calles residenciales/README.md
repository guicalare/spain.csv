# **Calles residenciales**

## **Licencia de este repositorio**

Debido a que este repositorio y sus codigos estan [licenciasdos](https://github.com/guicalare/spain.csv/blob/main/LICENSE) bajo la licencia [MIT](https://opensource.org/licenses/MIT) no me hago responsable del uso que se le de ni tampoco a si el codigo funciona.

> MIT License
>
>Copyright (c) 2021 Guillermo
>
>Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
>
>The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
>
>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## **Fuentes de datos y licencias**

Debido a la naturaleza de las bases de datos, es necesario citar las bases de datos asi como sus correspondientes licencias. Independientemente, los datos de este repositorio pueden usarse de forma libre y en cualquier ambito (lo que entiendo yo al leer las siguientes licencias y terminos de uso) siempre y cuando se sigan las indicaciones de las licencias.

 - **Fuente:** Open Streat Maps [geofabrik](https://download.geofabrik.de/)
  > This {calles residenciales España} is made available under the Open Database License: http://opendatacommons.org/licenses/odbl/1.0/. Any rights in individual contents of the database are licensed under the Database Contents License: http://opendatacommons.org/licenses/dbcl/1.0/
  >
  > Open Data Commons Open Database License (ODbL) Summary
>
>This is a human-readable summary of the [ODbL 1.0 license](https://opendatacommons.org/licenses/odbl/1-0/). Please see the disclaimer below.
>
>You are free:
>
>    To share: To copy, distribute and use the database.
>    To create: To produce works from the database.
>    To adapt: To modify, transform and build upon the database.
>
>As long as you:
>
>    Attribute: You must attribute any public use of the database, or works produced from the database, in the manner specified in the ODbL. For any use or redistribution of the database, or works produced from it, you must make clear to others the license of the database and keep intact any notices on the original database.
>    Share-Alike: If you publicly use any adapted version of this database, or works produced from an adapted database, you must also offer that adapted database under the ODbL.
>    Keep open: If you redistribute the database, or an adapted version of it, then you may use technological measures that restrict the work (such as DRM) as long as you also redistribute a version without such measures.
>
>Disclaimer
>
>This is not a license. It is simply a handy reference for understanding the [ODbL 1.0 license](https://opendatacommons.org/licenses/odbl/1-0/) — it is a human-readable expression of some of its key terms. This document has no legal value, and its contents do not appear in the actual license. [Read the full ODbL 1.0 license text for the exact terms that apply](https://opendatacommons.org/licenses/odbl/1-0/).

## **Definición**

> #### **Openstreetmap** [Web](https://wiki.openstreetmap.org/wiki/ES:Tag:highway%3Dresidential)
>
> Esta etiqueta se usa para carreteras que dan acceso o pasan alrededor de áreas residenciales pero no son vías clasificadas ni vías sin clasificar (unclassified).
>
>Ésta es una guía útil si no estás seguro de usar residential o unclassified para calles en poblado:
> residential - calle o carretera utilizada generalmente sólo para el tráfico local por personas que viven dentro del asentamiento.
>
>unclassified - una carretera que no tiene una clasificación administrativa ref=*. Las carreteras sin clasificación normalmente constituyen el elemento más bajo de la red de interconexión por carretera (inferior a highway=tertiary). Se usan habitualmente para la interconexión de pequeños asentamientos. Usa residential en lugar de unclassified en la sección de carretera que corresponda cuando haya restricciones de tráfico (como límites de velocidad más bajos) o elementos de calmado de tráfico cerca de pequeños asentamientos (véase también highway=unclassified).

## **Datos**

Debido a la gran cantidad de datos, recomiendo bajarte los datos brutos finales de mi repositorio de [Kaggle](https://www.kaggle.com/mordulv/spanish-streets), ya que para llegar hasta ellos se necesitan muchas horas y un ordenador potente capaz de trabajar con archivos grandes.

## **Instrucciones**

### Version 0

https://centrodedescargas.cnig.es/CentroDescargas/catalogo.do?Serie=CAANE# -> red de transporte -> toda españa -> shp >:D

### Version 1

```

wget -O - http://m.m.i24.cc/osmfilter.c |cc -x c - -O3 -o osmfilter
wget -O - http://m.m.i24.cc/osmconvert.c | cc -x c - -lz -O3 -o osmconvert

wget https://download.geofabrik.de/europe/spain-latest.osm.bz2
bzip2 -d -f -k spain-latest.osm.bz2

./osmfilter spain-latest.osm --keep="addr:*" --ignore-dependencies > calles.osm
./osmconvert calles.osm --all-to-nodes --csv="@id @lon @lat addr:city addr:postcode addr:street addr:housenumber addr:housename addr:flats addr:door addr:hamlet addr:suburb addr:subdistrict addr:district " --csv-headline > calles.csv

```

### Version 2

Open streat maps es un proyecto open source y alternativo a Google maps que sirve para obtener informacion geografica de cualquier zona (calles, shape files, rios, etc...).

Antes de nada, tendremos que descargar todos los archivos necesarios para poder obtener un callejero de vias residenciales de España.

```

wget https://download.geofabrik.de/europe/spain-latest-free.shp.zip & wget https://download.geofabrik.de/africa/canary-islands-latest-free.shp.zip
unzip canary-islands-latest-free.shp.zip -d ./canarias & unzip spain-latest-free.shp.zip -d ./peninsula

```

**Nota**: por razones desconocidad, el servicio de geofabrik suele tener conflicos de las urls *.latest-free.shp.zip por lo que en caso de que de error la descarga de los anteriores links, te recomiendo ir al [directorio](https://download.geofabrik.de/europe/) de geofabrik y reempleazar la url conflictiva con otra mas antigua que termine en *free.shp.zip. Ejemplo:

```

wget https://download.geofabrik.de/europe/spain-210901-free.shp.zip

```

Una vez ya tenemos descargados los archivos, procedermos a filtrar los datos por calles residenciales. Para esto, ejecutaremos el siguiente codigo:

```python
# Extraccion de calles residenciales

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

Una vez tenemos los datos guardados, tendremos que añadir mas informacion a las calles. Para ello existen dos opciones:

### **Usar la request API de Nominatim** [web](https://nominatim.org/release-docs/develop/api/Lookup/)

En el caso de optar por esta opcion, se tendra que emplear este codigo:

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
    sleep(1) # Respeta el tiempo entre llamadas y evita cargar al servidor

```

**Nota**: debido a que se esta usando un servidor ajeno y publico, tendremos que respetar sus normas y evitar colapsar el servidor con peticiones. Es por ello que sera necesario un tiempo de espera entre peticion y peticion (ya viene implementado en el codigo). Lo que aumentara el tiempo de procesamiento mucho mas.

Para terminar, tendras que unir las bases de datos "datos" y "final_data" mediante el ID "way_id", que no es mas que "w" + osm_id.

### **Hostear en el ordenador la API de Nominatim** [documentacion](https://github.com/mediagis/nominatim-docker/tree/master/3.7)

Por el contrario, si queremos optar por este camino, tendremos que instalar primero una serie de dependencias y aplicaciones:

- **Docker**: [instrucciones de instalacion](https://docs.docker.com/engine/install/)
- **Osmium tool**: [instrucciones de instalacion](https://osmcode.org/osmium-tool/)

Una vez tengamos instalados tanto docker como Osmium tendremos que descargar las bases de datos de la peninsula e islas del servidor de Nominatium y luego juntarlas en una unica base de datos llamada **spain.osm.pbf**:

```

wget https://download.geofabrik.de/europe/spain-latest.osm.pbf & wget https://download.geofabrik.de/africa/canary-islands-latest.osm.pbf
osmium merge spain-latest.osm.pbf canary-islands-latest.osm.pbf -o spain.osm.pbf

```

Cuando termine este proceso, tendremos que crear e inicializar el servicio de consulta api via docker (**este proceso puede tardar entre 30 minutos y 1h pero puede variar en funcion de la potencia del ordenador**). Para ello se tendra que ejecutar la siguiente linea en docker:

```

sudo docker run -it --rm \
  -e PBF_PATH=/nominatim/data/spain.osm.pbf \
  -e REPLICATION_URL=https://download.geofabrik.de/ \
  -p 8080:8080 \
  -v <YOUR_DIRECTORY>:/nominatim/data \
  --name nominatim \
  mediagis/nominatim:3.7

```

**Importante**: cambia **<YOUR_DIRECTORY>** por el directorio de la carpeta donde tengas creada la base de datos **spain.osm.pbf**. En el caso de que cambies el nombre del archivo **spain.osm.pbf** tendras que reemplazar dicho nombre en la sentencia -e de la creacion del contenedor de docker.

Cuando el servicio de docker este activo y listo, se tendra que ejecutar el siguiente codigo:

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

Para terminar, tendras que unir las bases de datos "datos" y "final_data" mediante el ID "way_id", que no es mas que "w" + osm_id.

### Añadir altitud a las Calles

Ya tenemos la base de datos de las calles residenciales con nombres, coordenadas, etc... pero nos queda saber la altitud de las mismas. Para ello, haremos uso de [Open elevation](https://www.open-elevation.com/) que es un proyecto opensource que nos permite saber la altitud de una coordenada.

Nuevamente existen las alternativas de usar el servidor publico o hostarlo en nuestro propio ordenador, pero en este caso recominedo hostear el servicio, ya que como dijo el [autor](https://stackoverflow.com/questions/65748099/open-elevation-api-for-python/68697220#68697220) de esta herramientda, el servidor publico suele dar problemas debido a que no es tan potente como otros servicios publicos opensource. Considera la opcion de [donar dinero al autor](https://www.open-elevation.com/#donate) para mejorar el servicio.

Sigue las [instrucciones](https://github.com/Jorl17/open-elevation/blob/master/docs/host-your-own.md) para hostaer el servicio de open elevation y luego ejecuta el siguiente codigo:

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
