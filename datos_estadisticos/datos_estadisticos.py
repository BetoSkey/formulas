'Estoy en branch creacion_tabla_estadistica'
import pandas
from IPython.core.display import display, HTML
from statistics import mean, median_grouped, median_high, variance, stdev, mode, multimode, quantiles, pvariance, pstdev

from pandas.core import indexing
from formulas_especiales import ceiling_to_a_number, floor_to_a_number

class DatosEstadisticos:

    def __init__(self, datos, titulo, repr_xi, repr_fa, agrupados=False, columna_xi=0, columna_fa=0, xi_es_index=False, muestra=True):
        

        if type(datos) == list:
            self.datos = pandas.DataFrame(datos)
        
        elif type(datos) == dict:
            self.datos = pandas.Series(datos, name=repr_xi)
            self.datos = pandas.DataFrame(self.datos)
            self.datos[repr_fa] = self.datos.index
            self.datos = self.datos.reset_index(drop=True)
            self.datos.set_index(repr_fa, inplace=True)

        elif type(datos) == pandas.Series:
            self.datos = datos.to_frame()
        
        else:
            self.datos = datos
        
        if xi_es_index == True:
            self.datos.reset_index(inplace= True)
            columna_fa = 1
            xi_es_index = False
        
        self.titulo = titulo
        self.agrupados = agrupados
        self.repr_xi = repr_xi
        self.columna_xi = columna_xi
        self.repr_fa = repr_fa
        self.columna_fa = columna_fa
        self.xi_es_index = xi_es_index
        self.muestra = muestra


        nombre_columnas = self.__obtener_nombre_columnas__()
        self.nombre_columna_xi = nombre_columnas['xi']
        self.nombre_columna_fa = nombre_columnas['fa']

        if self.xi_es_index:
            self.datos = self.datos.reset_index()
            self.xi_es_index = False


        datos_xi_ni = self.__obtener_datos_ni_xi__()
        self.xi_ni = datos_xi_ni
        self.xi = datos_xi_ni.iloc[:,0]
        self.fa = datos_xi_ni.iloc[:,1]

        self.__ordenar_datos__()

        self.total_n = self.__total_n__()

    def __ordenar_datos__(self):

        if self.xi_es_index == True:
            self.datos.sort_index(inplace=True)

        else:
            self.datos.sort_values(self.nombre_columna_xi, inplace=True)

    def __obtener_nombre_columnas__(self):
        '''
        Funcion.-   Obtiene el nombre de las columnas xi y fa de un DataFrame para futuras referencias en 
                    formulas estadisticas   
        Input:
            dataframe
        Output:
            (nombre columna "xi", nombre columna "fa")
        '''

        type_xi = type(self.columna_xi)
        type_fa = type(self.columna_fa)
        
        #------- obtenemos nombre de columna "xi" -------
        # Si "xi" esta en el index
        if self.xi_es_index == True:
            columna_xi_name = self.datos.index.name

        else:
            # Si "xi" no esta en el index
            # Si "xi" es string
            if type_xi == str:
                columna_xi_name = self.columna_xi
            
            # Si "xi" no esta en el index
            # Si "xi" es un numero
            else:
                columna_xi_name = self.datos.iloc[:,self.columna_xi].name

        #------- obtenemos nombre de columna "fa" -------
        # Si "fa" es string
        if type_fa == str:
            columna_fa_name = self.columna_fa

        # Si "fa" es un numero
        else:
            columna_fa_name = self.datos.iloc[:,self.columna_fa].name

        return {'xi':columna_xi_name, 'fa':columna_fa_name}    
   
    def __total_n__(self):

        if self.agrupados == False:
            total_n = len(self.xi)
        
        else:
            total_n = self.fa.sum()

        return total_n

    def __obtener_datos_ni_xi__(self):
        
        if self.xi_es_index == True:
            
            xi_ni = self.datos.reset_index().loc[: , [self.nombre_columna_xi, self.nombre_columna_fa]]
                
        else:

            xi_ni = self.datos.loc[: , [self.nombre_columna_xi, self.nombre_columna_fa]]
            
        return xi_ni

    def __creacion_intervalos__(self, rango_intervalos):
        '''
        Crea intervalos de los datos proporcionados de acuerdo al rango requerido para los
        intervalos.

        *** solo acepta listas***
        '''
        maximo_numero_en_rangos = ceiling_to_a_number(max(self.xi), rango_intervalos)
        minimo_numero_en_rangos = floor_to_a_number(min(self.xi), rango_intervalos)

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

    def __calculo_frecuencias_absolutas__(self, rango_intervalos):
        contar_datos = self.xi.value_counts().reset_index()
        contar_datos.columns = ['xi', 'fa']
        n = self.total_n

        intervalos = pandas.Series(self.__creacion_intervalos__(rango_intervalos), name='intervalos')
        ultimo_intervalo = intervalos[len(intervalos)-1]

        frecuencias = []

        for intervalo in intervalos:
            conteo = 0
            
            if intervalo == ultimo_intervalo:

                intervalo_inferior = intervalo[0]
                intervalo_superior = intervalo[1] +1
            else:
                intervalo_inferior = intervalo[0]
                intervalo_superior = intervalo[1]

            #recorriendo el index
            for i in range(len(contar_datos)):
              
                xi = contar_datos.iloc[i][0]
                fa = contar_datos.iloc[i][1]
    
                if xi in range(intervalo_inferior, intervalo_superior):
                    conteo += fa
            
            total_fa = conteo

            #frecuencias.append((intervalo, total_fa))
            frecuencias.append((total_fa))

            #frecuencias_series = pandas.Series(frecuencias, name=self.nombre_columna_xi)
            frecuencias_series = pandas.Series(frecuencias, name='fa')

            tabla_intervalos_frecuencias = pandas.concat([intervalos, frecuencias_series], axis=1)

        return tabla_intervalos_frecuencias

    def convertir_a_intervalos(self, rango_intervalos):
        datos_intervalos = self.__calculo_frecuencias_absolutas__(rango_intervalos)
        
        self.datos = datos_intervalos
        self.columna_xi = 'intervalos'
        self.nombre_columna_xi = 'intervalos'
        self.xi.name = 'intervalos'
        self.columna_fa = 'fa'
        self.fa.name = 'fa'
        self.nombre_columna_fa = 'fa'
        self.agrupados = True

    def _repr_html_(self):
        if self.agrupados == False:
            return f'''
            <body>
                <h1>
                    {self.titulo}
                </h1>

                <p align="left">
                    <pre><strong><span style="font-size:110%">{'Datos Agrupados' if self.agrupados ==True else 'Datos No Agrupados'}</span></strong></br></pre>
                    <pre>Total n: <strong><span style="font-size:110%">{self.total_n}</span></strong> {self.repr_fa}</br></pre>
                </p>

                <table border="1" align="center" cellspacing="0" cellpadding="5">
                    <tr valign="bottom" align="center">
                        <th width="300"><pre><span style="font-size:110%">Variable Aleatoria (Xi)</span></br></pre></pre></th>
                        <th width="300"><pre><span style="font-size:110%">Elementos (ni)</span></br></pre></pre></th>	
                    </tr>
                    <tr>
                        <td>
                            <table border="1" align="center" cellspacing="0" cellpadding="5"  width="300"  height="20">
                                <tr>
                                <td> Representa:</td>
                                <td><strong> {self.repr_xi}</strong></td>
                                </tr>
                                <tr>
                                <td> Columna Xi:</td>
                                <td><strong> {self.nombre_columna_xi}</strong></td>
                                </tr>
                            </table>
                        </td>
                        <td>
                            <table border="1" align="center" cellspacing="0" cellpadding="5"  width="300"  height="20">
                               <tr>
                                <td>Representa:</td>
                                <td><strong> {self.repr_fa}</strong></td>
                                </tr>
                            </table>
                        </td>	
                    </tr>
                    <tr>
                    </table>
            </body>
            {self.datos._repr_html_()}
            '''

        else:
            return f'''
            <body>
                <h1>
                    {self.titulo}
                </h1>

                <p align="left">
                    <pre><strong><span style="font-size:110%">{'Datos Agrupados' if self.agrupados ==True else 'Datos No Agrupados'}</span></strong></br></pre>
                    <pre>Total n: <strong><span style="font-size:110%">{self.total_n}</span></strong> {self.repr_fa}</br></pre>
                </p>

                <table border="1" align="center" cellspacing="0" cellpadding="5">
                    <tr valign="bottom" align="center">
                        <th width="300"><pre><span style="font-size:110%">Variable Aleatoria (Xi)</span></br></pre></pre></th>
                        <th width="300"><pre><span style="font-size:110%">Elementos (Fa/ni)</span></br></pre></pre></th>	
                    </tr>
                    <tr>
                        <td>
                            <table border="1" align="center" cellspacing="0" cellpadding="5"  width="300"  height="20">
                                <tr>
                                <td> Representa:</td>
                                <td><strong> {self.repr_xi}</strong></td>
                                </tr>
                                <tr>
                                <td> Columna Xi:</td>
                                <td><strong> {self.nombre_columna_xi}</strong></td>
                                </tr>
                            </table>
                        </td>
                        <td>
                            <table border="1" align="center" cellspacing="0" cellpadding="5"  width="300"  height="20">
                               <tr>
                                <td> Representa:</td>
                                <td><strong> {self.repr_fa}</strong></td>
                                </tr>
                                <tr>
                                <td> Columna Fa:</td>
                                <td><strong> {self.nombre_columna_fa}</strong></td>
                                </tr>
                            </table>
                        </td>	
                    </tr>
                    <tr>
                    </table>
            </body>
            {self.datos._repr_html_()}'''



