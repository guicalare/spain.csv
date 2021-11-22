# **Codigos postales**

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

Que yo sepa, el INE no impone algun tipo de licencia de uso para las bases de datos del callejero de Censo Electoral.

 - **Fuente:** Cartografía secciones censales y callejero de Censo Electoral [INE](https://www.ine.es/ss/Satellite?c=Page&cid=1259952026632&p=1259952026632&pagename=ProductosYServicios%2FPYSLayout)

## **Definición**

> #### **Wikipedia** [Web](https://es.wikipedia.org/wiki/C%C3%B3digo_postal_de_Espa%C3%B1a)
>
> El sistema de código postal español comprende una serie de códigos utilizados para mejorar el funcionamiento del servicio postal en España. Los códigos postales fueron introducidos en España en 1981,1​ coincidiendo con la puesta en marcha de los procedimientos automatizados de clasificación de correspondencia. Previamente, desde principios del decenio de 1961 a 1970, existían en las principales ciudades los denominados "distritos postales", que abarcaban zonas más amplias que los códigos postales que luego se introdujeron. En 1985, en una primera fase, se introdujo el uso del código solamente en las capitales de provincia (con el 0 como tercer dígito) y en las ciudades de Vigo y Gijón, al dividirse todas ellas en varias zonas y asignarse un código a cada una de ellas. En 1987, todas las localidades restantes estrenaron sus códigos postales, únicos para toda la población e incluso para varias poblaciones de un mismo municipio (tercer dígito entre el 1 y el 9). Posteriormente ha habido algunos cambios, que básicamente consistieron en la zonificación y asignación de códigos de los municipios no capitales de mayor población. [...]

## **Instrucciones**

Los codigos postales españoles pese a ser de uso publico, estan por asi decirlo explotados economicamente por [correos](https://www.correos.es), por lo que toca [pasar por caja]() para obtener dichas bases de datos (realciones [codigo postal - codigo ine](https://tienda.correos.es/product/base-de-datos-codigos-postales-plus) como sus correspondientes [mapas vectoriales](https://tienda.correos.es/product/capa-cartografica-codigos-postales)). Dicha decision parece inmoral y es algo que no se puede tolerar, ya que dichos codigos postales los usamos en nuestro dia a dia, siendo por asi decirlo un bien de interes publico que no deberia ser monetizado. Es por ello, que he decidido hacer ingenieria inversa para obtener dichos datos y sin licencia alguna.

A priori, puede parecer que esto parece un repositorio hacker y que es algo ilegal, pero me he percatado que toda esta infromacion esta publicada por el INE y solo hace falta hacer un poco de (ya lo habras adivinado...) ¡INGENIERIA INVERSA!.

El proceso es muy sencillo. El INE presenta casi cada año un [callejero censal](https://www.ine.es/ss/Satellite?c=Page&cid=1259952026632&p=1259952026632&pagename=ProductosYServicios%2FPYSLayout) donde presenta la realcion de calles con sus correspondientes codigos ine y codigos postales. Pero aun hay mas... Tambien ponen a disposicion los ficheros de mapas vectoriales de las areas censales, por lo que se podra obtener una reconstruccion de los shape files haciendo uso del callejero.

Bueno, vamos a ir al lio. Lo primero es descargarse el zip del callejero de la [web](https://www.ine.es/ss/Satellite?c=Page&cid=1259952026632&p=1259952026632&pagename=ProductosYServicios%2FPYSLayout)

![limites](https://media.githubusercontent.com/media/guicalare/spain.csv/main/codigos%20postales/img/callejero.png)

Tras esto, descomprimimos el archivo, y ejecutamos el siguiente codigo:

```python
# Creacion de tabla relacional codigos postales

from pandas import read_fwf

colspecs = [(0, 10), (42, 47)]
header = ['seccion_censal', 'cod_pos']
converters={'seccion_censal' : str, 'cod_pos' : str}

datos = read_fwf("TRAMOS_NAL_F210630",
    colspecs=colspecs,
    names=header,
    converters=converters,
    encoding = 'iso-8859-1'
)

datos.drop_duplicates(inplace=True)
datos.reset_index(inplace=True, drop=True)

datos["cod_ine"] = list(map(lambda x: x[:5], datos["seccion_censal"]))

datos.to_csv("data/codigos_postales.csv", sep=";", index=False)

```

```

>>> datos
      seccion_censal cod_pos cod_ine
0         0100101001   01240   01001
1         0100101001   01193   01001
2         0100101002   01240   01001
3         0100201001   01470   01002
4         0100201001   01450   01002
...              ...     ...     ...
46360     5200108013   52006   52001
46361     5200108013   52005   52001
46362     5200108014   52005   52001
46363     5200108015   52006   52001
46364     5200108015   52005   52001

[46365 rows x 3 columns]

```

Con esto generaremos un dataframe con la siguiente informacion:

- Seccion censal
- Codigo postal
- Codigo INE

Ya tenemos la tabla realcional que podremos usar ahora con el el mapa vectorial de las secciones censales. Para obtener dicho ficehro, volveremos a la [web](https://www.ine.es/ss/Satellite?c=Page&cid=1259952026632&p=1259952026632&pagename=ProductosYServicios%2FPYSLayout) y descargaremos el fichero correspondiente:

![limites](https://media.githubusercontent.com/media/guicalare/spain.csv/main/codigos%20postales/img/mapa_vectorial.png)

Una vez descargado, ejecutaremos el siguiente codigo:

```python
# Creacion de shape file codigos postales

from geopandas import read_file

secciones = read_file("shp/Secciones/SECC_CE_20210101.shp")

secciones.rename(columns = {'CUSEC':'seccion_censal'}, inplace = True)

codigos_postales = secciones.merge(datos, how='left', on='seccion_censal')

fig, ax = plt.subplots(figsize = (20,16))

codigos_postales.geometry.boundary.plot(color="blue",edgecolor='k',linewidth = 1,ax=ax)

plt.savefig("img/limites.png")

codigos_postales.to_file("shp/codigos postales/codigos_postales.shp")

```

```
>>> codigos_postales
      seccion_censal  CUMUN CSEC CDIS CMUN CPRO CCA    CUDIS  CLAU2         NPRO         NCA CNUT0 CNUT1 CNUT2 CNUT3 ESTADO   OBS              NMUN                                           geometry cod_pos cod_ine
0         0100101001  01001  001   01  001   01  16  0100101  01001  Araba/Álava  País Vasco    ES     2     1     1      I  None  Alegría-Dulantzi  MULTIPOLYGON (((539753.044 4743324.668, 539784...   01240   01001
1         0100101001  01001  001   01  001   01  16  0100101  01001  Araba/Álava  País Vasco    ES     2     1     1      I  None  Alegría-Dulantzi  MULTIPOLYGON (((539753.044 4743324.668, 539784...   01193   01001
2         0100101002  01001  002   01  001   01  16  0100101  01001  Araba/Álava  País Vasco    ES     2     1     1      I  None  Alegría-Dulantzi  POLYGON ((539559.740 4745571.157, 539562.677 4...   01240   01001
3         0100201001  01002  001   01  002   01  16  0100201  01002  Araba/Álava  País Vasco    ES     2     1     1      I  None           Amurrio  MULTIPOLYGON (((503618.553 4759559.798, 503620...   01470   01002
4         0100201001  01002  001   01  002   01  16  0100201  01002  Araba/Álava  País Vasco    ES     2     1     1      I  None           Amurrio  MULTIPOLYGON (((503618.553 4759559.798, 503620...   01450   01002
...              ...    ...  ...  ...  ...  ...  ..      ...    ...          ...         ...   ...   ...   ...   ...    ...   ...               ...                                                ...     ...     ...
46313     5200108013  52001  013   08  001   52  19  5200108  52001      Melilla     Melilla    ES     6     4     0      I  None           Melilla  POLYGON ((505958.610 3902872.793, 505937.912 3...   52006   52001
46314     5200108013  52001  013   08  001   52  19  5200108  52001      Melilla     Melilla    ES     6     4     0      I  None           Melilla  POLYGON ((505958.610 3902872.793, 505937.912 3...   52005   52001
46315     5200108014  52001  014   08  001   52  19  5200108  52001      Melilla     Melilla    ES     6     4     0      I  None           Melilla  POLYGON ((503912.677 3905564.529, 503950.922 3...   52005   52001
46316     5200108015  52001  015   08  001   52  19  5200108  52001      Melilla     Melilla    ES     6     4     0      I  None           Melilla  POLYGON ((505336.020 3904851.043, 505304.845 3...   52006   52001
46317     5200108015  52001  015   08  001   52  19  5200108  52001      Melilla     Melilla    ES     6     4     0      I  None           Melilla  POLYGON ((505336.020 3904851.043, 505304.845 3...   52005   52001

[46318 rows x 21 columns]
```

![limites](https://raw.githubusercontent.com/guicalare/spain.csv/main/codigos%20postales/img/limites.png)

Puedes encontrar el codigo completo en el archivo **[codigos_postales.py](https://github.com/guicalare/spain.csv/blob/main/codigos%20postales/codigos_postales.py)**

## **IMPORTANTE**

La tabla relacional de codigos postales es fiable, pero la base de datos vectorial de los mapas presenta algun que otro dato duplicado.
