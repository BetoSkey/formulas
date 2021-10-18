# Archivo con formulas estadisticas, se diseño con el curso de Estadistica nivel universitario de udemy

import math
import pandas
from collections import Counter
import unittest
from busqueda_binaria import Metodo_binario
from formulas_especiales import ceiling_to_a_number, floor_to_a_number

# FORMULAS ESTADISTICA DESCRIPTIVA UNIVARIADA
def media(datos, agrupados=False, columna=0):
    '''
    Puede recibir:
    
    * lista (valores) = [1, 2, 3, 4]
    
    * diccionario_simple (valores: frecuencias absolutas) = {1:3, 2:1, 3:4}
    
    * diccionario_intervalos ((intervalos):frecuencias absolutas) = {(1,10):3, (10,20):4, (20,30):7}

    * DataFrame de la libreria de pandas:
        - Se debera definir si los datos estan agrupados (default: agrupados=False) y definir el nombre de la columna
        que contiene los datos o las frecuencias acumuladas en caso que aplique (default: columna=0)
    '''
    if type(datos) is pandas.core.series.Series:
            datos = datos.to_list()
    
    if type(datos) is pandas.core.frame.DataFrame:
        
        try:
            if agrupados == True:
                datos = datos.iloc[:,columna].to_dict()
            else:
                datos = datos.iloc[:, columna].to_list()
        except:
            if agrupados == True:
                datos = datos.loc[:,columna].to_dict()
            else:
                datos = datos.loc[:, columna].to_list()

    if type(datos) is dict:

        if type(list(datos)[0]) is tuple:

            sumatoria_ni = 0
            sumatoria_xi_ni = 0
            for intervalo, ni in datos.items():
                sumatoria_ni += ni
                marca_de_clase = (intervalo[0] + intervalo[1]) / 2
                sumatoria_xi_ni += marca_de_clase * ni
            media = sumatoria_xi_ni / sumatoria_ni

        else:
            total_n = sum(datos.values())
            lista_ni_xi = []

            for xi, ni in datos.items():
                lista_ni_xi.append(xi * ni)

            suma_lista_ni_xi = sum(lista_ni_xi)
            media = suma_lista_ni_xi / total_n

    else:
        media = sum(datos) / len(datos)

    return media


def mediana(datos, agrupados=False, columna=0):
    '''Puede recibir:
    
    * lista.- [1, 2, 3...]
    
    * diccionario numeros y frecuencas absolutas.- {1:4, 2:10, 3:30...}
    
    * diccionario intervalos y frecuencias absolutas.- {(1,5):3, (5,10):10, (10,15):20...}

    * DataFrame de la libreria de pandas:
        - Se debera definir si los datos estan agrupados (default: agrupados=False) y definir el nombre de la columna
        que contiene los datos o las frecuencias acumuladas en caso que aplique (default: columna=0)
    '''
    if type(datos) is pandas.core.series.Series:
            datos = datos.to_list()
    
    if type(datos) is pandas.core.frame.DataFrame:
        
        try:
            if agrupados == True:
                datos = datos.iloc[:,columna].to_dict()
            else:
                datos = datos.iloc[:, columna].to_list()
        except:
            if agrupados == True:
                datos = datos.loc[:,columna].to_dict()
            else:
                datos = datos.loc[:, columna].to_list()

    if type(datos) is dict:
        if type(list(datos)[0]) is tuple:
            # Creacion de tabla con marcas de clase y frecuencias absolutas acumuladas
            lista_intervalos = [(intervalo,fa) for intervalo, fa in datos.items()]
            tabla_datos = []
            sumatoria_fa = 0
            
            for intervalo in lista_intervalos:
                
                rango_intervalo = intervalo[0]
                li_intervalo = intervalo[0][0]
                ls_intervalo = intervalo[0][1]
                fa_intervalo = intervalo[1]
                marca_clase = (li_intervalo + ls_intervalo) / 2
                
                sumatoria_fa += fa_intervalo
                faa_intervalo = sumatoria_fa
                
                tabla_datos.append((rango_intervalo, marca_clase ,fa_intervalo, faa_intervalo))
                
            mitad_faa = sumatoria_fa / 2
            
            # Encontrar intervalo de mitad de datos
            index_clase_mediana = 0
            while True:
                if tabla_datos[index_clase_mediana][3] < mitad_faa:
                    index_clase_mediana +=1
                else:
                    clase_mediana = tabla_datos[index_clase_mediana]
                    break
            
            li_clase_mediana = clase_mediana[0][0]
            ls_clase_mediana = clase_mediana[0][1]
            fa_clase_mediana = clase_mediana[2]
            faa_clase_anterior_mediana = 0 if index_clase_mediana == 0 else tabla_datos[(index_clase_mediana-1)][3]
            tamano_intervalo_clase_mediana = ls_clase_mediana - li_clase_mediana
            
            mediana = li_clase_mediana + (((mitad_faa - faa_clase_anterior_mediana) / fa_clase_mediana) * tamano_intervalo_clase_mediana)
            print(f'mediana {mediana} = Li: {li_clase_mediana} + (((total n: {mitad_faa}/2 - faa intervalo mediana anterior: {faa_clase_anterior_mediana}) / ni: {fa_clase_mediana}) * ti: {tamano_intervalo_clase_mediana}')

        else:
            lista_xi_ordenada = Metodo_binario(
                [xi for xi in datos.keys()]).ordenar()
            
            # faa= frecuencias absolutas acumuladas (FAA)
            xi_fa_acumulada = []
            fa_acumulada_list = []

            for xi in lista_xi_ordenada:
                fa_xi = datos[xi]
                if len(xi_fa_acumulada) == 0:
                    xi_fa_acumulada.append((fa_xi, xi))
                    fa_acumulada_list.append(fa_xi)
                else:
                    xi_fa_acumulada.append(
                        (fa_xi + xi_fa_acumulada[-1][0], xi))
                    fa_acumulada_list.append(fa_xi + fa_acumulada_list[-1])
            
            total_n = xi_fa_acumulada[-1][0]
            dict_xi_fa_acumulada = dict(xi_fa_acumulada)
            
            # si n no es par
            if total_n % 2 > 0:
                
                numero_medio = int(round(total_n/2, 0))
                ubicacion_mediana = fa_acumulada_list[Metodo_binario(
                    fa_acumulada_list).ubicacion(numero_medio)+1]
                
                mediana = dict_xi_fa_acumulada[ubicacion_mediana]
            else:
                
                fa_acumulada_list_binaria = Metodo_binario(fa_acumulada_list)
                
                numero_medio1 = int(round(total_n/2, 0)-1)
                
                numero_medio2 = int(round(total_n/2, 0))
                
                ubicacion_numero_medio1 = fa_acumulada_list[fa_acumulada_list_binaria.ubicacion(numero_medio1)]
                
                ubicacion_numero_medio2 = fa_acumulada_list[fa_acumulada_list_binaria.ubicacion(numero_medio2)]
                
                if ubicacion_numero_medio1 == ubicacion_numero_medio2:
                    numero_medio = media([numero_medio1, numero_medio2])
                    ubicacion_mediana = fa_acumulada_list[fa_acumulada_list_binaria.ubicacion(numero_medio)]
                    mediana = dict_xi_fa_acumulada[ubicacion_mediana]
                else:
                    mediana = media([
                        dict_xi_fa_acumulada[ubicacion_numero_medio1], dict_xi_fa_acumulada[ubicacion_numero_medio2]])

    else:
        lista_ordenada = Metodo_binario(datos).ordenar()

        if len(lista_ordenada) % 2 > 0:
            mediana = lista_ordenada[int(
                round(len(lista_ordenada)/2, 0)-1)]
        else:
            numero_medio1 = lista_ordenada[int(
                round(len(lista_ordenada)/2, 0)-1)]
            numero_medio2 = lista_ordenada[int(
                round(len(lista_ordenada)/2, 0))]

            mediana = media([numero_medio1, numero_medio2])

    return mediana


