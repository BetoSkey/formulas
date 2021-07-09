import pandas
from IPython.core.display import display, HTML
from statistics import mean, median_grouped, median_high, variance, stdev, mode, multimode, quantiles
from formulas_especiales import ceiling_to_a_number, floor_to_a_number

class DatosEstadisticos:

    def __init__(self, datos, titulo, agrupados=False, columna_xi=0, columna_fa=0, xi_es_index=False, muestra=True):
        
        if type(datos) == list:
            self.datos = pandas.DataFrame(datos)

        elif type(datos) == pandas.Series:
            self.datos = datos.to_frame()
        
        else:
            self.datos = datos
        
        self.titulo = titulo
        self.agrupados = agrupados
        self.columna_xi = columna_xi
        self.columna_fa = columna_fa
        self.xi_es_index = xi_es_index
        self.muestra = muestra

        nombre_columnas = self.__obtener_nombre_columnas__()
        self.nombre_columna_xi = nombre_columnas['xi']
        self.nombre_columna_fa = nombre_columnas['fa']

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

            frecuencias_series = pandas.Series(frecuencias, name=self.nombre_columna_xi)

            tabla_intervalos_frecuencias = pandas.concat([intervalos, frecuencias_series], axis=1)

        return tabla_intervalos_frecuencias

    def convertir_a_intervalos(self, rango_intervalos):
        datos = self.__calculo_frecuencias_absolutas__(rango_intervalos)
        #self.__init__(datos, self.titulo, columna_xi='intervalos', columna_fa=self.columna_fa, agrupados=True)
        
        return datos

    def __total_n__(self):

        if self.agrupados == False:
            total_n = len(self.datos[self.nombre_columna_xi])
        
        else:
            total_n = self.datos[self.nombre_columna_fa].sum()

        return total_n

    def _repr_html_(self):
        if self.agrupados == False:
            return f'''
            <p align="left">
            <pre>Titulo:      <strong><span style="font-size:110%">{self.titulo}</span></strong></br></pre>
            <pre>Agrupados:   <strong><span style="font-size:110%">{self.agrupados}</span></strong></br></pre>
            <pre>Columna Xi:  <strong><span style="font-size:110%">{self.nombre_columna_xi}</span></strong></br></pre>
            <pre>Total n:     <strong><span style="font-size:110%">{self.total_n}</span></strong></br></pre>
            </p>
            {self.datos._repr_html_()}
            '''

        else:
            return f'''
            <p align="left">
            <pre>Titulo:          <strong><span style="font-size:110%">{self.titulo}</span></strong></br></pre>
            <pre>Agrupados:       <strong><span style="font-size:110%">{self.agrupados}</span></strong></br></pre>
            <pre>Columna Xi:      <strong><span style="font-size:110%">{self.nombre_columna_xi}</span></strong></br></pre>
            <pre>Columna ni/Fa:   <strong><span style="font-size:110%">{self.nombre_columna_fa}</span></strong></pre>
            <pre>Total n:     <strong><span style="font-size:110%">{self.total_n}</span></strong></br></pre>
            </p>
            {self.datos._repr_html_()}'''





