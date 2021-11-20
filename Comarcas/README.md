# **Comarcas agrarias**

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

 - **Fuente:** 	© Ministerio de Agricultura, Pesca y Alimentación (Comarcas Agrarias)
 > Esta información se puede usar de modo libre y gratuito siempre que se mencione al Ministerio de Agricultura, Pesca y Alimentación (MAPA) como autor y propietario de la información de la siguiente manera: Fuente: «© Ministerio de Agricultura, Pesca y Alimentación (MAPA)»
 >
 > [Mas informacion](https://www.mapa.gob.es/es/cartografia-y-sig/ide/descargas/agricultura/default.aspx)

## **Definición**

> #### **Ministerio de agricultura, pesca y alimentacion** [Web](https://www.mapa.gob.es/es/cartografia-y-sig/ide/descargas/agricultura/default.aspx)
>
>  La distribución de la superficie de España en “Comarcas Agrarias” fue una iniciativa del antiguo Ministerio de Agricultura que tuvo su origen al inicio de la década de los 70 del pasado siglo y se materializó en 1976 con la publicación del documento de la Secretaría General Técnica que llevaba por título “Comarcalización Agraria de España” respondiendo a la necesidad de agrupar los territorios en “unidades espaciales intermedias entre la provincia y el municipio que sin personalidad jurídico-administrativa alguna, tuvieran un carácter uniforme desde el punto de vista agrario, que permitiera utilizarlas como unidades para la planificación y ejecución de la actividad del Ministerio y para la coordinación de sus distintos Centros Directivos”. En este trabajo, la superficie española se agrupaba en 322 comarcas agrarias. [...]


## **Instrucciones**

El **[INE](https://ine.es/)** tiene un [excel](http://www.ine.es/daco/daco42/agricultura/comarcas99_metodologia.xls) donde aparecen las relaciones entre municipios y las 319 comarcas agrarias. Por otra parte, el Ministerio de agricultura posee un [shape file](https://www.mapa.gob.es/es/cartografia-y-sig/ide/descargas/ComarcasAgrarias_tcm30-175866.rar) (.shp) con 356 comarcas. Como se puede observar, existe una diferencia significativa entre la base de datos del INE y del ministerio, por lo que solo nos podremos fiar del shape file, ya que por asi decirlo es un mapa oficial.

```python
# Cargar librerias necesarias

from geopandas import read_file
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

municipios = read_file("shp/municipios/municipios_espanna.shp")
comarcas = read_file("shp/comarcas/ComarcasAgrarias.shp")

```

```python
>>> municipios
                     NAMEUNIT cod_ine  provincia                                           geometry
0         Caldes de Malavella   17033         17  POLYGON ((2.75239 41.85429, 2.75291 41.85453, ...
1       Calonge i Sant Antoni   17034         17  MULTIPOLYGON (((3.11364 41.84826, 3.11364 41.8...
2                       Camós   17035         17  POLYGON ((2.73213 42.08602, 2.73222 42.08613, ...
3                 Campdevànol   17036         17  POLYGON ((2.09486 42.22201, 2.09489 42.22210, ...
4                   Campelles   17037         17  POLYGON ((2.09759 42.28165, 2.09756 42.28182, ...
...                       ...     ...        ...                                                ...
8126             Vallehermoso   38050         38  MULTIPOLYGON (((-17.32973 28.08035, -17.32968 ...
8127  La Victoria de Acentejo   38051         38  MULTIPOLYGON (((-16.48783 28.43752, -16.48775 ...
8128       Vilaflor de Chasna   38052         38  POLYGON ((-16.68464 28.12064, -16.68468 28.120...
8129            Villa de Mazo   38053         38  MULTIPOLYGON (((-17.79311 28.52490, -17.79311 ...
8130    El Pinar de El Hierro   38901         38  MULTIPOLYGON (((-17.96450 27.68740, -17.96445 ...

[8131 rows x 4 columns]

>>> comarcas
     CO_CCAA    DS_CCAA  ...          DS_COMARCA                                           geometry
0          6  Cantabria  ...             COSTERA  MULTIPOLYGON (((-3.58988 43.51366, -3.58970 43...
1          6  Cantabria  ...             LIEBANA  POLYGON ((-4.64658 43.26886, -4.64571 43.26879...
2          6  Cantabria  ...  TUDANCA-CABUERNIGA  POLYGON ((-4.40131 43.29627, -4.39187 43.29300...
3          6  Cantabria  ...           PAS-IGUÑA  POLYGON ((-3.70508 43.31434, -3.70258 43.31342...
4          6  Cantabria  ...                ASON  MULTIPOLYGON (((-3.50917 43.30201, -3.50674 43...
..       ...        ...  ...                 ...                                                ...
351        5   Canarias  ...   NORTE DE TENERIFE  MULTIPOLYGON (((-16.32170 28.57803, -16.32022 ...
352        5   Canarias  ...     SUR DE TENERIFE  MULTIPOLYGON (((-16.12064 28.55877, -16.12096 ...
353        5   Canarias  ...    ISLA DE LA PALMA  MULTIPOLYGON (((-17.91369 28.85651, -17.91333 ...
354        5   Canarias  ...   ISLA DE LA GOMERA  MULTIPOLYGON (((-17.27479 28.21804, -17.27446 ...
355        5   Canarias  ...      ISLA DE HIERRO  MULTIPOLYGON (((-17.92494 27.84918, -17.92391 ...

[356 rows x 7 columns]

>>> comarcas.columns
Index(['CO_CCAA', 'DS_CCAA', 'CO_PROVINC', 'DS_PROVINC', 'CO_COMARCA',
       'DS_COMARCA', 'geometry'],
      dtype='object')

```

Como se puede observar, no existe una columna que realcione las comarcas con los municipios, pero al tener los vectores de ambas entidades podremos ir viendo el area en comun de cada municipio con cada comarca mapeando de forma "manual" dicha realcion.

```python
# Creacion de mapas fronterizos de municipios y comarcas

fig, ax = plt.subplots(figsize = (20,16))

municipios.geometry.boundary.plot(color="blue",edgecolor='k',linewidth = 1,ax=ax)
comarcas.geometry.boundary.plot(color="red",edgecolor='k',linewidth = 2,ax=ax)

plt.savefig("img/limites.png")

```

![limites](https://raw.githubusercontent.com/guicalare/spain.csv/main/Comarcas/img/limites.png)

Dicha relacion se consigue ejecutando el siguiente codigo:

```python
# Cruce de municipios por area comun

municipios["area_comun"] = 0
municipios["CO_COMARCA"] = "-9999"
municipios["DS_COMARCA"] = "--NAN--"

mun_list, com_list, area_com = [], [], []

for idx_mun, row_mun in municipios.iterrows():
    municipio_area = row_mun["geometry"].area
    comarcas_querry = comarcas[comarcas["CO_PROVINC"] == int(row_mun["cod_ine"][:2])]
    for idx_com, row_com in comarcas_querry.iterrows():
        area_comun = row_mun["geometry"].intersection(row_com["geometry"]).area/municipio_area
        if area_comun >= 0.55: # % de area comun. A mayor valor, mas municipios solitarios
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
print(f"Area minima registrada: {min(area_com)}")

```

Al representar el match en % de cada municipio con su area comarcal, podremos observar que el cruce final es de buena calidad, ya que la gran mayoria tienen un porcentaje muy cercano al 100%.

```python
# Mapa de municipios y comarcas por % de area en comun

fig, ax = plt.subplots(figsize = (20,16))

municipios.plot(column='area_comun', legend=True, ax=ax, edgecolor='k', linewidth = 1)
comarcas.geometry.boundary.plot(color="red",edgecolor='k',linewidth = 2,ax=ax)

plt.savefig("img/areas.png")
```

![areas](https://raw.githubusercontent.com/guicalare/spain.csv/main/Comarcas/img/areas.png)

Exportar los shape files de los municipios con sus correspondientes comarcas:

```python
municipios.to_file("/home/guillermo/Comarcas/municipios_2_comarcas/municipios_comarcas.shp")
municipios[["cod_ine", 'CO_COMARCA', 'DS_COMARCA']].to_csv("/home/guillermo/Comarcas/municipios_2_comarcas/relacion_municipios_comarcas.csv", index=False, sep=";")

```

Puedes encontrar el codigo completo en el archivo **[comarcas.py](https://github.com/guicalare/spain.csv/blob/main/Comarcas/comarcas.py)**