def moda(datos, agrupados=False, columna=0):
    '''Puede recibir:
    
    * lista.- [1, 2, 3...]
    
    * diccionario numeros y frecuencas absolutas.- {1:4, 2:10, 3:30...}
    
    * diccionario intervalos y frecuencias absolutas.- {(1,5):3, (5,10):10, (10,15):20...}

    * DataFrame de la libreria de pandas:
        - Se debera definir si los datos estan agrupados (default: agrupados=False) y definir el nombre de la columna
        que contiene los datos o las frecuencias acumuladas en caso que aplique (default: columna=0)

    ** Si el resultado es mas de 1 moda, regresa una lista de los valores con mayor frecuencia
    '''
    if type(datos) is pandas.core.series.Series:
            datos = datos.to_list()

    if type(datos) is pandas.core.frame.DataFrame:
        
        try:
            if agrupados == True:
                datos = datos.iloc[:,columna].to_dict()
            else:
                datos = datos.iloc[:, columna].to_list()
        except:
            if agrupados == True:
                datos = datos.loc[:,columna].to_dict()
            else:
                datos = datos.loc[:, columna].to_list()

    # Si los datos son un diccionario
    if type(datos) is dict:
        
        # Si los datos son un diccionario con intervalos
        if type(list(datos)[0]) is tuple:
            # Creacion de tabla con marcas de clase y frecuencias absolutas acumuladas
            lista_intervalos = [(intervalo,fa) for intervalo, fa in datos.items()]
            tabla_datos = []
            tabla_fa = []
            sumatoria_fa = 0
            
            for intervalo in lista_intervalos:
                
                index_intervalo = lista_intervalos.index(intervalo)
                rango_intervalo = intervalo[0]
                li_intervalo = intervalo[0][0]
                ls_intervalo = intervalo[0][1]
                fa_intervalo = intervalo[1]
                marca_clase = (li_intervalo + ls_intervalo) / 2
                
                sumatoria_fa += fa_intervalo
                faa_intervalo = sumatoria_fa
                
                tabla_datos.append((rango_intervalo, marca_clase ,fa_intervalo, faa_intervalo))
                
                tabla_fa.append((index_intervalo, fa_intervalo))

            max_fa = max(dict(tabla_fa).values())
            index_intervalo_modal = [index for index, values in dict(tabla_fa).items() if values == max_fa][0]
            intervalo_modal =   tabla_datos[index_intervalo_modal]  
            li_intervalo_modal = intervalo_modal[0][0]
            ls_intervalo_modal = intervalo_modal[0][1]
            fa_intervalo_modal = intervalo_modal[2]
            fa_intervalo_modal_anteror = 0 if index_intervalo_modal == 0 else tabla_datos[(index_intervalo_modal-1)][2]
            fa_intervalo_modal_siguiente = tabla_datos[(index_intervalo_modal+1)][2]
            tamano_intervalo_modal = ls_intervalo_modal - li_intervalo_modal
            
            moda = li_intervalo_modal + (((fa_intervalo_modal - fa_intervalo_modal_anteror) / ((fa_intervalo_modal - fa_intervalo_modal_anteror) + (fa_intervalo_modal - fa_intervalo_modal_siguiente))) * tamano_intervalo_modal)
                
            
        # Si los datos son un diccionario de numeros y frecuencias absolutas
        else:        
            maximo = max(datos.values())
            moda = [id for id, value in datos.items()if value == maximo]

    # Si los datos son una lista
    else:
        conteo_elementos = Counter(datos)
        maximo = max(conteo_elementos.values())
        moda = [id for id, value in conteo_elementos.items()
                if value == maximo]
    # Se analiza si las modas encontradas son mas de 1 regresa una lista o solo 1 regresa un valor
    try:
        if len(moda) == 1:
            moda = moda[0]
    finally:
        return moda