class AnalisisEstadistico:
    
    def __init__(self, datos, titulo, agrupados=False, columna_xi=0, columna_fa=0, xi_es_index=False, muestra=True):
        
        if type(datos) == list:

            self.datos = pandas.DataFrame(datos)

        elif type(datos) == pandas.Series:

            self.datos = datos.to_frame()
        
        else:
            self.datos = datos
        
        self.tabla_estadistica = self.datos.copy()
        self.titulo = titulo
        self.agrupados = agrupados
        self.columna_xi = columna_xi
        self.columna_fa = columna_fa
        self.xi_es_index = xi_es_index
        self.muestra = muestra

        nombre_columnas = self.__obtener_nombre_columnas__()
        self.nombre_columna_xi = nombre_columnas['xi']
        self.nombre_columna_fa = nombre_columnas['fa']
        
        

        datos_xi_ni = self.__obtener_datos_ni_xi__()
        self.xi = datos_xi_ni[0]
        self.fa = datos_xi_ni[1]

        self.total_n = self.__total_n__()

        frecuencias_acumuladas = self.__calculo_frecuencias_acumuladas__()
        self.faa = frecuencias_acumuladas['faa']
        self.fr = frecuencias_acumuladas['fr']
        self.fra = frecuencias_acumuladas['fra']

        self.mc = self.__calculo_marcas_clase__()
        self.xi2 = self.__obtener_xi2__()

        columnas_ni_por_xi = self.__calcular_columna_ni_por_xi__()
        self.ni_xi = columnas_ni_por_xi[0]
        self.ni_xi2 = columnas_ni_por_xi[1]

        self.__ordenar_datos__()

    def __ordenar_datos__(self):

        if self.xi_es_index == True:
            self.tabla_estadistica.sort_index(inplace=True)

        else:
            self.tabla_estadistica.sort_values(self.nombre_columna_xi, inplace=True)

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
            columna_xi_name = self.tabla_estadistica.index.name

        else:
            # Si "xi" no esta en el index
            # Si "xi" es string
            if type_xi == str:
                columna_xi_name = self.columna_xi
            
            # Si "xi" no esta en el index
            # Si "xi" es un numero
            else:
                columna_xi_name = self.tabla_estadistica.iloc[:,self.columna_xi].name

        #------- obtenemos nombre de columna "fa" -------
        # Si "fa" es string
        if type_fa == str:
            columna_fa_name = self.columna_fa

        # Si "fa" es un numero
        else:
            columna_fa_name = self.tabla_estadistica.iloc[:,self.columna_fa].name

        return {'xi':columna_xi_name, 'fa':columna_fa_name}

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

            frecuencias_series = pandas.Series(frecuencias, name=self.nombre_columna_xi)

            tabla_intervalos_frecuencias = pandas.concat([intervalos, frecuencias_series], axis=1)

        return tabla_intervalos_frecuencias

    def convertir_a_intervalos(self, rango_intervalos):
        datos = self.__calculo_frecuencias_absolutas__(rango_intervalos)
        #self.__init__(datos, self.titulo, columna_xi='intervalos', columna_fa=self.columna_fa, agrupados=True)
        
        return datos


    def __es_rango__(self):
        
        xi = self.xi
        
        try:
            es_rango = True if (type(xi.iloc[0]) is list or type(xi.iloc[0]) is tuple) else False

        except:
            es_rango = True if (type(xi[0]) is list or type(xi[0]) is tuple) else False

        return es_rango

    def __total_n__(self):

        if self.agrupados == False:
            total_n = len(self.xi)
        
        else:
            total_n = self.fa.sum()

        return total_n

    def __obtener_datos_ni_xi__(self):
        
        if self.xi_es_index == True:

            xi = self.tabla_estadistica.index
                
        else:
            
            xi = self.tabla_estadistica.loc[: , self.nombre_columna_xi]

        ni = self.tabla_estadistica.loc[: , self.nombre_columna_fa]
        
        return (xi, ni)

    def __obtener_xi2__(self):

        if self.agrupados == False:
            xi2 = None
        
        else:
            es_rango = self.__es_rango__()

            xi = self.xi
            mc = self.mc

            if es_rango:
                xi2 = self.tabla_estadistica['xi2'] = mc ** 2
            
            else:
                xi2 = self.tabla_estadistica['xi2'] = xi ** 2
        
        return xi2

    def __calcular_columna_ni_por_xi__(self):

        if self.agrupados == True:
            if self.mc is not None:
                self.tabla_estadistica['ni*xi'] = self.mc * self.fa
                
            else:
                self.tabla_estadistica['ni*xi'] = self.xi * self.fa
            
            self.tabla_estadistica['ni*xi2'] = self.xi2 * self.fa

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

        xi = self.xi
        
        es_rango = self.__es_rango__()
        
        if es_rango:

            self.tabla_estadistica['marca clase'] = self.xi
            
            self.tabla_estadistica['marca clase'] = self.tabla_estadistica['marca clase'].apply(self.__marca_clase__)

            marcas_de_clase = self.tabla_estadistica['marca clase']

        else:
            marcas_de_clase = None
        
        return marcas_de_clase

    def __calculo_frecuencias_acumuladas__(self):
        
        xi = self.xi
        fa = self.fa
        total_n = self.total_n

        if self.agrupados == False:
            faa = None
            fr = None
            fra = None

        else:
            faa = self.tabla_estadistica['faa'] = fa.cumsum()
            fr = self.tabla_estadistica['fr'] = fa / total_n
            fra = self.tabla_estadistica['fra'] = fr.cumsum()

        return {'faa': faa, 'fr': fr, 'fra': fra}

    @property
    def media(self):
            
        xi = self.xi
        ni = self.fa

        if self.agrupados == False:

            media = xi.mean()

        else:
            
            #Si los datos estan agrupados por rangos
            if self.mc is not None:
                xi = self.mc

            
            sumatoria_ni = ni.sum()
            sumatoria_ni_xi = (xi * ni).sum()

            media = sumatoria_ni_xi / sumatoria_ni
        
        return media

    @property
    def mediana(self):
        
        # Si los datos no estan agrupados
        if self.agrupados == False:
            mediana = self.fa.median()

        # Si los datos estan agrupados
        else:
            total_n = self.total_n
            faa = self.faa
            es_rango = self.__es_rango__()

            mediana_faa = median_grouped(faa)

            mask1 = self.tabla_estadistica['faa'] == mediana_faa
            
            try:
                index_mediana = self.tabla_estadistica[mask1].index[0]
            
            except:
                mediana_faa = median_high(faa)

                mask1 = self.tabla_estadistica['faa'] == mediana_faa

                index_mediana = self.tabla_estadistica[mask1].index[0]

            iloc_mediana = self.tabla_estadistica.index.get_loc(index_mediana)

            # Si "xi" no son intervalos/rangos
            if es_rango == False:
                if self.xi_es_index == True:
                    mediana = index_mediana
                
                else:
                    mediana = self.tabla_estadistica[mask1][self.nombre_columna_xi][index_mediana]
            
            # Si "xi" son intervalos/rangos
            else:

                # Se obteiene el intervalo de la mediana si esta en el index
                if self.xi_es_index == True:
                    intervalo_mediana = index_mediana

                # Se obtiene el intevalo de la mediana si esta en las columnas
                else:
                    intervalo_mediana = self.tabla_estadistica[mask1][self.nombre_columna_xi][index_mediana]
                
                # Limite inferior y superior del intervalo de la mediana
                Li = intervalo_mediana[0]
                Ls = intervalo_mediana[1]

                # Frecuencia absoluta acumulada del intervalo de la mediana anterior
                faa_intervalo_mediana_anterior = self.tabla_estadistica.iloc[iloc_mediana-1].loc['faa']

                # Frecuencia absoluta del intervalo de la mediana
                ni = self.tabla_estadistica.iloc[iloc_mediana].loc[self.nombre_columna_fa]
                
                # Tamano del intervalo de la mediana
                ti = Ls - Li

                # Formula de mediana para datos agrupados por intervalos / rangos
                mediana = Li + (((total_n /2) - faa_intervalo_mediana_anterior) / ni) * ti

        return mediana

    @property
    def moda(self, multimoda=False):

        # Datos No Agrupados
        if self.agrupados == False:
            if multimoda == False:
                moda = mode(self.xi)
            
            else:
                moda = multimode(self.xi)

        # Datos Agrupados
        else:

            es_rango = self.__es_rango__()
            moda_fa = max(self.fa)

            mask1 = self.tabla_estadistica['fa'] == moda_fa

            index_moda = self.tabla_estadistica[mask1].index[0]
            iloc_moda = self.tabla_estadistica.index.get_loc(index_moda)

            # Si "xi" no son intervalos/rangos
            if es_rango == False:
                if self.xi_es_index == True:
                    moda = index_moda
                
                else:
                    moda = self.tabla_estadistica[mask1][self.nombre_columna_xi][index_moda]
            
            else:
                # Se obteiene el intervalo modal si esta en el index
                if self.xi_es_index == True:
                    intervalo_moda = index_moda

                # Se obtiene el intevalo modal si esta en las columnas
                else:
                    intervalo_moda = self.tabla_estadistica[mask1][self.nombre_columna_xi][index_moda]
                
                # Limite inferior y superior del intervalo modal
                Li = intervalo_moda[0]
                Ls = intervalo_moda[1]

                # Frecuencia absoluta del intervalo anterior y siguiente al intevalo modal
                fa_intervalo_modal_anterior = self.tabla_estadistica.iloc[iloc_moda-1].loc[self.nombre_columna_fa]
                fa_intervalo_modal_siguiente = self.tabla_estadistica.iloc[iloc_moda+1].loc[self.nombre_columna_fa]

                # Frecuencia absoluta del intervalo modal
                ni = self.tabla_estadistica.iloc[iloc_moda].loc[self.nombre_columna_fa]
                
                # Tamano del intervalo modal
                ti = Ls - Li

                # Formula de moda para datos agrupados por intervalos / rangos
                moda = Li + (ni - fa_intervalo_modal_anterior) / (
                    (ni - fa_intervalo_modal_anterior) + (ni - fa_intervalo_modal_siguiente)
                    ) * ti

        return moda

    @property
    def varianza(self):
        xi = self.xi
        nixi2 = self.ni_xi2
        n = self.total_n
        media = self.media

        if self.agrupados == True:
            varianza = ((sum(nixi2) / n) - (media ** 2))
        
        else:
            varianza = variance(xi)
        
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
        mediana = self.mediana
        stdev = self.desviacion_estandar

        As = (3 * (media - mediana)) / stdev

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

        q1 = cuartiles[0]
        q2 = cuartiles[1]
        q3 = cuartiles[2]

        As = (q1 +q3 - (2 * q2)) / (q3 - q1)

        return As

    @property
    def medida_fisher(self):
        
        media = self.media
        mediana = self.mediana
        s = self.desviacion_estandar
        xi = self.xi
        n = self.total_n


        if self.agrupados == False:
            
            xi_menos_media_al_cubo = []

            for x in xi:
                resultado = (x - media) ** 3
                xi_menos_media_al_cubo.append(resultado)

            sumatoria_xi_menos_media_al_cubo = sum(xi_menos_media_al_cubo)

            As = sumatoria_xi_menos_media_al_cubo / (n * (s**3))
        
        else:
            
            if self.es_rango() == False:

                xi_ni = self.tabla_estadistica[['xi', 'fa']]

                As = sum((xi_ni['fa'] * (xi_ni['xi'] - media)) ** 3) / (n * (s**3))
        
            else:

                mc_ni = self.tabla_estadistica[['mc', 'fa']]

                As = sum((xi_ni['fa'] * (xi_ni['mc'] - media)) ** 3) / (n * (s**3))

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

    def cuantiles(self, n=4, method='exclusive'):
        xi = self.xi

        if self.agrupados == False:
            cuantiles = quantiles(xi, n=n, method=method)
        
        else:
            cuantiles = 'falta calcular los cuantiles con datos agrupados'
        
        return cuantiles

    def buscar_percentil(self, percentil_objetivo):
        '''
        Objetivo. regresa [xi, fa, fra] del renglon del porcentaje (percentil) objetivo

        '''
        mascara = self.tabla_estadistica['fra'] > percentil_objetivo
        index_resultado = self.tabla_estadistica[mascara].index.min()

        resultado = self.tabla_estadistica.loc[index_resultado][[self.nombre_columna_xi, 'faa', 'fra']]

        return resultado

    def diagrama_caja_bigotes(self):
        
        titulo = self.titulo
        agrupados = self.agrupados

        xi = self.xi
        cuartiles = self.cuantiles(n=4)
        
        q1 = cuartiles[0]
        q2 = cuartiles[1]
        q3 = cuartiles[2]

        rango_intercuartilico = q3 - q1

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
        <p align="left">
        <pre>Titulo:      <strong><span style="font-size:110%">{self.titulo}</span></strong></br></pre>
        <pre>Agrupados:   <strong><span style="font-size:110%">{agrupados}</span></strong></br></pre>
        </br>
        <pre>Q1:                     <strong><span style="font-size:110%">{q1}</span></strong></br></pre>
        <pre>Q2:                     <strong><span style="font-size:110%">{q2}</span></strong></br></pre>
        <pre>Q3:                     <strong><span style="font-size:110%">{q3}</span></strong></br></pre>
        
        <pre>Rango Intercuartilico:  <strong><span style="font-size:110%">{rango_intercuartilico}</span></strong></br></pre>
        <pre>Barra Inferior:         <strong><span style="font-size:110%">{barra_inferior}</span></strong></br></pre>
        <pre>Barra Superior:         <strong><span style="font-size:110%">{barra_superior}</span></strong></br></pre>
        <pre>Atipicos Inferior:      <strong><span style="font-size:110%">{datos_atipicos_inferior}</span></strong></pre>
        <pre>Atipicos Superior:      <strong><span style="font-size:110%">{datos_atipicos_superior}</span></strong></pre></br>
        <pre>El <strong>50%</strong> de "{titulo}" se encuentran entre <strong>{q1}</strong> y <strong>{q3}</strong></br></pre>
        <pre>El <strong>75%</strong> de "{titulo}" se encuentran en menos de <strong>{q3}</strong></br></pre>
        <pre>El <strong>50%</strong> de "{titulo}" se encuentan en mas de <strong>{q2}</strong></pre>
        </p>
        '''))

        return {'Q1': q1, 'Q2': q2, 'Q3': q3, 'RI': rango_intercuartilico, 
        'BI': barra_inferior, 'BS': barra_superior, 'atipicos': datos_atipicos, 
        'atipicos_inf': datos_atipicos_inferior, 'atipicos_sup': datos_atipicos_superior}



    @property
    def info(self):
        titulo = self.titulo
        agrupados = self.agrupados

        total_n = self.total_n
        media = self.media
        mediana = self.mediana
        moda = self.moda
        varianza = self.varianza
        stdev = self.desviacion_estandar
        pearson = self.coeficiente_pearson

        display(HTML(f'''
        <p align="left">
        <pre>Titulo:      <strong><span style="font-size:110%">{self.titulo}</span></strong></br></pre>
        <pre>Agrupados:   <strong><span style="font-size:110%">{agrupados}</span></strong></br></pre>
        </br>
        <pre>n:           <strong><span style="font-size:90%">{total_n}</span></strong></br></pre>
        <pre>media:       <strong><span style="font-size:90%">{media}</span></strong></br></pre>
        <pre>mediana:     <strong><span style="font-size:90%">{mediana}</span></strong></br></pre>
        <pre>moda:        <strong><span style="font-size:90%">{moda}</span></strong></br></pre>
        <pre>varianza:    <strong><span style="font-size:90%">{varianza}</span></strong></br></pre>
        <pre>stdev:       <strong><span style="font-size:90%">{stdev}</span></strong></br></pre>
        <pre>pearson:     <strong><span style="font-size:90%">{pearson}</span></strong></br></pre>
        '''))

        return {'n': total_n, 'media': media, 'mediana': mediana, 'moda': moda, 'varianza': varianza, 'moda': moda, 'stdev': stdev, 'pearson': pearson}

    def __str__(self):
        return f'''
        Titulo: {self.titulo}
        Agrupados: {self.agrupados}
        Xi se encuentra en index: {self.xi_es_index}
        Xi: {self.nombre_columna_xi}
        Fa: {self.nombre_columna_fa}
        '''

    def _repr_html_(self):
        if self.agrupados == False:
            return f'''
            <p align="left">
            <pre>Titulo:      <strong><span style="font-size:110%">{self.titulo}</span></strong></br></pre>
            <pre>Agrupados:   <strong><span style="font-size:110%">{self.agrupados}</span></strong></br></pre>
            <pre>Columna Xi:  <strong><span style="font-size:110%">{self.nombre_columna_xi}</span></strong></br></pre>
            <pre>Total n:     <strong><span style="font-size:110%">{self.total_n}</span></strong></br></pre>
            </p>
            {self.tabla_estadistica._repr_html_()}
            '''

        else:
            return f'''
            <p align="left">
            <pre>Titulo:          <strong><span style="font-size:110%">{self.titulo}</span></strong></br></pre>
            <pre>Agrupados:       <strong><span style="font-size:110%">{self.agrupados}</span></strong></br></pre>
            <pre>Columna Xi:      <strong><span style="font-size:110%">{self.nombre_columna_xi}</span></strong></br></pre>
            <pre>Columna ni/Fa:   <strong><span style="font-size:110%">{self.nombre_columna_fa}</span></strong></pre>
            <pre>Total n:     <strong><span style="font-size:110%">{self.total_n}</span></strong></br></pre>
            </p>
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
