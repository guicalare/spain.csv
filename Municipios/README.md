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

## **Definición**

> #### **Wikipedia** [Web](https://es.wikipedia.org/wiki/Municipio_(Espa%C3%B1a))
>
>  En España, un municipio es, según la Ley reguladora de las Bases del Régimen Local, la entidad local básica de la organización territorial del Estado. La misma ley indica que el municipio tiene personalidad jurídica y plena capacidad para el cumplimiento de sus fines y que sus elementos son el territorio, la población y la organización. [...]

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

Exportar los shape files de los municipios:

```python

municipios.to_file("shp/municipios final/municipios_espanna.shp")
municipios[["NAMEUNIT", "cod_ine"]].to_csv("data/municipios.csv")

```

Puedes encontrar el codigo completo en el archivo **[municipios.py](https://github.com/guicalare/spain.csv/blob/main/Municipios/municipios.py)**

# **Datos municipales**

WORK IN PROGRESS