def varianza(datos, agrupados=False, columna=0, muestra=False):
    '''Puede recibir:
    
    * lista.- [1, 2, 3...]
    
    * diccionario numeros y frecuencas absolutas.- {1:4, 2:10, 3:30...}
    
    * diccionario intervalos y frecuencias absolutas.- {(1,5):3, (5,10):10, (10,15):20...}

    * DataFrame de la libreria de pandas:
        - Se debera definir si los datos estan agrupados (default: agrupados=False) y definir el nombre de la columna
        que contiene los datos o las frecuencias acumuladas en caso que aplique (default: columna=0)
    '''
    if type(datos) is pandas.core.series.Series:
            datos = datos.to_list()

    if type(datos) is pandas.core.frame.DataFrame:

        try:
            if agrupados == True:
                datos = datos.iloc[:,columna].to_dict()
            else:
                datos = datos.iloc[:, columna].to_list()
        except:
            if agrupados == True:
                datos = datos.loc[:,columna].to_dict()
            else:
                datos = datos.loc[:, columna].to_list()

    if muestra == False:
        
        
        if type(datos) is dict:
            
            # Si es diccionario de datos agrupados con intervalos
            if type(list(datos)[0]) is tuple:

                # Creacion de tabla con marcas de clase y frecuencias absolutas
                lista_intervalos = [(intervalo,fa) for intervalo, fa in datos.items()]
                tabla_datos = []
                
                for intervalo in lista_intervalos:
                    
                    rango_intervalo = intervalo[0]
                    li_intervalo = intervalo[0][0]
                    ls_intervalo = intervalo[0][1]
                    fa_intervalo = intervalo[1]
                    marca_clase = (li_intervalo + ls_intervalo) / 2
                    
                    tabla_datos.append((marca_clase ,fa_intervalo))
                datos = dict(tabla_datos)
                
            media_dict_xi_fa = media(datos)
            total_n = sum(datos.values())
            xi2_fa = []
            for xi, fa in datos.items():
                xi2_fa.append((xi**2)*fa)
            varianza = (
                (sum(xi2_fa)/total_n) - media_dict_xi_fa**2)

        else:
            media_lista = media(datos)
            diferencias_vs_media = []
            for i in range(len(datos)):
                diferencia = (datos[i] - media_lista)**2
                diferencias_vs_media.append(diferencia)

            varianza = media(diferencias_vs_media)

    else:
        
        if type(datos) is dict:
            media_dict_xi_fa = media(datos)
            total_n = sum(datos.values())-1
            xi2_fa = []
            for xi, fa in datos.items():
                xi2_fa.append((xi**2)*fa)
            varianza = (
                (sum(xi2_fa)/total_n) - media_dict_xi_fa**2)

        else:
            media_lista = media(datos)
            diferencias_vs_media = []
            for i in range(len(datos)):
                diferencia = (datos[i] - media_lista)**2
                diferencias_vs_media.append(diferencia)

            varianza = sum(diferencias_vs_media) / \
                (len(diferencias_vs_media)-1)

    return varianza


def desviacion_estandar(datos, agrupados=False, columna=0, muestra=False):
    '''Puede recibir:
    
    * lista.- [1, 2, 3...]
    
    * diccionario numeros y frecuencas absolutas.- {1:4, 2:10, 3:30...}
    
    * diccionario intervalos y frecuencias absolutas.- {(1,5):3, (5,10):10, (10,15):20...}

    * DataFrame de la libreria de pandas:
        - Se debera definir si los datos estan agrupados (default: agrupados=False) y definir el nombre de la columna
        que contiene los datos o las frecuencias acumuladas en caso que aplique (default: columna=0)
    '''
    
    formula_varianza = varianza(datos, agrupados=agrupados, columna=columna, muestra=muestra)
    desviacion_estandar = formula_varianza ** 0.5

    return desviacion_estandar


def coeficiente_variacion(datos, columna=0, agrupados=False):
    '''
    Porcentaje de la desviacion estandar frente a la media.

    * datos. - Recibe una lista o un DataFrame de pandas
             - Se debera definir el nombre de la columna que contiene los datos o 
               las frecuencias acumuladas en caso que aplique (default: columna=0)

              *ojo* Todos los valores deben ser positivos para poder determinar el coheficiente.

    * columna. - En caso de ser DataFrame se debera definir 
                 el nombre de la columna que contiene los datos. (default: columna=0)
    
    * agrupados. - Bool en caso que los datos esten agrupados. (default: agrupados=0)

    Regresa:
        Coeficiente de variacion.
    
    Interpretacion:
        * Si el coeficiente es ***<= 0.80*** el conjunto de datos es ***homogeneo***, por lo tanto
            la ***media es representativa*** del conjunto de datos.

        * Si el coeficiente es ***> 0.80*** el conjunto de datos es ***heterogeneo***, por lo tanto
            la ***media "no" es representativa*** del conjunto de datos.

    '''
    if agrupados == True:

        s = desviacion_estandar(datos, columna=columna, agrupados=True)
        media_datos = media(datos, columna=columna, agrupados=True)
    
    else:

        s = desviacion_estandar(datos, columna=columna)
        media_datos = media(datos, columna=columna)

    cv = s / media_datos

    return cv


def creacion_intervalos(datos, rango_intervalos):
    '''
    Crea intervalos de los datos proporcionados de acuerdo al rango requerido para los
    intervalos.

    *** solo acepta listas***
    '''
    maximo_numero_en_rangos = ceiling_to_a_number(max(datos), rango_intervalos)
    minimo_numero_en_rangos = floor_to_a_number(min(datos), rango_intervalos)

    distancia_minimo_numero_vs_maximo_numero_en_rangos = maximo_numero_en_rangos - \
        minimo_numero_en_rangos

    cantidad_intervalos = int(
        distancia_minimo_numero_vs_maximo_numero_en_rangos / rango_intervalos)

    intervalos = [[
        minimo_numero_en_rangos,
        minimo_numero_en_rangos + rango_intervalos
    ]]

    for intervalo in range(cantidad_intervalos - 1):
        intervalos.append(
            [intervalos[-1][1], (intervalos[-1][1]) + rango_intervalos])

    return intervalos


