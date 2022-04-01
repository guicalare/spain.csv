# **Municipios España**

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

## **Definiciones**

> #### **Municipios** [Wikipedia](https://es.wikipedia.org/wiki/Municipio_(Espa%C3%B1a))
>
>  En España, un municipio es, según la Ley reguladora de las Bases del Régimen Local, la entidad local básica de la organización territorial del Estado. La misma ley indica que el municipio tiene personalidad jurídica y plena capacidad para el cumplimiento de sus fines y que sus elementos son el territorio, la población y la organización. [...]

> #### **Geohash** [Wikipedia](https://en.wikipedia.org/wiki/Geohash)
>
>  Geohash is a public domain geocode system invented in 2008 by **Gustavo Niemeyer** which encodes a geographic location into a short string of letters and digits. Similar ideas were introduced by G.M. Morton in 1966. It is a hierarchical spatial data structure which subdivides space into buckets of grid shape, which is one of the many applications of what is known as a Z-order curve, and generally space-filling curves.

# **Limites**

## **Fuentes de datos y licencias**

Debido a la naturaleza de las bases de datos, es necesario citar las bases de datos asi como sus correspondientes licencias. Independientemente, los datos de este repositorio pueden usarse de forma libre y en cualquier ambito (lo que entiendo yo al leer las siguientes licencias y terminos de uso) siempre y cuando se sigan las indicaciones de las licencias.

 - **Fuente:** Límites municipales, provinciales y autonómicos 2021 CC-BY 4.0 [ign.es](https://www.ign.es)
  > ### Licencia de los productos y servicios de datos geográficos producidos por el IGN y de los coproducidos por las CC. AA. y la AGE en el marco del Sistema Cartográfico Nacional
  > En  esta  licencia  se  establecen  las  condiciones  de  uso  y  acceso  a  los  productos  y  servicios  de  información  geográfica  generados  por  la  Dirección  General  del  Instituto  Geográfico  Nacional  de España, en adelante IGN, que depende del Ministerio  de  Fomento,  condiciones  que  s e  ajustan a lo establecido en la Orden Ministerial FOM/2807/2015, de 18 de diciembre del año 2015, BOE 2015.12.26, que modifica la Orden Ministerial FOM/956/2008 de fecha 31 de marzo, BOE 2008.04.08.
  >
  > Según  se  recoge  en  la  mencionada  Orden  Ministerial  FOM/2807/2015,  Artículo  4:  «El  uso  de  los  productos  de  datos  geográficos  digitales  mencionados  en  el  Artículo  2  tendrá  carácter  libre  y  gratuito,  siempre  que  se  mencione  el  origen  y  propiedad  de  los  datos,  con  el  alcance  y  forma  que autorice la licencia de uso correspondiente».
  >
  > [...]
  >
  > Para  los  productos,  en  el    caso  de  que  no  se  modifique  o  altere  la  información  geográfica digital  original,  se  utilizará  la  expresión  general:  «<identificador  del  producto>  <fecha>  CC-BY 4.0 <atribución de productores>», en la que las etiquetas <identificador del producto>, <fecha> y <atribución de productores> serán sustituidas por los valores correspondientes de la tabla de productos, que se encuentra en la  página web publicada a tal efecto [...]
  >
  > [Licencia completa](https://www.ign.es/resources/licencia/Condiciones_licenciaUso_IGN.pdf)

## **Instrucciones**

El Instituto Geografico Nacional de España tiene una serie de bases de datos donde se incluyen imagenes e mapas, shape files (.shp), cartografias, etc... En este caso nos centraremos en los limites municipales del territorio español (peninsula e islas). Para ello, nos dirigiremos a esta [web](https://centrodedescargas.cnig.es/CentroDescargas/buscador.do) y descargaremos los shape files que se encuentran situados en la siguiente ruta: **"divisiones administrativas" >> "Toda España" >> "Limites municipales, provinciales y autonómicos"**.

Una vez tenemos los correspondientes ficheros shp, procederemos a cargar la infromacion en python, para ello emplearemos el siguiente codigo:

```python
# Cargar librerias y datos necesarios

from geopandas import read_file
from pandas import merge, read_csv, concat

municipios1 = read_file("shp/recintos_municipales_inspire_peninbal_etrs89/recintos_municipales_inspire_peninbal_etrs89.shp")
municipios2 = read_file("shp/recintos_municipales_inspire_canarias_wgs84/recintos_municipales_inspire_canarias_wgs84.shp")

```

```python

>>> municipios1
                     INSPIREID COUNTRY  ... CODNUT3                                           geometry
0     ES.IGN.BDDAE.34091717033      ES  ...   ES512  POLYGON ((2.75239 41.85429, 2.75291 41.85453, ...
1     ES.IGN.BDDAE.34091717034      ES  ...   ES512  MULTIPOLYGON (((3.11364 41.84826, 3.11364 41.8...
2     ES.IGN.BDDAE.34091717035      ES  ...   ES512  POLYGON ((2.73213 42.08602, 2.73222 42.08613, ...
3     ES.IGN.BDDAE.34091717036      ES  ...   ES512  POLYGON ((2.09486 42.22201, 2.09489 42.22210, ...
4     ES.IGN.BDDAE.34091717037      ES  ...   ES512  POLYGON ((2.09759 42.28165, 2.09756 42.28182, ...
...                        ...     ...  ...     ...                                                ...
8124  ES.IGN.BDDAE.34091717028      ES  ...   ES512  POLYGON ((2.61315 41.91290, 2.61361 41.91327, ...
8125  ES.IGN.BDDAE.34091717029      ES  ...   ES512  POLYGON ((2.83689 42.33952, 2.83847 42.34107, ...
8126  ES.IGN.BDDAE.34091717030      ES  ...   ES512  POLYGON ((2.94377 42.33121, 2.94402 42.33132, ...
8127  ES.IGN.BDDAE.34091717031      ES  ...   ES512  MULTIPOLYGON (((2.82788 42.18302, 2.82794 42.1...
8128  ES.IGN.BDDAE.34091717032      ES  ...   ES512  MULTIPOLYGON (((3.30879 42.29113, 3.30873 42.2...

[8129 rows x 10 columns]
>>> municipios2
                   INSPIREID COUNTRY  ... CODNUT3                                           geometry
0   ES.IGN.BDDAE.34053535001      ES  ...   ES705  MULTIPOLYGON (((-15.74605 28.05094, -15.74605 ...
1   ES.IGN.BDDAE.34053535002      ES  ...   ES705  MULTIPOLYGON (((-15.38210 27.86163, -15.38204 ...
2   ES.IGN.BDDAE.34053535003      ES  ...   ES704  POLYGON ((-14.05965 28.37793, -14.05962 28.378...
3   ES.IGN.BDDAE.34053535004      ES  ...   ES708  MULTIPOLYGON (((-13.54974 28.95257, -13.54947 ...
4   ES.IGN.BDDAE.34053535005      ES  ...   ES705  POLYGON ((-15.77285 28.03183, -15.77286 28.031...
..                       ...     ...  ...     ...                                                ...
83  ES.IGN.BDDAE.34053838050      ES  ...   ES706  MULTIPOLYGON (((-17.32973 28.08035, -17.32968 ...
84  ES.IGN.BDDAE.34053838051      ES  ...   ES709  MULTIPOLYGON (((-16.48783 28.43752, -16.48775 ...
85  ES.IGN.BDDAE.34053838052      ES  ...   ES709  POLYGON ((-16.68464 28.12064, -16.68468 28.120...
86  ES.IGN.BDDAE.34053838053      ES  ...   ES707  MULTIPOLYGON (((-17.79311 28.52490, -17.79311 ...
87  ES.IGN.BDDAE.34053838901      ES  ...   ES703  MULTIPOLYGON (((-17.96450 27.68740, -17.96445 ...

[88 rows x 10 columns]

```

Una vez tenemos cargados ambos ficheros, procederemos a concatenarlos y agruparlos en una unica variable:

```python
# Concatenar shape files

municipios = concat([municipios1, municipios2], ignore_index=True)

```

```python

>>> municipios.columns
Index(['INSPIREID', 'COUNTRY', 'NATLEV', 'NATLEVNAME', 'NATCODE', 'NAMEUNIT',
       'CODNUT1', 'CODNUT2', 'CODNUT3', 'geometry'],
      dtype='object')

```

Ahora pasaremos a depurar la base de datos, ya que como se puede observar en la salida anterior, existen codigos ine, postales, etc... pegados unos con otro, por lo que procederemos a darle un formato mas claro y amigable:

```python
# Depuracion de la base de datos de municipios

municipios = municipios[["NAMEUNIT", "NATCODE", "geometry"]]
municipios["cod_ine"] = list(map(lambda x: x[-5:], municipios.NATCODE))
municipios["provincia"] = list(map(lambda x: int(x[:2]), municipios.cod_ine))
municipios = municipios[municipios["provincia"] <= 52]
municipios.reset_index(inplace=True)

del(municipios["NATCODE"])
del(municipios["index"])

```

```python

>>> municipios
                     NAMEUNIT                                           geometry cod_ine  provincia
0         Caldes de Malavella  POLYGON ((2.75239 41.85429, 2.75291 41.85453, ...   17033         17
1       Calonge i Sant Antoni  MULTIPOLYGON (((3.11364 41.84826, 3.11364 41.8...   17034         17
2                       Camós  POLYGON ((2.73213 42.08602, 2.73222 42.08613, ...   17035         17
3                 Campdevànol  POLYGON ((2.09486 42.22201, 2.09489 42.22210, ...   17036         17
4                   Campelles  POLYGON ((2.09759 42.28165, 2.09756 42.28182, ...   17037         17
...                       ...                                                ...     ...        ...
8126             Vallehermoso  MULTIPOLYGON (((-17.32973 28.08035, -17.32968 ...   38050         38
8127  La Victoria de Acentejo  MULTIPOLYGON (((-16.48783 28.43752, -16.48775 ...   38051         38
8128       Vilaflor de Chasna  POLYGON ((-16.68464 28.12064, -16.68468 28.120...   38052         38
8129            Villa de Mazo  MULTIPOLYGON (((-17.79311 28.52490, -17.79311 ...   38053         38
8130    El Pinar de El Hierro  MULTIPOLYGON (((-17.96450 27.68740, -17.96445 ...   38901         38

[8131 rows x 4 columns]

```

Una vez tenemos creada la base de datos, procederemos a usar la libreria [polygeohasher](https://github.com/rohitsinghsalyan/polygeohasher), la cual nos ayudara a transformar un poligono (en este caso los municipios) en geohashes con el fin de obtener una relacion entre un geohash y un municipio. Esto puede sonar un poco confuso, asi que como se suele decir: "una imagen vale mas que mil palabras". Veamos el ejemplo que se plantea en el github de [polygeohasher](https://github.com/rohitsinghsalyan/polygeohasher):

Partimos un municipio (en este ejemplo se seguira el que aparece en polygeohasher):

![a](https://raw.githubusercontent.com/rohitsinghsalyan/polygeohasher/master/example/study_area.png)

Y queremos obtener la combinacion optima e ideal de geohashes que engloben el municipio:

![](https://raw.githubusercontent.com/rohitsinghsalyan/polygeohasher/master/example/secondary_output.png)

Como se puede observar en el ejemplo de polygeohasher, se pueden dar ciertos problemas en las zonas fronterizas de los municipios, por lo que es algo a tener en cuenta al usar esta base de datos (retornar 2 o mas respuestas). No obstante, no existira problema alguno entre los geohashes que caigan en el centro del municipio, ya que retornaran una una respuesta

Bueno, al lio. Para obtener todo esto se tendra que aplicar el siguiente codigo:


```python
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
```

**Importante**: este proceso puede durar horas o dias, por lo que recomiendo ejecutar varias instancias del codigo de arriba apuntando a diferentes partes de la base de datos de los municipios con el fin de calcular varios municipios a la vez. Esto es:

```python

# En una terminal ejecutar esto [ira del municipio 8131 hasta el municipio 0]

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

# En otra terminal ejecutar esto [ira del municipio 4000 hasta el municipio 0]

for i in range(4000, -1, -1):
    archivos = listdir("/home/guillermo/Descargas/shp/geohash_shp")
    data_slice = municipios[i-1:i]
    try:
        if data_slice.shape[0] >= 1:
            id = data_slice["cod_ine"][i-1]
            if f"{id}.csv" not in archivos:
                print(f"{i} {id}")
                primary_df = polygeohasher.create_geohash_list(data_slice, 8, inner=False)
                secondary_df = polygeohasher.geohash_optimizer(primary_df, 3, 8, 8)
                secondary_df.to_csv(f"/home/guillermo/Descargas/shp/geohash_shp/{id}.csv", sep="#", index=False)
            else:
                print(f"EXISTE {i} -- {id}.csv")
    except Exception as e:
        print(e)

# ETC...
```

Esto mismo se podria programar orientado a [hilos](https://realpython.com/intro-to-python-threading/) (yo he optado por esta opcion, pese a ser algo primitiva). 

**Ejemplo de salida de municipio a geohash**

```python
>>> data
      Unnamed: 0             NAMEUNIT  cod_ine  provincia optimized_geohash_list
0            318  Caldes de Malavella    17033         17               sp3vyy0b
1            318  Caldes de Malavella    17033         17               sp3vzh2f
2            318  Caldes de Malavella    17033         17               sp3ynf8j
3            318  Caldes de Malavella    17033         17               sp6jb4qz
4            318  Caldes de Malavella    17033         17               sp6jbcne
...          ...                  ...      ...        ...                    ...
5459         318  Caldes de Malavella    17033         17               sp3ypp64
5460         318  Caldes de Malavella    17033         17               sp6n07dg
5461         318  Caldes de Malavella    17033         17                sp3vyyr
5462         318  Caldes de Malavella    17033         17               sp6n04st
5463         318  Caldes de Malavella    17033         17               sp3vzf8u

[5464 rows x 5 columns]
```

Una vez ya se han generado los archivos, procederemos a concatenerlos y a guardarlos en un archivo csv unico, para ello ejecutaremos:

```python
datos = pd.concat(map(read_csv, glob.glob(path.join('/home/guillermo/Descargas/shp/geohash_shp', "*.csv"))))
datos.to_csv("/home/guillermo/Descargas/shp/bb_geohash.csv", sep="#", index=False)
```

# Usos para esta base de datos

Esta base de datos se creo con la idea de validar coordenadas o de obtener mas informacion sobre unas coordenadas. Veamos un ejemplo.

En la web de [phrozen (demo geohash)](https://phrozen.github.io/geohash/) podemos obtener el geohash en funcion de unas coordenadas. Seleccionaremos pues el ejemplo de la puerta del sol (40.416832946749224, -3.7033463198490324 que en geohash de nivel 9 es ezjmgtxm1).

Si vamos buscando dicho geohash en la base de datos (bajando o subiendo de nivel el geohash) se nos retornara la informacion del municipio:

```python
>>> datos[datos["optimized_geohash_list"] == "ezjmgtxm1"]
Empty DataFrame
Columns: [NAMEUNIT, Municipio, cod_ine, provincia, optimized_geohash_list]
Index: []
>>> datos[datos["optimized_geohash_list"] == "ezjmgtxm"]
Empty DataFrame
Columns: [NAMEUNIT, Municipio, cod_ine, provincia, optimized_geohash_list]
Index: []
>>> datos[datos["optimized_geohash_list"] == "ezjmgtx"]
Empty DataFrame
Columns: [NAMEUNIT, Municipio, cod_ine, provincia, optimized_geohash_list]
Index: []
>>> datos[datos["optimized_geohash_list"] == "ezjmgt"]
Empty DataFrame
Columns: [NAMEUNIT, Municipio, cod_ine, provincia, optimized_geohash_list]
Index: []
>>> datos[datos["optimized_geohash_list"] == "ezjmg"]
         NAMEUNIT Municipio cod_ine provincia optimized_geohash_list
24964723     2243    Madrid   28079        28                  ezjmg
```

De esta forma podemos obtener el codigo INE asi como el nombre de un municipio de unas coordenadas.

Veamos ahora el ejemplo de esto mismo pero en la frontera de dos municipios (40.70863520106818, -4.140481126892041 que en geohash de nivel 9 es ezjp9fbbz):

```python
>>> datos[datos["optimized_geohash_list"] == "ezjp9fbbz"]
Empty DataFrame
Columns: [NAMEUNIT, Municipio, cod_ine, provincia, optimized_geohash_list]
Index: []
>>> datos[datos["optimized_geohash_list"] == "ezjp9fbb"]
         NAMEUNIT   Municipio cod_ine provincia optimized_geohash_list
27117382     2233  Guadarrama   28068        28               ezjp9fbb
>>> datos[datos["optimized_geohash_list"] == "ezjp9fb"]
         NAMEUNIT   Municipio cod_ine provincia optimized_geohash_list
22397446     5792  El Espinar   40076        40                ezjp9fb
>>> datos[datos["optimized_geohash_list"] == "ezjp9f"]
Empty DataFrame
Columns: [NAMEUNIT, Municipio, cod_ine, provincia, optimized_geohash_list]
Index: []
>>> datos[datos["optimized_geohash_list"] == "ezjp9"]
Empty DataFrame
Columns: [NAMEUNIT, Municipio, cod_ine, provincia, optimized_geohash_list]
Index: []
>>> datos[datos["optimized_geohash_list"] == "ezjp"]
Empty DataFrame
Columns: [NAMEUNIT, Municipio, cod_ine, provincia, optimized_geohash_list]
Index: []
```

Como se puede observar, existen problemas en las fronteras de los municipios (tal y como se menciono anteriormente).

Puedes encontrar el codigo completo en el archivo **[municipios_geohash.py](https://github.com/guicalare/spain.csv/blob/main/Municipios_geohash/municipios_geohash.py)**