class AnalisisEstadistico:
    
    def __init__(self, datos, titulo=None, repr_xi=None, repr_fa=None, agrupados=False, columna_xi=0, columna_fa=0, xi_es_index=False, muestra=True):
        
        if type(datos) == DatosEstadisticos:
            
            self.__datos__ = datos.datos
            self.__titulo__ = datos.titulo
            self.__agrupados__ = datos.agrupados
            self.__repr_xi__ = datos.repr_xi
            self.__columna_xi__ = datos.columna_xi
            self.__repr_fa__ = datos.repr_fa
            self.__columna_fa__ = datos.columna_fa
            self.__xi_es_index__ = datos.xi_es_index
            self.__muestra__ = datos.muestra

        else:

            if type(datos) == list:

                self.__datos__ = pandas.DataFrame(datos)

            elif type(datos) == pandas.Series:

                self.__datos__ = datos.to_frame()
            
            else:
                self.__datos__ = datos

            if xi_es_index == True:
                self.__datos__.reset_index(inplace= True)
                columna_fa = 1
                xi_es_index = False


            self.__titulo__ = titulo
            self.__agrupados__ = agrupados
            self.__repr_xi__ = repr_xi
            self.__columna_xi__ = columna_xi
            self.__repr_fa__ = repr_fa
            self.__columna_fa__ = columna_fa
            self.__xi_es_index__ = xi_es_index
            self.__muestra__ = muestra

        self.tabla_estadistica = self.__datos__.reset_index().copy() if self.__xi_es_index__ == True else self.__datos__.copy()
        self.__xi_es_index__ = False


        nombre_columnas = self.__obtener_nombre_columnas__()
        self.__nombre_columna_xi__ = nombre_columnas['xi']
        self.__nombre_columna_fa__ = nombre_columnas['fa']
        
        
        datos_xi_ni = self.__obtener_datos_ni_xi__()
        self.__xi_ni__ = datos_xi_ni
        self.__xi__ = datos_xi_ni.iloc[:,0]
        self.__fa__ = datos_xi_ni.iloc[:,1]
        self.fa = self.__fa__

        self.__total_n__ = self.__total_n__()

        frecuencias_acumuladas = self.__calculo_frecuencias_acumuladas__()
        self.__faa__ = frecuencias_acumuladas['faa']
        self.__fr__ = frecuencias_acumuladas['fr']
        self.__fra__ = frecuencias_acumuladas['fra']

        self.__mc__ = self.__calculo_marcas_clase__()
        self.__xi2__ = self.__obtener_xi2__()

        columnas_ni_por_xi = self.__calcular_columna_ni_por_xi__()
        self.__ni_xi__ = columnas_ni_por_xi[0]
        self.__ni_xi2__ = columnas_ni_por_xi[1]

        self.__ordenar_datos__()

    def __ordenar_datos__(self):

        if self.__xi_es_index__ == True:
            self.tabla_estadistica.sort_index(inplace=True)

        else:
            self.tabla_estadistica.sort_values(self.__nombre_columna_xi__, inplace=True)

    def __obtener_nombre_columnas__(self):
        '''
        Funcion.-   Obtiene el nombre de las columnas xi y fa de un DataFrame para futuras referencias en 
                    formulas estadisticas   
        Input:
            dataframe
        Output:
            (nombre columna "xi", nombre columna "fa")
        '''

        type_xi = type(self.__columna_xi__)
        type_fa = type(self.__columna_fa__)
        
        #------- obtenemos nombre de columna "xi" -------
        # Si "xi" esta en el index
        if self.__xi_es_index__ == True:
            columna_xi_name = self.tabla_estadistica.index.name

        else:
            # Si "xi" no esta en el index
            # Si "xi" es string
            if type_xi == str:
                columna_xi_name = self.__columna_xi__
            
            # Si "xi" no esta en el index
            # Si "xi" es un numero
            else:
                columna_xi_name = self.tabla_estadistica.iloc[:,self.__columna_xi__].name

        #------- obtenemos nombre de columna "fa" -------
        # Si "fa" es string
        if type_fa == str:
            columna_fa_name = self.__columna_fa__

        # Si "fa" es un numero
        else:
            columna_fa_name = self.tabla_estadistica.iloc[:,self.__columna_fa__].name

        return {'xi':columna_xi_name, 'fa':columna_fa_name}

    def __creacion_intervalos__(self, rango_intervalos):
        '''
        Crea intervalos de los datos proporcionados de acuerdo al rango requerido para los
        intervalos.

        *** solo acepta listas***
        '''
        maximo_numero_en_rangos = ceiling_to_a_number(max(self.__xi__), rango_intervalos)
        minimo_numero_en_rangos = floor_to_a_number(min(self.__xi__), rango_intervalos)

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

    def __calculo_frecuencias_absolutas__(self, rango_intervalos):
        contar_datos = self.__xi__.value_counts().reset_index()
        n = self.__total_n__

        intervalos = pandas.Series(self.__creacion_intervalos__(rango_intervalos), name='intervalos')
        ultimo_intervalo = intervalos[len(intervalos)-1]

        frecuencias = []

        for intervalo in intervalos:
            conteo = 0
            
            if intervalo == ultimo_intervalo:

                intervalo_inferior = intervalo[0]
                intervalo_superior = intervalo[1] +1
            else:
                intervalo_inferior = intervalo[0]
                intervalo_superior = intervalo[1]

            #recorriendo el index
            for i in range(len(contar_datos)):
              
                xi = contar_datos.iloc[i][0]
                fa = contar_datos.iloc[i][1]
    
                if xi in range(intervalo_inferior, intervalo_superior):
                    conteo += fa
            
            total_fa = conteo

            #frecuencias.append((intervalo, total_fa))
            frecuencias.append((total_fa))

            frecuencias_series = pandas.Series(frecuencias, name=self.__nombre_columna_xi__)

            tabla_intervalos_frecuencias = pandas.concat([intervalos, frecuencias_series], axis=1)

        return tabla_intervalos_frecuencias

    def convertir_a_intervalos(self, rango_intervalos):
        datos = self.__calculo_frecuencias_absolutas__(rango_intervalos)
        #self.__init__(datos, self.__titulo__, columna_xi='intervalos', columna_fa=self.__columna_fa__, agrupados=True)
        
        return datos

    def __es_rango__(self):
        
        xi = self.__xi__
        
        try:
            es_rango = True if (type(xi.iloc[0]) is list or type(xi.iloc[0]) is tuple) else False

        except:
            es_rango = True if (type(xi[0]) is list or type(xi[0]) is tuple) else False

        return es_rango

    def __total_n__(self):

        if self.__agrupados__ == False:
            total_n = len(self.__xi__)
        
        else:
            total_n = self.__fa__.sum()

        return total_n

    def __obtener_datos_ni_xi__(self):
        
        if self.__xi_es_index__ == True:
            
            xi_ni = self.tabla_estadistica.reset_index().loc[: , [self.__nombre_columna_xi__, self.__nombre_columna_fa__]]
                
        else:

            xi_ni = self.tabla_estadistica.loc[: , [self.__nombre_columna_xi__, self.__nombre_columna_fa__]]
            
        return xi_ni

    def __obtener_xi2__(self):

        if self.__agrupados__ == False:
            xi2 = None
        
        else:
            es_rango = self.__es_rango__()

            xi = self.__xi__
            mc = self.__mc__

            if es_rango:
                xi2 = self.tabla_estadistica['xi2'] = mc ** 2
            
            else:
                xi2 = self.tabla_estadistica['xi2'] = xi ** 2
        
        return xi2

    def __calcular_columna_ni_por_xi__(self):

        if self.__agrupados__ == True:
            if self.__mc__ is not None:
                self.tabla_estadistica['ni*xi'] = self.__mc__ * self.__fa__
                
            else:
                self.tabla_estadistica['ni*xi'] = self.__xi__ * self.__fa__
            
            self.tabla_estadistica['ni*xi2'] = self.__xi2__ * self.__fa__

            ni_xi = self.tabla_estadistica['ni*xi']
            ni_xi2 = self.tabla_estadistica['ni*xi2']
        else:
            ni_xi = None   
            ni_xi2 = None

        return (ni_xi, ni_xi2)

    def __marca_clase__(self, rango):
        '''
        Funcion:
            Calcula la marca de clase de un rango
        
        Input:
            recibe lista o tupla de "dos" valores.
            
            ejemplo: [1, 2] o (1, 2)
        
        Output:
            marca_clase
            
        '''
        
        if len(rango) ==2:
            
            marca_clase = (rango[0] + rango[1]) / 2
            
            return marca_clase
        
        else:
            raise ValueError('Solo se aceptan dos valores como rango!')

    def __calculo_marcas_clase__(self):
        '''
        Funcion:
            Calcula las marcas de clase cuando los datos estan agrupados por intervalos
        '''

        xi = self.__xi__
        
        es_rango = self.__es_rango__()
        
        if es_rango:

            self.tabla_estadistica['marca clase'] = xi
            
            self.tabla_estadistica['marca clase'] = self.tabla_estadistica['marca clase'].apply(self.__marca_clase__)

            marcas_de_clase = self.tabla_estadistica['marca clase']

        else:
            marcas_de_clase = None
        
        return marcas_de_clase

    def __calculo_frecuencias_acumuladas__(self):
        
        fa = self.__fa__
        total_n = self.__total_n__
        
        
        if self.__agrupados__ == False:
            faa = None
            fr = None
            fra = None

        else:
            faa = self.tabla_estadistica['faa'] = fa.cumsum()
            fr = self.tabla_estadistica['fr'] = fa / total_n
            fra = self.tabla_estadistica['fra'] = fr.cumsum()

        return {'faa': faa, 'fr': fr, 'fra': fra}

    def __encontrar_index_mediana_datos_agrupados__(self):
        
        mitad_faa = self.__total_n__ / 2

        index_clase_mediana = 0
        
        while True:
            if self.tabla_estadistica.iloc[index_clase_mediana].loc['faa'] < mitad_faa:
                index_clase_mediana +=1
            else:
                clase_mediana = index_clase_mediana
                break

        return clase_mediana

    def __encontrar_index_cuantil_datos_agrupados__(self, n):
        '''
        n = total de cuantiles
        N = total de frecuencias absolutas
        '''

        N = self.__total_n__

        dict_index_cuantiles = {}

        for k in range(0,n):

            cuantil_a_buscar = (N * k) / n

            index_clase_cuantil = 0
            
            while True:
                if self.tabla_estadistica.iloc[index_clase_cuantil].loc['faa'] < cuantil_a_buscar:
                    index_clase_cuantil +=1
                else:
                    break
            
            dict_index_cuantiles['index_Q' + str(k)] = index_clase_cuantil

        return dict_index_cuantiles

    def __sumatoria_xi_menos_media_por_ni_al_cubo__(self, dataframe, media):

        xi = dataframe[0]
        ni = dataframe[1]

        resultado = ((xi - media)** 3) * ni

        return resultado 

    def __medida_fisher_datos_agrupados__(self):
        es_rango = self.__es_rango__()
        N = self.__total_n__
        s = self.desviacion_estandar
        
        if es_rango == True:
            print('formula medida_fisher_datos_agrupados para rango')
            fisher = self.tabla_estadistica[['marca clase', self.__nombre_columna_fa__]].apply(self.__sumatoria_xi_menos_media_por_ni_al_cubo__, args=[self.media], axis='columns')
        
        else:
            print('formula medida_fisher_datos_agrupados Sin rango')
            fisher = self.tabla_estadistica[[self.__nombre_columna_xi__, self.__nombre_columna_fa__]].apply(self.__sumatoria_xi_menos_media_por_ni_al_cubo__, args=[self.media], axis='columns')
            
        fisher = sum(fisher) / (N * (s ** 3))
            
        return fisher

    @property
    def media(self):
            
        xi = self.__xi__
        ni = self.__fa__

        if self.__agrupados__ == False:

            media = xi.mean()

        else:
            
            #Si los datos estan agrupados por rangos
            if self.__mc__ is not None:
                xi = self.__mc__

            
            sumatoria_ni = ni.sum()
            sumatoria_ni_xi = (xi * ni).sum()

            media = sumatoria_ni_xi / sumatoria_ni
        
        return media

    @property
    def mediana(self):
        
        # Datos no agrupados
        if self.__agrupados__ == False:

            mediana = self.__fa__.median()

        # Datos agrupados
        else:

            total_n = self.__total_n__
            mitad_faa = total_n/2
            es_rango = self.__es_rango__()

            index_mediana = self.__encontrar_index_mediana_datos_agrupados__()

            
            
            # xi "no" son rango
            if es_rango == False:
                
                if self.__xi_es_index__ == True:
                    mediana = self.tabla_estadistica.index[index_mediana]
                
                else:
                    mediana = self.tabla_estadistica.iloc[index_mediana][self.__nombre_columna_xi__]
            
            
            # xi son rangos
            else:

                #iloc_mediana = self.tabla_estadistica.index.get_loc(index_mediana)

                # Se obteiene el intervalo de la mediana si esta en el index
                if self.__xi_es_index__ == True:
                    intervalo_mediana = self.tabla_estadistica.index[index_mediana]
                    
                # Se obtiene el intevalo de la mediana si esta en las columnas
                else:
                    intervalo_mediana = self.tabla_estadistica.iloc[index_mediana][self.__nombre_columna_xi__]
                    
                # Limite inferior y superior del intervalo de la mediana
                Li = intervalo_mediana[0]
                
                Ls = intervalo_mediana[1]
                

                # Frecuencia absoluta acumulada del intervalo de la mediana anterior
                faa_intervalo_mediana_anterior = self.tabla_estadistica.iloc[index_mediana-1].loc['faa']
                
                # Frecuencia absoluta del intervalo de la mediana
                ni = self.tabla_estadistica.iloc[index_mediana].loc[self.__nombre_columna_fa__]
                
                # Tamano del intervalo de la mediana
                ti = Ls - Li
                

                # Formula de mediana para datos agrupados por intervalos / rangos
                mediana = Li + (((mitad_faa) - faa_intervalo_mediana_anterior) / ni) * ti
                
        return mediana

    @property
    def moda(self, multimoda=False):

        # Datos No Agrupados
        if self.__agrupados__ == False:
            if multimoda == False:
                moda = mode(self.__xi__)
            
            else:
                moda = multimode(self.__xi__)

        # Datos Agrupados
        else:

            es_rango = self.__es_rango__()
            moda_fa = max(self.__fa__)

            mask1 = self.tabla_estadistica[self.__nombre_columna_fa__] == moda_fa

            index_moda = self.tabla_estadistica[mask1].index[0]
            iloc_moda = self.tabla_estadistica.index.get_loc(index_moda)

            # Si "xi" no son intervalos/rangos
            if es_rango == False:
                if self.__xi_es_index__ == True:
                    moda = index_moda
                
                else:
                    moda = self.tabla_estadistica[mask1][self.__nombre_columna_xi__][index_moda]
            
            else:
                # Se obteiene el intervalo modal si esta en el index
                if self.__xi_es_index__ == True:
                    intervalo_moda = index_moda

                # Se obtiene el intevalo modal si esta en las columnas
                else:
                    intervalo_moda = self.tabla_estadistica[mask1][self.__nombre_columna_xi__][index_moda]
                
                # Limite inferior y superior del intervalo modal
                Li = intervalo_moda[0]
                Ls = intervalo_moda[1]

                # Frecuencia absoluta del intervalo anterior y siguiente al intevalo modal
                fa_intervalo_modal_anterior = self.tabla_estadistica.iloc[iloc_moda-1].loc[self.__nombre_columna_fa__]
                fa_intervalo_modal_siguiente = self.tabla_estadistica.iloc[iloc_moda+1].loc[self.__nombre_columna_fa__]

                # Frecuencia absoluta del intervalo modal
                ni = self.tabla_estadistica.iloc[iloc_moda].loc[self.__nombre_columna_fa__]
                
                # Tamano del intervalo modal
                ti = Ls - Li

                # Formula de moda para datos agrupados por intervalos / rangos
                moda = Li + (ni - fa_intervalo_modal_anterior) / (
                    (ni - fa_intervalo_modal_anterior) + (ni - fa_intervalo_modal_siguiente)
                    ) * ti

        return moda

    @property
    def rango_recorrido(self):
        agrupados = self.__agrupados__

        if agrupados == False:
            rango_recorrido = max(self.__xi__) - min(self.__xi__)
        
        else:
            rango_recorrido = 'Sin rango recorrido para datos agrupados'
        
        return rango_recorrido

    @property
    def varianza(self):
        muestra = self.__muestra__
        
        xi = self.__xi__
        nixi2 = self.__ni_xi2__
        n = self.__total_n__
        media = self.media

        if self.__agrupados__ == True:
            varianza = ((sum(nixi2) / n) - (media ** 2))
            

        else:
            if muestra == True:
                varianza = variance(xi)
            else:
                varianza = pvariance(xi)
        
        return varianza

    @property
    def desviacion_estandar(self):

        stdev = self.varianza ** .5

        return stdev

    @property
    def coeficiente_pearson(self):
        '''
        Interpretacion del resultado:
            Si As < 0 sera asimetrica negativa (izquierda), la media se encuentra por debajo de la mediana
            Si As = 0 sera simetrica
            Si As > 0 sera asimetrica positiva (derecha), la media se encuentra por encima de la mediana
        '''
        media = self.media
        moda = self.moda
        stdev = self.desviacion_estandar

        As = (media - moda) / stdev

        return As

    @property
    def medida_bowley(self):
        '''
        Interpretacion del resultado:
            Varia entre -1 y 1

            Si As < 0 sera asimetrica negativa (izquierda), la media se encuentra por debajo de la mediana
            Si As = 0 sera simetrica
            Si As > 0 sera asimetrica positiva (derecha), la media se encuentra por encima de la mediana
        '''

        cuartiles = self.cuantiles()
        
        cuartiles_keys = list(cuartiles.keys())

        q1 = cuartiles[cuartiles_keys[0]]
        q2 = cuartiles[cuartiles_keys[1]]
        q3 = cuartiles[cuartiles_keys[2]]

        As = (q1 +q3 - (2 * q2)) / (q3 - q1)

        return As

    @property
    def medida_fisher(self):
        
        media = self.media
        mediana = self.mediana
        s = self.desviacion_estandar
        xi = self.__xi__
        n = self.__total_n__


        xi_menos_media_al_cubo = []

        for x in xi:
            resultado = (x - media) ** 3
            xi_menos_media_al_cubo.append(resultado)

        sumatoria_xi_menos_media_al_cubo = sum(xi_menos_media_al_cubo)


        # Datos no agrupados
        if self.__agrupados__ == False:
            print('Fisher Datos No Agrupados')
            As = sumatoria_xi_menos_media_al_cubo / (n * (s**3))
        
        # Datos Agrupados
        else:
            print('Fisher Datos Agrupados')
            As = self.__medida_fisher_datos_agrupados__()

        return As

    @property
    def coeficiente_variacion(self):

        '''
        Interpretacion:
            Muestra el porcentaje de variabilidad contra la media, esto es, muestra la desviacion estandar promedio.
            cv <= 80% significa que el conjunto de datos es "homogeneo", 
                      por lo tanto la media es representativa de los datos.

            cv > 80%  significa que el conjunto de datos es "heterogeneo", 
                      por lo tanto la media no es representativa.
        '''

        s = self.desviacion_estandar
        media = self.media

        cv = s / media

        return cv

    @property
    def info(self):
        titulo = self.__titulo__
        agrupados = self.__agrupados__

        total_n = self.__total_n__
        media = self.media
        mediana = self.mediana
        moda = self.moda
        rango_recorrido = self.rango_recorrido
        varianza = self.varianza
        stdev = self.desviacion_estandar
        pearson = self.coeficiente_pearson
        bowley = self.medida_bowley
        fisher = self.medida_fisher
        cv = self.coeficiente_variacion

        if pearson < 0:
            interpretacion_pearson = 'Asimetrica Negativa'
        elif pearson > 0:
            interpretacion_pearson = 'Asimetrica Positiva'
        else:
            interpretacion_pearson = 'Simetrica'
        
        if bowley < 0:
            interpretacion_bowley = 'Asimetrica Negativa'
        elif pearson > 0:
            interpretacion_bowley = 'Asimetrica Positiva'
        else:
            interpretacion_bowley = 'Simetrica'

        if fisher < 0:
            interpretacion_fisher = 'Asimetrica Negativa'
        elif pearson > 0:
            interpretacion_fisher = 'Asimetrica Positiva'
        else:
            interpretacion_fisher = 'Simetrica'

        if cv <= .80:
            interpretacion_cv = 'Homogeneo'
        else:
            interpretacion_cv = 'Heterogeneo'

        display(HTML(f'''
            <h1>
                {titulo}
            </h1>
            <p align="left">
            <pre><strong><span style="font-size:120%">{'Datos Agrupados' if agrupados == True else 'Datos no Agrupados'}</span></strong></br></pre>
            <pre>Total n : <strong><span style="font-size:90%">{total_n} {self.__repr_fa__}</span></strong></br></pre>
            </br>
            <pre><strong><span style="font-size:120%">Variable Aleatoria "Xi": ({self.__repr_xi__})</span></strong></br></pre>
            <pre>media:                        <strong><span style="font-size:90%">{round(media, 4)}</span></strong></br></pre>
            <pre>mediana:                      <strong><span style="font-size:90%">{round(mediana, 4)}</span></strong></br></pre>
            <pre>moda:                         <strong><span style="font-size:90%">{round(moda, 4)}</span></strong></br></pre>
            <pre>rango recorrido:              <strong><span style="font-size:90%">{rango_recorrido}</span></strong></br></pre>
            <pre>varianza:                     <strong><span style="font-size:90%">{round(varianza, 4)}</span></strong></br></pre>
            <pre>desviacion tipica:            <strong><span style="font-size:90%">{round(stdev, 4)}</span></strong></br></pre>
            <pre>coeficiente variacion:        <strong><span style="font-size:90%">{round(cv, 4)} ({interpretacion_cv})</span></strong></br></pre>
            </br>
            <pre><strong><span style="font-size:120%">Asimetria:</span></strong></br></pre>
            <pre>pearson:           <strong><span style="font-size:90%">{round(pearson, 4)} ({interpretacion_pearson})</span></strong></br></pre>
            <pre>bowley:            <strong><span style="font-size:90%">{round(bowley, 4)} ({interpretacion_bowley})</span></strong></br></pre>
            <pre>fisher:            <strong><span style="font-size:90%">{round(fisher, 4)} ({interpretacion_fisher})</span></strong></br></pre>
            '''))
        
        dict_info = {
            'n': total_n, 'media': media, 'mediana': mediana, 'moda': moda, 
            'rango_recorrido': rango_recorrido, 'varianza': varianza, 'stdev': stdev, 'cv': cv, 
            'pearson': pearson, 'bowley': bowley, 'fisher': fisher}
        
        return dict_info

    def cuantiles(self, n=4, method='exclusive'):
        ''' Calculo de cuantiles para datos agrupados y no agrupados.'''
        
        xi = self.__xi__
        total_n = self.__total_n__
        mitad_faa = total_n/2
        es_rango = self.__es_rango__()
        
        # Datos "no" agrupados
        if self.__agrupados__ == False:
            cuantiles_formula = quantiles(xi, n=n, method=method)

            cuantiles = {}

            for k in range(1, n):
                cuantil_key = 'Q' + str(k)
                cuantil_value = cuantiles_formula[k-1]

                cuantiles[cuantil_key] = cuantil_value

        # Datos Agrupados
        else:
            # Genera una lista de llaves para buscar en los resultados de la formula "__encontrar_index_cuantil_datos_agrupados()"
            cuantiles_keys = [('index_Q' + str(k), 'Q' + str(k)) for k in range(1, n)]
            
            # La siguiente formula regresa un diccionario con los index de los cuartiles [indexQ{numero de cuantil}]
            index_cuantiles = self.__encontrar_index_cuantil_datos_agrupados__(n)
            
            clase_cuantiles = {}
            conteo_cuantil = 1
                
            # datos agrupados, xi no es rango y esta en index
            if self.__xi_es_index__ == True:
                for k in cuantiles_keys:
                    nombre_cuantil = 'Q' + str(conteo_cuantil)
                    clase_cuantiles[nombre_cuantil] = self.tabla_estadistica.index[index_cuantiles[k[0]]]

                    conteo_cuantil += 1


            # datos agrupados xi no es rango y "no" esta en index
            else:

                for k in cuantiles_keys:
                    nombre_cuantil = 'Q' + str(conteo_cuantil)
                    clase_cuantiles[nombre_cuantil] = self.tabla_estadistica.iloc[index_cuantiles[k[0]]][self.__nombre_columna_xi__]

                    conteo_cuantil += 1
            
            
            # datos agrupados, xi "no" es rango
            if es_rango == False:
                cuantiles = clase_cuantiles
            
            
            # datos agrupados, xi es rango
            else:
                
                k = 1
                cuantiles = {}
                
                for cuantil in cuantiles_keys:
                    
                    nombre_index_cuantil = cuantil[0]
                    
                    nombre_cuantil = cuantil[1]
                    
                    kn = (k * total_n) / n
                    
                    # Limite inferior y superior del intervalo del cuantil
                    Li = clase_cuantiles[nombre_cuantil][0]                    
                    Ls = clase_cuantiles[nombre_cuantil][1]
                    
                    
                    # Frecuencia absoluta acumulada del intervalo de la mediana anterior                    
                    faa_intervalo_cuantil_anterior = self.tabla_estadistica.iloc[index_cuantiles[nombre_index_cuantil]-1].loc['faa']
                    
                    
                    # Frecuencia absoluta del intervalo de la mediana                    
                    fi = self.tabla_estadistica.iloc[index_cuantiles[nombre_index_cuantil]].loc[self.__nombre_columna_fa__]
                                        
                    # Tamano del intervalo de la mediana
                    ai = Ls - Li
                                        
                    # Formula de mediana para datos agrupados por intervalos / rangos
                    cuantil = Li + (((kn) - faa_intervalo_cuantil_anterior) / fi) * ai
                    
                    cuantiles[nombre_cuantil] = cuantil
                    
                    k += 1

        return cuantiles

    def ubicar_rango_de_un_numero(self, objetivo, signo):
        '''
        Funcion. - Ubica el rango al que pertenece un numero objetivo

        Parametros:
            Objetivo.- numero a comparar.
            signo.- "=", "<", ">", ">=", "<="
        Regresa. - Serie del rango objetivo
        '''
        es_rango = self.__es_rango__()

        if es_rango == True:
            
            # Se filtran los intervalos
            intervalos = self.tabla_estadistica[self.__nombre_columna_xi__]
            ultimo_intervalo = intervalos[len(intervalos)-1]
            
            # Lista de indices encontrados
            indices_objetivo = []
            
            #try:
                # Por cada intervalo
            for index, intervalo in intervalos.items():
                if intervalo == ultimo_intervalo:

                    intervalo_inferior = intervalo[0]
                    intervalo_superior = intervalo[1] +1
                else:
                    intervalo_inferior = intervalo[0]
                    intervalo_superior = intervalo[1]

                # Rango de caja intervalo
                rango = range(intervalo_inferior, intervalo_superior)

                # Busqueda de acuerdo a signo
                if signo == '=':
                    if objetivo in rango:
                        indices_objetivo.append(index)
                    
                elif signo == '>=':
                    for numero in rango:
                        if objetivo <= numero:
                            indices_objetivo.append(index)
                            break

                elif signo == '<=':
                    for numero in rango:
                        if objetivo >= numero:
                            indices_objetivo.append(index)
                            break
                
                elif signo == '>':
                    for numero in rango:
                        if objetivo < numero:
                            indices_objetivo.append(index)
                            break

                elif signo == '<':
                    for numero in rango:
                        if objetivo > numero:
                            indices_objetivo.append(index)
                            break

                else:
                    raise ValueError('Signo erroneo')

            return self.tabla_estadistica.iloc[indices_objetivo]

            #except:
            #    raise ValueError('Objetivo fuera de rango')

        else:
            return 'No es rango'

    def buscar_percentil(self, percentil_objetivo):
        '''
        Objetivo. regresa [xi, fa, fra] del renglon del porcentaje (percentil) objetivo

        '''
        if self.__agrupados__ == False:
            percentiles= self.cuantiles(100)
            objetivo = 'Q' + str(int(percentil_objetivo*100))

            resultado = percentiles[objetivo]

        else:
            mascara = self.tabla_estadistica['fra'] > percentil_objetivo
            index_resultado = self.tabla_estadistica[mascara].index.min()

            resultado = self.tabla_estadistica.loc[index_resultado][[self.__nombre_columna_xi__, 'faa', 'fra']]

        return resultado

    def diagrama_caja_bigotes(self):
        
        titulo = self.__titulo__
        agrupados = self.__agrupados__
        total_n = self.__total_n__

        xi = self.__xi__
        cuartiles = self.cuantiles()
        
        cuartiles_keys = list(cuartiles.keys())


        q1 = cuartiles[cuartiles_keys[0]]
        q2 = cuartiles[cuartiles_keys[1]]
        q3 = cuartiles[cuartiles_keys[2]]

        rango_intercuartilico = q3 - q1

        bigote_inferior = min(xi)
        bigote_superior = max(xi)

        barra_inferior = q1 - (1.5 * rango_intercuartilico)
        barra_superior = q3 + (1.5 * rango_intercuartilico)

        datos_atipicos = []
        datos_atipicos_inferior = []
        datos_atipicos_superior = []

        for x in xi:
            if x < barra_inferior:
                datos_atipicos.append(x)
                datos_atipicos_inferior.append(x)

            elif x > barra_superior:
                datos_atipicos.append(x)
                datos_atipicos_superior.append(x)
        
        display(HTML(f'''
        <h1>
                {titulo}
        </h1>
        <p align="left">
        <pre><strong><span style="font-size:120%">{'Datos Agrupados' if agrupados == True else 'Datos no Agrupados'}</span></strong></br></pre>
        <pre>Total n : <strong><span style="font-size:90%">{total_n} {self.__repr_fa__}</span></strong></br></pre>
        </br>
        <pre><strong><span style="font-size:120%">Variable Aleatoria "Xi": ({self.__repr_xi__})</span></strong></br></pre>
        </br>
        <pre>Q1:                     <strong><span style="font-size:110%">{round(q1, 4)}</span></strong></br></pre>
        <pre>Q2:                     <strong><span style="font-size:110%">{round(q2, 4)}</span></strong></br></pre>
        <pre>Q3:                     <strong><span style="font-size:110%">{round(q3, 4)}</span></strong></br></pre>
        <pre>Bigote Inferior:        <strong><span style="font-size:110%">{round(bigote_inferior, 4)}</span></strong></br></pre>
        <pre>Bigote Superior:        <strong><span style="font-size:110%">{round(bigote_superior,4)}</span></strong></br></pre>
        </br>
        <pre>Rango Intercuartilico:  <strong><span style="font-size:110%">{round(rango_intercuartilico, 4)}</span></strong></br></pre>
        <pre>Barra Inferior:         <strong><span style="font-size:110%">{round(barra_inferior, 4)}</span></strong></br></pre>
        <pre>Barra Superior:         <strong><span style="font-size:110%">{round(barra_superior, 4)}</span></strong></br></pre>
        <pre>Atipicos Inferior:      <strong><span style="font-size:110%">{datos_atipicos_inferior}</span></strong></pre>
        <pre>Atipicos Superior:      <strong><span style="font-size:110%">{datos_atipicos_superior}</span></strong></pre></br>
        <pre>El <strong>50%</strong> de "{titulo}" se encuentran entre <strong>{round(q1, 4)}</strong> y <strong>{round(q3, 4)} {self.__repr_xi__}</strong></br></pre>
        <pre>El <strong>75%</strong> de "{titulo}" se encuentran en menos de <strong>{round(q3, 4)} {self.__repr_xi__}</strong></br></pre>
        <pre>El <strong>50%</strong> de "{titulo}" se encuentan en mas de <strong>{round(q2, 4)} {self.__repr_xi__}</strong></pre>
        </p>
        '''))

        return {'Q1': q1, 'Q2': q2, 'Q3': q3, 'BiI': bigote_inferior, 'BiS': bigote_superior, 'RI': rango_intercuartilico, 
        'BaI': barra_inferior, 'BaS': barra_superior, 'atipicos': datos_atipicos, 
        'atipicos_inf': datos_atipicos_inferior, 'atipicos_sup': datos_atipicos_superior}

    def __str__(self):
        return f'''
        Titulo: {self.__titulo__}
        Agrupados: {self.__agrupados__}
        Xi se encuentra en index: {self.__xi_es_index__}
        Xi: {self.__nombre_columna_xi__}
        Fa: {self.__nombre_columna_fa__}
        '''

    def _repr_html_(self):
        if self.__agrupados__ == False:
            return f'''
            <body>
                <h1>
                    {self.__titulo__}
                </h1>

                <p align="left">
                    <pre><strong><span style="font-size:110%">{'Datos Agrupados' if self.__agrupados__ ==True else 'Datos No Agrupados'}</span></strong></br></pre>
                    <pre>Total n: <strong><span style="font-size:110%">{self.__total_n__}</span></strong> {self.__repr_fa__}</br></pre>
                </p>

                <table border="1" align="center" cellspacing="0" cellpadding="5">
                    <tr valign="bottom" align="center">
                        <th width="300"><pre><span style="font-size:110%">Variable Aleatoria (Xi)</span></br></pre></pre></th>
                        <th width="300"><pre><span style="font-size:110%">Elementos (ni)</span></br></pre></pre></th>	
                    </tr>
                    <tr>
                        <td>
                            <table border="1" align="center" cellspacing="0" cellpadding="5"  width="300"  height="20">
                                <tr>
                                <td> Representa:</td>
                                <td><strong> {self.__repr_xi__}</strong></td>
                                </tr>
                                <tr>
                                <td> Columna Xi:</td>
                                <td><strong> {self.__nombre_columna_xi__}</strong></td>
                                </tr>
                            </table>
                        </td>
                        <td>
                            <table border="1" align="center" cellspacing="0" cellpadding="5"  width="300"  height="20">
                               <tr>
                                <td>Representa:</td>
                                <td><strong> {self.__repr_fa__}</strong></td>
                                </tr>
                            </table>
                        </td>	
                    </tr>
                    <tr>
                    </table>
            </body>
            {self.tabla_estadistica._repr_html_()}
            '''

        else:
            return f'''
            <body>
                <h1>
                    {self.__titulo__}
                </h1>

                <p align="left">
                    <pre><strong><span style="font-size:110%">{'Datos Agrupados' if self.__agrupados__ ==True else 'Datos No Agrupados'}</span></strong></br></pre>
                    <pre>Total n: <strong><span style="font-size:110%">{self.__total_n__}</span></strong> {self.__repr_fa__}</br></pre>
                </p>

                <table border="1" align="center" cellspacing="0" cellpadding="5">
                    <tr valign="bottom" align="center">
                        <th width="300"><pre><span style="font-size:110%">Variable Aleatoria (Xi)</span></br></pre></pre></th>
                        <th width="300"><pre><span style="font-size:110%">Elementos (Fa/ni)</span></br></pre></pre></th>	
                    </tr>
                    <tr>
                        <td>
                            <table border="1" align="center" cellspacing="0" cellpadding="5"  width="300"  height="20">
                                <tr>
                                <td> Representa:</td>
                                <td><strong> {self.__repr_xi__}</strong></td>
                                </tr>
                                <tr>
                                <td> Columna Xi:</td>
                                <td><strong> {self.__nombre_columna_xi__}</strong></td>
                                </tr>
                            </table>
                        </td>
                        <td>
                            <table border="1" align="center" cellspacing="0" cellpadding="5"  width="300"  height="20">
                               <tr>
                                <td> Representa:</td>
                                <td><strong> {self.__repr_fa__}</strong></td>
                                </tr>
                                <tr>
                                <td> Columna Fa:</td>
                                <td><strong> {self.__nombre_columna_fa__}</strong></td>
                                </tr>
                            </table>
                        </td>	
                    </tr>
                    <tr>
                    </table>
            </body>
            {self.tabla_estadistica._repr_html_()}'''



if '__main__' == __name__:

    saltos = [
    283.6, 269.4, 262.2, 261.1, 246.7, 245.5, 239.2, 233.7, 230.3, 227.9, 
    226.4, 225.5, 224.1, 223.6, 222.3, 221.4, 217.8, 217.2, 216.9, 211.6,
    211.4, 208.5, 204.9, 202.7, 202.4, 200.5, 198.5, 182.4, 111
    ]

    saltos = pandas.DataFrame(saltos, columns = ['saltos'])

    de_saltos = AnalisisEstadistico(saltos, 'Resultados de Saltos de Esqui Masculino')

    print(de_saltos)