def calculo_frecuencias(datos, intervalos=None, rango_intervalos=1, columna=0):
    '''
    Calcula las frecuencias absolutas de intervalos.
    
    * datos.- Acepta lista o DataFrame de la libreria de pandas:
        - Se debera definir el nombre de la columna que contiene los datos(default: columna=0)
    
    * intervalos.- acepta lista de numeros [1, 2, ...] o de intervalos [[1, 2], [2, 3], ...] (intervalos: default=None)

    * rango_intervalos.- Si no se otorga una lista de intervalos, crea intervalos de acuerdo un rango dado (default: rango_intervalos=1)

    * columna.- En caso de ser DataFrame, se debe especifiar el nombre o el numero de la columna que contiene los datos (default: columna=0)

    *** El ultimo numero de cada intervalo no es considerado hasta su siguiente intervalo,
    el ultimo intervalo considera el ultimo numero dentro del intervalo***

     *** Regresa una lista [[intervalo], fa, faa, fr, far]***

    ejemplos:
        calculo_frecuencias([1, 1, 2, 3, 3], intervalos=[1, 2, 3])
            output: [[intervalo], fa, faa, fr, far]
                [(1, 2, 2, 0.4), (2, 1, 3, 0.6), (3, 2, 5, 1.0)]

        calculo_frecuencias([1, 2, 2, 4, 5, 6 , 4, 7 , 8, 10, 10], rango_intervalos=3)
            output: [[intervalo], fa, faa, fr, far]
                [([0, 3], 3, 3, 0.27),
                ([3, 6], 3, 6, 0.55),
                ([6, 9], 3, 9, 0.81),
                ([9, 12], 2, 11, 1.0)]
   
    '''
    if type(datos) is pandas.core.series.Series:
            datos = datos.to_list()

    if type(datos) is pandas.core.frame.DataFrame:
        
        try:

            datos = datos.iloc[:, columna].to_list()
        except:

            datos = datos.loc[:, columna].to_list()

    if intervalos == None:
        intervalos = creacion_intervalos(datos, rango_intervalos)
    
    if type(intervalos[0]) == list:
    
        ultimo_intervalo = intervalos[len(intervalos)-1]
        contar_datos = Counter(datos)
        n = len(datos)
        
        frecuencias = []
        faa = 0
        

        for intervalo in intervalos:
            conteo = 0

            if intervalo == ultimo_intervalo:
                for key, value in contar_datos.items():

                    if key in range(intervalo[0], intervalo[1]+1):
                        conteo += value

            else:

                for key, value in contar_datos.items():

                    if key in range(intervalo[0], intervalo[1]):
                        conteo += value
            
            fa = conteo
            faa += conteo
            fr = fa/n
            far = faa/n

            frecuencias.append((intervalo, fa, faa, fr, far))

        

    else:
        contar_datos = Counter(datos)
        n = len(datos)

        frecuencias = []
        faa = 0
        far = 0

        for intervalo in intervalos:
            conteo = 0
            
            for key, value in contar_datos.items():

                if key == intervalo:
                    conteo += value
            
            fa = conteo
            faa += conteo
            fr = fa/n
            far = faa/n

            frecuencias.append((intervalo, fa, faa, fr, far))

    return frecuencias


def medidas_posicion(datos, k=4, columna=0):
    '''
    Ubica las posiciones para la agrupacion de datos ordenados, si los datos no se encuentran ordenados, los ordena.
    
    Entrada:    -Lista de datos no agrupados (pueden no estar ordenados)
                -DataFrame de la libreria de pandas:
                    Se debera definir el nombre de la columna que contiene los datos (default: columna=0)

    * k.- es la cantidad de divisiones que se requieren, (default "cuartiles": k=4), "deciles": k=10 y "percentiles": k=100

    * columna.- es la columna que contiene los datos en caso de ser un DataFrame de pandas (default: columna=0)

    Salida:     -diccionario {posicion: (ubicacion, valor)}
                                posicion = el nombre de la ubicacion Q=cuartil, D=decil, P=percentil
                                ubicacion = ubicacion de la posicion en la lista ordenada
                                valor = numero que se ecuentra en dicha ubicacion
    '''

    if type(datos) is pandas.core.series.Series:
            datos = datos.to_list()

    if type(datos) is pandas.core.frame.DataFrame:
        
        try:

            datos = datos.iloc[:, columna].to_list()
        except:

            datos = datos.loc[:, columna].to_list()


    n = len(datos)
    if k != 4 and k != 10 and k != 100:
        raise NameError('"k" solo puede ser 4, 10 o 100')

    tipo = 'Q' if k == 4 else 'D' if k == 10 else 'P' if k == 100 else 'error'

    analisis_binario = Metodo_binario(datos)
    datos_ordenados = analisis_binario.ordenar()

    ubicaciones_k = []
    valor_ubicaciones_k = {}

    for q in range(k-1):
        ubicaciones_k.append(
            ((tipo + str(q + 1)), round((((q+1) * (n + 1)) / k) - 1, 3)))

    for i in ubicaciones_k:

        medida_de_posicion = i[0]
        ubicacion = i[1]
        ubicacion_entero = int(ubicacion)
        ubicacion_decimal = ubicacion - int(ubicacion)
        valor_ubicacion_entero = datos_ordenados[ubicacion_entero]
        valor_ubicacion_entero_siguiente = valor_ubicacion_entero if ubicacion_entero == len(
            datos)-1 else datos_ordenados[ubicacion_entero + 1]

        if ubicacion_decimal == 0:
            valor_ubicaciones_k[medida_de_posicion] = (
                ubicacion, round(valor_ubicacion_entero, 3))

        else:
            valor_ubicaciones_k[medida_de_posicion] = (ubicacion, round(
                ((valor_ubicacion_entero_siguiente - valor_ubicacion_entero) * ubicacion_decimal) + valor_ubicacion_entero, 3))

    return valor_ubicaciones_k


def asimetria_bowley(datos):
    '''
    Utiliza la medida de Yule Bowley
    
    Acepta: listade datos no agrupados, pueden estar desordenados

    Regresa: Negativa (<0), Simetrica (=0), Positiva (>0)
    '''
    cuartiles = medidas_posicion(datos, k=4)
    q1 = cuartiles['Q1'][1]
    q2 = cuartiles['Q2'][1]
    q3 = cuartiles['Q3'][1]

    medida_yule_bowley = ((q1 + q3) - (2 * q2)) / (q3 - q1)

    asimetria_bowley = 'Asimetrica negativa' if medida_yule_bowley < 0 else 'Asimetrica positiva' if medida_yule_bowley > 0 else 'Simetrica'

    return asimetria_bowley


def asimetria_pearson(datos, columna=0, agrupados=False):
    '''
    Funcion:
        Calcula la distribucion de los datos por medio del calculo del coeficiente de asimetria de Pearson.

    * datos. - lista o DataFrame de la libreria de pandas:
                "Se debera definir el nombre de la columna que contiene los datos(default: columna=0)"
   
             - diccionario numeros y frecuencas absolutas.- {1:4, 2:10, 3:30...}
            
             - diccionario intervalos y frecuencias absolutas.- {(1,5):3, (5,10):10, (10,15):20...}
    
    * agrupados. - Si los datos estan agrupados (default: agrupados=False)

    Regresa: Coeficiente de Asimetria de Pearson

    Interpretacion del resultado: 
        (< 0 : asimetrica negativa 'hacia izquierda'), (= 0 : simetrica), (> 0 : asimetrica positiva 'hacia derecha')
    
    '''
    
    if agrupados == True:

        media_datos = media(datos, columna=columna, agrupados=True)
        mediana_datos = mediana(datos, columna=columna, agrupados=True)
        desviacion_estandar_datos = desviacion_estandar(datos, columna=columna, agrupados=True)

    else:

        media_datos = media(datos)
        mediana_datos = mediana(datos)
        desviacion_estandar_datos = desviacion_estandar(datos)
    
    asimetria_pearson = (3*(media_datos - mediana_datos)) / desviacion_estandar_datos
    
    return asimetria_pearson


def covarianza(datos, agrupados=False, index_name=None, column_name=None, correlacion=False):
    '''
    Funcion:
        Calcula la relacion entre dos variables de acuerdo a su tendencia

        Si las varibles tienen una tendencia lineal:
            positiva (una crece cuando la otra crece), 
            negativa (una decrece cuando la otra crece)
    
    Parametros:
    * datos. - 
        Puede recibir:
            Para agrupados=False:

                * lista (valores) = [(1, 1), (2, 2) ...(xn, yn)]

                * diccionario (keys: titulos, values: {index:(x o y)n}) = 

                                {titulo1: {1:1, 2:2, 3:3, ... (x)n}, 
                                 titulo2: {1:1, 2:2, 3:3, ... (y)n}}
                                 o
                                {index: [1, 2, 3, ... n],
                                 titulo1: [1, 2, 3, ...n]
                                 titulo2: [1, 2, 3, ...n]}

                * pandas DataFrame:

            Para agrupados=True:

                * diccionario ({'yi': [1, 2, 3 ... n], 
                                'xi': {0: [0, 1, 2 ...n], 
                                       1: [0, 1, 2 ...n], 
                                       2: [0, 1, 2 ...n],
                                       ... n
                                       }})
                
    * agrupados. - si los datos estan agrupados (default: agrupados=False)
    
    * index_name. - si los datos estan agrupados, index_name seria "yi" (default: index_name=None)
    
    * column_name. - si los datos estan agrupados, column_name seria "xi" (default: column_name=None)
    
    
    Interpretacion de resultado:
        > Si covarianza > 0 la relacion es **positiva o directa**  
        > Si covarianza < 0 la relacion es **negativa o inversa**
        
    '''
    if agrupados == False:
    
        if type(datos) == list:
            xi = []
            yi = []
            xiyi = []
            n = len(datos)

            for renglon in datos:
                xi.append(renglon[0])
                yi.append(renglon[1])
                xiyi.append(renglon[0]*renglon[1])

        elif type(datos) == dict:
            xi = list(list(datos.values())[0].values())
            yi = list(list(datos.values())[1].values())
            xiyi = []

            for i in zip(xi,yi):
                xiyi.append(i[0] * i[1])

            n = len(xiyi)

        elif type(datos) is pandas.core.frame.DataFrame:

            xi = datos.iloc[:, 0]
            yi = datos.iloc[:, 1]
            xiyi = datos.iloc[:, 0] * datos.iloc[:, 1]
            n = len(datos)

        media_xi = media(xi)
        media_yi = media(yi)
        suma_xiyi = sum(xiyi)
    
    elif agrupados == True:
        
        if type(datos) == dict:
            datos_df = pandas.DataFrame(data=datos[column_name].values(), index=datos[index_name], columns=datos[column_name].keys())
            datos_df = datos_df.rename_axis('xi',axis=1).rename_axis('yi', axis=0)
            datos_df = datos_df.stack().reset_index()
            datos_df.rename(columns={0: 'ni'}, inplace = True)
            datos_df['xi*ni'] = datos_df['xi'] * datos_df['ni']
            datos_df['yi*ni'] = datos_df['yi'] * datos_df['ni']
            datos_df['xi*yi*ni'] =  datos_df['xi'] * datos_df['yi'] * datos_df['ni']
            
            xini_sum = datos_df['xi*ni'].sum()
            yini_sum = datos_df['yi*ni'].sum()
            
            n = datos_df['ni'].sum()
            suma_xiyi = datos_df['xi*yi*ni'].sum()
            media_xi = xini_sum / n
            media_yi = yini_sum / n
            stdev_xi = desviacion_estandar(datos_df['xi'])
            stdev_yi = desviacion_estandar(datos_df['yi'])

    covarianza = (suma_xiyi / n) - (media_xi * media_yi)
     

    if correlacion == False:
        return covarianza

    if correlacion == True:
        return (covarianza, stdev_xi, stdev_yi)


# FORMULAS PARA GRAFICAR
class Diagrama_caja_bigotes:
    '''
    Calcula informacion para grafica de caja y bigotes:
    
    * datos.- Acepta lista de datos o DataFrame de pandas
    * columna.- En caso de ser DataFrame, seleccionar la columna que contiene los datos (default: columna=0)

    Output:
    
    * datos_ordenados
    * q1 
    * q2
    * q3
    * bigote_inferior
    * bigote_superior
    * rango_intercuartilico
    * barrera_superior
    * barrera_inferior
    * datos_atipicos
    '''

    def __init__(self, datos, columna=0):
        

        if type(datos) is pandas.core.frame.DataFrame:
        
            try:

                self.datos = datos.iloc[:, columna].to_list()
            except:

                self.datos = datos.loc[:, columna].to_list()
        else:
            self.datos = datos

        self.datos_ordenados = Metodo_binario(
            self.datos).ordenar()

        self.n = len(self.datos)

        self.cuartiles = medidas_posicion(self.datos, k=4)

        self.q1 = self.cuartiles['Q1'][1]
        self.q2 = self.cuartiles['Q2'][1]
        self.q3 = self.cuartiles['Q3'][1]

        self.rango_intercuartilico = self.q3 - self.q1

        self.barrera_inferior = self.q1 - (1.5 * self.rango_intercuartilico)
        self.barrera_superior = self.q3 + (1.5 * self.rango_intercuartilico)

        ubicacion_barrera_inferior = 0
        ubicacion_barrera_superior = 1

        while True:
            self.bigote_inferior = self.datos_ordenados[ubicacion_barrera_inferior]
            if self.bigote_inferior < self.barrera_inferior:
                ubicacion_barrera_inferior += 1
            else:
                break

        while True:
            self.bigote_superior = self.datos_ordenados[self.n -
                                                        ubicacion_barrera_superior]
            if self.bigote_superior > self.barrera_superior:
                ubicacion_barrera_superior += 1
            else:
                break

        self.datos_atipicos = [
            i for i in self.datos if i <
            self.barrera_inferior or i > self.barrera_superior
        ]

    def __str__(self):
        return f'''
    Datos ordenados: {self.datos_ordenados}

    Cuartiles = Q1:{self.q1}, Q2:{self.q2}, Q3:{self.q3}
    Bigote inferior = {self.bigote_inferior}
    bigote superior = {self.bigote_superior}

    Rango intercuartilico: {self.rango_intercuartilico}

    Barrera inferior: {self.barrera_inferior}
    Barrera superior: {self.barrera_superior}

    Datos atipicos: {self.datos_atipicos}
            '''

def regresion_lineal_y(x, media_xi, media_yi, covarianza=None, varianza_x=None, n=None, coeficiente_variacion_x=None, coeficiente_variacion_y=None, coeficiente_correlacion=None):
    '''
    Recta de regresion de Y sobre X:    
        Se utiliza para estimar los valores de la Y (dependiente /eje vertical) 
        a partir de los de la X (independiente /eje horizontal). La pendiente de 
        la recta es el cociente entre la covarianza y la varianza de la variable X

    covarianza.-    La covarianza de una variable bidimensional (x, y) es el promedio 
                    de la multiplicacion de las desviaciones de cada una de las variables
                    respecto a sus promedios respectivos; mide la relacion entre las 
                    variables pero presenta como inconveniente el hecho de que su valor 
                    depende de la escala, si son diferentes, entonces puede fallar.

    coeficiente_variacion:  Expresa el porcentaje de variacion de las desviaciones con 
                            respecto a la media.

    coeficiente_correlacion:    La correlacion es igual a la covarianza pero no presenta el 
                                inconveniente de las escalas ya que es relativo osea en 
                                porcentaje.

                                - Si el coeficiente toma valores cercanos a -1 por cada 
                                    aumento de "x", "y" disminuye.
                                - Si el coeficiente toma valores cercanos a 1 por cada 
                                    aumento de "x", "y" aumenta.
                                - Si el coeficiente toma valores cercanos a 0, por cada 
                                    aumento de "x", "y" no aumenta ni disminuye.

    '''
    try:
        if varianza_x != None:
            y = ((covarianza/varianza_x) * x) -((covarianza/varianza_x) * media_xi) + media_yi

        else:
        
            desviacion_estandar_y = media_yi * coeficiente_variacion_y
            desviacion_estandar_x = media_xi * coeficiente_variacion_x
            pendiente_1 = coeficiente_correlacion * (desviacion_estandar_y/desviacion_estandar_x)
            pendiente_0 = media_yi - (pendiente_1 * media_xi)

            y = pendiente_0 + (pendiente_1 * x)
            
    except:
        
        raise ValueError('No fue posible calcularlo, revisa si no hizo falta algun parametro')

    return y

def coeficiente_determinacion(coeficiente_correlacion):
    '''
    Es el porcentaje de confianza del modelo lineal conforme a la realidad, mientras mas se acerque a 1 es mas confiable.
    '''
    determinacion = coeficiente_correlacion ** 2

    return determinacion

# FORMULAS ESTADISTICA DESCRIPTIVA BIVARIADA

def tabla_doble_entrada(dataframe, tipo, totales=True):
    '''
    Crea un dataframe dependiendo el tipo:
        relativa. - Calcula las frecuencias relativas
        marginal. - Calcula las frecuencias marginales
    
    Recibe:
        dataframe.pivot_table

    * dataframe. - dataframe.pivot_table
    * tipo. - relativa o marginal
    * totales. - bool, regresa los totales de las filas y las columnas (default: totales=True)
                        
    Regresa:
        Una copia del dataframe original.
        
    '''
    
    dataframe_copy = dataframe.copy()
    n = dataframe_copy.sum().sum()

    for index in dataframe_copy.index:
        dataframe_copy.loc[index, 'total'] = dataframe_copy.loc[index, : ].sum()
        
    for column in dataframe_copy.columns:
        dataframe_copy.loc['total', column] = dataframe_copy.loc[ : , column].sum()

    
    if tipo == 'relativa':

        for index in dataframe_copy.index:
            
            for column in dataframe_copy.columns:
                
                dataframe_copy.loc[index, column] = dataframe_copy.loc[index, column] / n
    
                                                                     
    elif tipo == 'marginal':

        for index in dataframe_copy.index:
            
            for column in dataframe_copy.columns:
                
                dataframe_copy.loc[index,column] = dataframe_copy.loc[index, column] / dataframe_copy.loc[index, 'total']

    if totales == False:
        dataframe_copy = dataframe_copy.drop('total').drop('total', axis='columns')

    return dataframe_copy
    

def valores_x_y_distribucion_normal(datos):
    '''Regresa listas de "x" y "y" a partir de una datos, para graficar su distribucion normal'''
    media_lista = media(datos)
    sigma_lista = desviacion_estandar(datos)
    valores_x = datos
    valores_y = []

    for i in datos:
        y = (1/(sigma_lista*math.sqrt(2*math.pi))) * \
            math.exp(-1/2*((i-media_lista)/(sigma_lista))**2)
        valores_y.append(y)

    return valores_x, valores_y


# FORMULAS ESTADISTICA INFERENCIAL
def valores_z(datos, valor_a_convertir=None, media_lista=None, sigma=None):
    '''Regresa un diccionario de valrores z, 'z' es el alejamiento de la media en "veces desviacion estandar",
    la formula tambien puede convertir un valor dando la media de datos y sigma.'''

    if valor_a_convertir == None:
        media_lista = media(datos)
        desviacion_estandar_poblacion_lista = desviacion_estandar(datos)
        valores_z = {}

        for i in range(len(datos)):
            valor_z = (datos[i] - media_lista) / \
                desviacion_estandar_poblacion_lista
            valores_z[datos[i]] = round(valor_z, 2)

    else:
        valores_z = round(
            (valor_a_convertir - media_lista) /
            sigma, 2
        )

    return valores_z


def probabilidades_z_distribucion_normal_estandar():
    '''Regresa las probabilidades de z en la distribucion normal estandar'''
    df = pandas.read_csv('../cursos/Estadistica Computacional con Python/Formulas Estadisticas/fdp.csv')
    z = df['z']
    probabilidad = df['prob']
    probabilidades_z = dict(
        [(z[i], probabilidad[i])
            for i in range(len(z))]
    )
    return probabilidades_z


def buscar_z_probabilidad_intermedia(probabilidad):
    '''Busca Z en la tabla de probabilidades de la distribucion normal estandar dada una probabilidad'''
    probabilidad_dns = round(1-((1-probabilidad)/2), 5)
    lista_probabilidades_dns = [
        val for val in probabilidades_z_distribucion_normal_estandar().values()]
    lista_z = {
        val: key for key,
        val in probabilidades_z_distribucion_normal_estandar().items()
    }
    if Metodo_binario(lista_probabilidades_dns).buscar(probabilidad_dns):
        z = lista_z[probabilidad_dns]
    else:
        ubicacion1 = Metodo_binario(
            lista_probabilidades_dns).ubicacion(probabilidad_dns) - 1
        ubicacion2 = Metodo_binario(
            lista_probabilidades_dns).ubicacion(probabilidad_dns)
        z = (
            lista_z[lista_probabilidades_dns[ubicacion1]] +
            lista_z[lista_probabilidades_dns[ubicacion2]]
        ) / 2
    return z


def buscar_z_probabilidad_izquierda(probabilidad):
    '''Busca Z en la tabla de probabilidades de la distribucion normal estandar dada una probabilidad'''
    probabilidad_dns = round(probabilidad, 5)
    lista_probabilidades_dns = [
        val for val in probabilidades_z_distribucion_normal_estandar().values()]
    lista_z = {
        val: key for key,
        val in probabilidades_z_distribucion_normal_estandar().items()
    }

    if Metodo_binario(lista_probabilidades_dns).buscar(probabilidad_dns):
        z = lista_z[probabilidad_dns]

    else:
        ubicacion1 = Metodo_binario(
            lista_probabilidades_dns).ubicacion(probabilidad_dns) - 1

        ubicacion2 = Metodo_binario(
            lista_probabilidades_dns).ubicacion(probabilidad_dns)

        z = (
            lista_z[lista_probabilidades_dns[ubicacion1]] +
            lista_z[lista_probabilidades_dns[ubicacion2]]
        ) / 2

    return z


def buscar_z_probabilidad_derecha(probabilidad):
    '''Busca Z en la tabla de probabilidades de la distribucion normal estandar dada una probabilidad'''
    probabilidad_dns = round((1-probabilidad), 5)

    lista_probabilidades_dns = [
        val for val in probabilidades_z_distribucion_normal_estandar().values()]

    lista_z = {
        val: key for key,
        val in probabilidades_z_distribucion_normal_estandar().items()
    }

    if Metodo_binario(lista_probabilidades_dns).buscar(probabilidad_dns):
        z = lista_z[probabilidad_dns]

    else:
        ubicacion1 = Metodo_binario(
            lista_probabilidades_dns).ubicacion(probabilidad_dns) - 1

        ubicacion2 = Metodo_binario(
            lista_probabilidades_dns).ubicacion(probabilidad_dns)

        z = (
            lista_z[lista_probabilidades_dns[ubicacion1]] +
            lista_z[lista_probabilidades_dns[ubicacion2]]
        ) / 2

    return round(z, 3)


class Pruebas_caja_cristal(unittest.TestCase):

    def test_media_lista(self):
        formula_media = round(media(analisis_lista), 2)

        self.assertEqual(formula_media, 69.86)

    def test_media_diccionario(self):
        formula_media = round(media(analisis_dict), 2)

        self.assertEqual(formula_media, 7.8)

    def test_mediana(self):
        formula_mediana = mediana(analisis_lista)

        self.assertEqual(formula_mediana, 70)

    def test_mediana_datos_agrupados(self):
        formula_mediana = mediana(analisis_dict)

        self.assertEqual(formula_mediana, 8)

    def test_moda(self):
        analisis_lista.append(70)
        formula_moda = moda(analisis_lista)

        try:
            self.assertEqual(formula_moda, 70)
        finally:
            analisis_lista.remove(70)

    def test_muchas_modas(self):
        analisis_lista.append(70)
        analisis_lista.append(82)
        formula_moda = moda(analisis_lista)
        try:
            self.assertEqual(formula_moda, [82, 70])
        except:
            self.assertEqual(formula_moda, [70, 82])
        finally:
            analisis_lista.remove(70)
            analisis_lista.remove(82)

    def test_varianza(self):
        formula_varianza = round(varianza(analisis_lista), 2)

        self.assertEqual(formula_varianza, 122.69)

    def test_varianza_muestral(self):
        formula_varianza = round(
            varianza(analisis_lista, muestra=True), 2)

        self.assertEqual(formula_varianza, 143.14)

    def test_varianza_datos_agrupados(self):
        formula_varianza = round(varianza(analisis_dict), 3)

        self.assertEqual(formula_varianza, 0.8)

    def test_varianza_muestral_datos_agrupados(self):
        formula_varianza = round(
            varianza(analisis_dict, muestra=True), 3)

        self.assertEqual(formula_varianza, 2.058)

    def test_desviacion_estandar(self):
        formula_desviacion_estandar = round(
            desviacion_estandar(analisis_lista), 2)

        self.assertEqual(formula_desviacion_estandar, 11.08)

    def test_desviacion_estandar_datos_agrupados(self):
        formula_desviacion_estandar = round(
            desviacion_estandar(analisis_dict), 4)

        self.assertEqual(formula_desviacion_estandar, 0.8944)

    def test_desviacion_estandar_muestral(self):
        formula_desviacion_estandar = round(
            desviacion_estandar(analisis_lista, muestra=True), 4)

        self.assertEqual(formula_desviacion_estandar, 11.9642)

    def test_desviacion_estandar_muestral_datos_agrupados(self):
        formula_desviacion_estandar = round(
            desviacion_estandar(analisis_dict, muestra=True), 4)

        self.assertEqual(formula_desviacion_estandar, 1.4346)

    def test_coeficiente_variacion(self):
        formula_coeficiente_variacion = coeficiente_variacion(analisis_lista)

        self.assertEqual(round(formula_coeficiente_variacion, 3), 0.159)

    def test_creacion_intervalos(self):
        formula_creacion_intervalos = creacion_intervalos(analisis_lista2, 5)

        self.assertEqual(formula_creacion_intervalos, [
            [50, 55], [55, 60], [60, 65], [65, 70], [70, 75], [75, 80], [80, 85]
        ])

    def test_calculo_frecuencias(self):
        formula_calculo_frecuencias = calculo_frecuencias(
            analisis_lista2, rango_intervalos=5)

        self.assertEqual(formula_calculo_frecuencias, [
            ([50, 55], 2, 2, 0.025, 0.025), ([55, 60], 7, 9, 0.0875, 0.1125), ([
                60, 65], 17, 26, 0.2125, 0.325), ([65, 70], 30, 56, 0.375, 0.7),
            ([70, 75], 14, 70, 0.175, 0.875), ([75, 80], 7, 77, 0.0875, 0.9625), ([80, 85], 3, 80, 0.0375, 1.0)
        ])

    def test_medidas_posicion(self):
        formula_medidas_posicion = medidas_posicion(analisis_lista)

        self.assertEqual(
            formula_medidas_posicion, {'Q1': (1.0, 59), 'Q2': (3.0, 70), 'Q3': (5.0, 82)})

    def test_rango_intercuartilico(self):
        formula_rango_intercuartilico = Diagrama_caja_bigotes(
            analisis_lista).rango_intercuartilico

        self.assertEqual(formula_rango_intercuartilico, 23)

    def test_asimetria(self):
        formula_asimetria = asimetria_bowley(analisis_lista)

        self.assertEqual(formula_asimetria, 'Asimetrica positiva')

    def test_valor_z_muchos_datos(self):
        formula_valor_z = valores_z(analisis_lista)

        self.assertEqual(
            formula_valor_z, {
                55: -1.34, 87: 1.55, 74: 0.37, 70: 0.01, 82: 1.1, 62: -0.71, 59: -0.98}
        )

    def test_valor_z_un_dato(self):
        valor_a_convertir = 55
        formula_valor_z = valores_z(analisis_lista,
                                    valor_a_convertir=valor_a_convertir, media_lista=69.86, sigma=11.08)

        self.assertEqual(formula_valor_z, -1.34)

    def test_valores_x_y_distribucion_normal(self):
        formula_valores_x_y_distribucion_normal = valores_x_y_distribucion_normal(analisis_lista)[
            1]

        self.assertEqual(
            formula_valores_x_y_distribucion_normal, [
                0.014649940215369783, 0.010873903333325743, 0.03358323798357501, 0.028005203898067346, 0.02227796183372684, 0.03601326534529145, 0.01974872533379657]
        )

    def test_probabilidades_z_distribucion_normal_estandar(self):
        probabilidades_z = probabilidades_z_distribucion_normal_estandar()

        self.assertEqual(probabilidades_z[2.71], 0.9966)

    def test_buscar_z_probabilidad_intermedia(self):
        probabilidad = 0.9966
        formula_buscar_z_probabilidad_intermedia = buscar_z_probabilidad_intermedia(
            probabilidad)

        self.assertEqual(formula_buscar_z_probabilidad_intermedia, 2.93)

    def test_buscar_z_probabilidad_izquierda(self):
        probabilidad = 0.9115
        formula_buscar_z_probabilidad_izquierda = buscar_z_probabilidad_izquierda(
            probabilidad)

        self.assertEqual(formula_buscar_z_probabilidad_izquierda, 1.35)

    def test_buscar_z_probabilidad_derecha(self):
        probabilidad = 0.9115
        formula_buscar_z_probabilidad_derecha = buscar_z_probabilidad_derecha(
            probabilidad)

        self.assertEqual(formula_buscar_z_probabilidad_derecha, -1.35)


# INFORMACION PARA PRUEBAS
if '__main__' == __name__:

    analisis_lista = [55, 87, 74, 70, 82, 62, 59]

    analisis_dict = dict(
        [(6, 3), (7, 16), (8, 20), (9, 10), (10, 1)]
    )

    analisis_lista2 = [
        60, 66, 77, 70, 66, 68, 57, 70, 66, 52, 75, 65, 69, 71, 58, 66, 67, 74,
        61, 63, 69, 80, 59, 66, 70, 67, 78, 75, 64, 71, 81, 62, 64, 69, 68, 72,
        83, 56, 65, 74, 67, 54, 65, 65, 69, 61, 67, 73, 57, 62, 67, 68, 63, 67,
        71, 68, 76, 61, 62, 63, 76, 61, 67, 67, 64, 72, 64, 73, 79, 58, 67, 71,
        68, 59, 69, 70, 66, 62, 63, 66
    ]

    unittest.main()
