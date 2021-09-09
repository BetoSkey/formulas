'Estoy en branch bivariada'
import sys
sys.path.append('C:\\Users\\gilbe\\github\\formulas_personales\\datos_estadisticos\\')
sys.path.append('C:\\Users\\gilbe\\github\\formulas_personales\\')
import pandas
import copy
from IPython.core.display import display, HTML
from statistics import variance, mode, multimode, quantiles, pvariance
from formulas_especiales import ceiling_to_a_number, floor_to_a_number
import unittest

class Backup:
    def __crear_backup__(self):

        if type(self) == DatosBivariada or type(self) == AnalisisBivariada:

            self.__yi_en_columnas_backup__ = copy.copy(self.__yi_en_columnas__)
            self.__columna_yi_backup__ = copy.copy(self.__columna_yi__)
            self.__nombre_columna_yi_backup__ = copy.copy(self.__nombre_columna_yi__)
            self.__yi_name_backup__ = copy.copy(self.__yi__.name)
            self.__yi_backup__ = copy.copy(self.__yi__)

            if type(self) == DatosBivariada:
                self.__datos_backup__ = copy.copy(self.datos)
            else:
                self.__datos_backup__ = copy.copy(self.datos.datos)

        self.__columna_xi_backup__ = copy.copy(self.__columna_xi__)
        self.__nombre_columna_xi_backup__ = copy.copy(self.__nombre_columna_xi__)
        self.__xi_name_backup__ = copy.copy(self.__xi__.name)
        self.__columna_fa_backup__ = copy.copy(self.__columna_fa__)
        self.__fa_name_backup__ = copy.copy(self.__fa__.name)
        self.__nombre_columna_fa_backup__ = copy.copy(self.__nombre_columna_fa__)
        self.__agrupados_backup__ = copy.copy(self.__agrupados__)
        self.__xi_backup__ = copy.copy(self.__xi__)
        self.__fa_backup__ = copy.copy(self.__fa__)



    def __regresar_backup__(self):

        if type(self) == DatosBivariada or type(self) == AnalisisBivariada:
            
            self.__yi_en_columnas__ = self.__yi_en_columnas_backup__
            self.__columna_yi__ = self.__columna_yi_backup__
            self.__nombre_columna_yi__ = self.__nombre_columna_yi_backup__
            self.__yi__.name = self.__yi_name_backup__
            self.__yi__ = self.__yi_backup__

            if type(self) == DatosBivariada:
                self.datos = self.__datos_backup__
            else:
                self.datos.datos = self.__datos_backup__
                self.tabla_estadistica = self.__datos_backup__

        self.__columna_xi__ = self.__columna_xi_backup__
        self.__nombre_columna_xi__ = self.__nombre_columna_xi_backup__
        self.__xi__.name = self.__xi_name_backup__
        self.__columna_fa__ = self.__columna_fa_backup__
        self.__fa__.name = self.__fa_name_backup__
        self.__nombre_columna_fa__ = self.__nombre_columna_fa_backup__
        self.__agrupados__ = self.__agrupados_backup__
        self.__xi__ = self.__xi_backup__
        self.__fa__ = self.__fa_backup__
            


    def datos_originales(self):
        try:
            self.__regresar_backup__()
        except:
            raise TypeError('No hay backup de datos')
        
        return self

class TablaPivote:

    def __establecer_index_y_columnas_para_tabla_pivote(self, index):
        
        if index == None:
            index = [self.__nombre_columna_xi__, self.__nombre_columna_yi__]
            columnas = None
        
        elif index == self.__nombre_columna_xi__:
            columnas = self.__nombre_columna_yi__
        
        elif index == self.__nombre_columna_yi__:
            columnas = self.__nombre_columna_xi__
        
        else:
            raise ValueError('Nombre de index SOLAMENTE puede ser el nombre de la columna xi o el de yi')

        return (index, columnas)

    def __crear_tabla_pivote__(self, index, tipo, totales):

        index, columnas = self.__establecer_index_y_columnas_para_tabla_pivote(index=index)
        
        
        fill_value = None
        
        # columnas == None es para la formula DatosBivariados.agrupar()
        if columnas == None:
            '''tabla_pivote = self.datos.pivot_table(
                index=index, columns=columnas, aggfunc= lambda x: len(x)/len(self.datos), 
                fill_value=fill_value).reset_index().rename({0:'ni'}, axis=1)'''

            tabla_pivote = self.datos.pivot_table(
                index=index, columns=columnas, aggfunc= lambda x: len(x), 
                fill_value=fill_value).reset_index().rename({0:'ni'}, axis=1)


        # columnas != None
        else:
            
            if tipo == None:
                if totales == False:
                    tabla_pivote = self.datos.pivot_table(
                        index= index, columns= columnas, aggfunc= len, fill_value=fill_value)
                else:
                    tabla_pivote = self.datos.pivot_table(
                        index= index, columns= columnas, aggfunc= len, margins=True, margins_name='Total', 
                        fill_value=fill_value)
            
            elif tipo == 'relativa':
                if totales == False:
                    tabla_pivote = self.datos.pivot_table(
                        index= index, columns= columnas, aggfunc= lambda x: len(x)/len(self.datos), 
                        fill_value=fill_value)
                else:
                    tabla_pivote = self.datos.pivot_table(
                        index= index, columns= columnas, aggfunc= lambda x: len(x)/len(self.datos), 
                        margins=True, margins_name='Total', fill_value=fill_value)

            elif tipo == 'marginal':
                if totales == False:
                    tabla_pivote = self.datos.pivot_table(
                        index= index, columns= columnas, aggfunc= lambda x: len(x)/len(self.datos), 
                        fill_value=fill_value)
                else:
                    tabla_pivote = self.datos.pivot_table(
                        index= index, columns= columnas, aggfunc= lambda x: len(x)/len(self.datos), 
                        margins=True, margins_name='Total', fill_value=fill_value)
                
            elif tipo == 'marginal_index':
                if totales == False:
                    tabla_pivote = pandas.crosstab(
                        index=self.datos[index], columns=self.datos[columnas], normalize='index')
                else:
                    tabla_pivote = pandas.crosstab(
                        index=self.datos[index], columns=self.datos[columnas], normalize='index', 
                        margins=True, margins_name='Total')

            elif tipo == 'marginal_columns':
                if totales == False:
                    tabla_pivote = pandas.crosstab(
                        index=self.datos[index], columns=self.datos[columnas], normalize='columns')
                else:
                    tabla_pivote = pandas.crosstab(
                        index=self.datos[index], columns=self.datos[columnas], normalize='columns', 
                        margins=True, margins_name='Total')

            else:
                raise ValueError('"tipo" no reconocido')


        return tabla_pivote





class DatosEstadisticos(Backup):
    def __init__(self, datos, titulo, repr_xi, repr_fa, agrupados, columna_xi, columna_fa, xi_es_index, muestra):
        self.datos = datos
        self.__titulo__ = titulo
        self.__repr_xi__ = repr_xi
        self.__repr_fa__ = repr_fa
        self.__agrupados__ = agrupados
        self.__columna_xi__ = columna_xi
        self.__columna_fa__ = columna_fa
        self.__xi_es_index__ = xi_es_index
        self.__muestra__ = muestra

    def __reubicar_columna_fa__(self):
        
        # Si self.__columna_fa__ es str se mantiene el nombre ya que pandas lo tiene seleccionado con el nombre de la columna, si es un numero, se debe aumentar en 1
        if type(self.__columna_fa__) != str:
            
            self.__columna_fa__ = self.__columna_fa__ + 1
        
    def __quitar_xi_de_index__(self):

        self.datos.reset_index(inplace= True)
        self.datos.rename(mapper = {self.datos.columns[0]: self.__repr_xi__}, axis='columns', inplace=True)

        self.__reubicar_columna_fa__()

        self.__xi_es_index__ = False

    def __melt_datos__(self):
        if self.__yi_en_columnas__ == True:

            self.datos = self.datos.melt(
                id_vars=self.__nombre_columna_xi__, var_name= self.__repr_yi__, value_name=self.__repr_fa__).sort_values(
                    self.__nombre_columna_xi__)

            self.datos.reset_index(drop=True, inplace=True)

            self.__agrupados__ = True
            self.__yi_en_columnas__ = False
            self.__columna_fa__ = self.__repr_fa__


    def __quitar_indices__(self):

        if type(self) == DatosUnivariada:
            if (self.__xi_es_index__ == True) or (len(self.datos.columns)  == 1 and self.__agrupados__ == True):
                self.__quitar_xi_de_index__()
        
        elif type(self) == DatosBivariada:
            if (self.__xi_es_index__ == True) or (len(self.datos.columns)  == 2 and self.__agrupados__ == True):
                
                self.__quitar_xi_de_index__()
                self.__obtener_nombre_columnas__()
                
                self.__melt_datos__()
        else:
            raise ValueError('type no reconocido')


    def __dar_formato_datos__(self):
        
        if type(self) == DatosUnivariada:
            datos = self.datos
            repr_xi = self.__repr_xi__
            repr_fa = self.__repr_fa__
            
            if type(self.datos) == list:
                
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
        
        else:
            datos = self.datos
            repr_xi = self.__repr_xi__
            repr_yi = self.__repr_yi__
            repr_fa = self.__repr_fa__
            

            if type(datos) == list:
                
                self.datos = pandas.DataFrame(datos)

            elif type(datos) == pandas.Series:
                
                self.datos = pandas.DataFrame(datos.to_list())
                
            
            elif type(datos) == pandas.DataFrame:
                
                self.datos = datos
            else:
                raise ValueError('Solo se acepta Dataframe 2 columnas o lista de tuplas')

    def __obtener_nombre_columnas__(self):

        type_xi = type(self.__columna_xi__)
        type_fa = type(self.__columna_fa__)
        
        #------- obtenemos nombre de columna "xi" -------
        # Si "xi" esta en el index
        if self.__xi_es_index__ == True:
            self.__nombre_columna_xi__ = self.datos.index.name

        else:
            # Si "xi" no esta en el index
            # Si "xi" es string
            if type_xi == str:
                self.__nombre_columna_xi__ = self.__columna_xi__
            
            # Si "xi" no esta en el index
            # Si "xi" es un numero
            else:
                self.__nombre_columna_xi__ = self.datos.iloc[:,self.__columna_xi__].name

            if type(self) == DatosBivariada:
                #------- obtenemos nombre de columna "yi" -------
                # Si "yi" es string

                type_yi = type(self.__columna_yi__)
                if type_yi == str:
                    self.__nombre_columna_yi__ = self.__columna_yi__

                # Si "yi" es un numero
                else:
                    self.__nombre_columna_yi__ = self.datos.iloc[:,self.__columna_yi__].name


        #------- obtenemos nombre de columna "fa" -------
        # Si "fa" es string
        if type_fa == str:
            self.__nombre_columna_fa__ = self.__columna_fa__

        # Si "fa" es un numero
        else:
            self.__nombre_columna_fa__ = self.datos.iloc[:,self.__columna_fa__].name

    def __obtener_xi_yi_fa__(self):
        self.__xi__ = self.datos.loc[: , self.__nombre_columna_xi__]
        self.__fa__ = self.datos.loc[: , self.__nombre_columna_fa__]

        if type(self) == DatosBivariada:
            self.__yi__ = self.datos.loc[: , self.__nombre_columna_yi__]

    def __ordenar_datos__(self):

        if self.__xi_es_index__ == True:
            self.datos.sort_index(inplace=True)

        else:
            if type(self) == DatosUnivariada:
                self.datos.sort_values(self.__nombre_columna_xi__, inplace=True)
            else:
                self.datos.sort_values([self.__nombre_columna_xi__, self.__nombre_columna_yi__], inplace=True)

    def __total_n__(self):

            if self.__agrupados__ == False:
                total_n = len(self.__xi__)
            
            else:
                total_n = self.__fa__.sum()

            return total_n

class DatosUnivariada(DatosEstadisticos):

    def __init__(self, datos, titulo, repr_xi, repr_fa, agrupados=False, columna_xi=0, columna_fa=0, xi_es_index=False, muestra=True):
        
        super().__init__(datos, titulo, repr_xi, repr_fa, agrupados, columna_xi, columna_fa, xi_es_index, muestra)

        self.__dar_formato_datos__()

        self.__quitar_indices__()
        
        self.__obtener_nombre_columnas__()

        self.__obtener_xi_yi_fa__()

        self.__ordenar_datos__()

        self.__total_n__ = self.__total_n__()
                
    def __creacion_intervalos__(self, rango_intervalos):
        '''
        Crea intervalos de los datos proporcionados de acuerdo al rango requerido para los
        intervalos.

        *** solo acepta listas***
        '''

        if type(rango_intervalos) == float:

            len_int = len(str(int(rango_intervalos)))
            len_rango_intervalo = (len(str(rango_intervalos)) - 1) - len_int

        else:
            len_rango_intervalo = rango_intervalos


        maximo_numero_en_rangos = round(ceiling_to_a_number(max(self.__xi__), rango_intervalos), len_rango_intervalo)
        minimo_numero_en_rangos = round(floor_to_a_number(min(self.__xi__), rango_intervalos), len_rango_intervalo)


        distancia_minimo_numero_vs_maximo_numero_en_rangos = round((maximo_numero_en_rangos - \
            minimo_numero_en_rangos), len_rango_intervalo)


        cantidad_intervalos = int(distancia_minimo_numero_vs_maximo_numero_en_rangos / rango_intervalos)

        intervalos = [[
            minimo_numero_en_rangos,
            round((minimo_numero_en_rangos + rango_intervalos), len_rango_intervalo)
        ]]

        for intervalo in range(cantidad_intervalos - 1):
            intervalos.append(
                [intervalos[-1][1], round(((intervalos[-1][1]) + rango_intervalos), len_rango_intervalo)])

        return intervalos

    def __calculo_frecuencias_absolutas__(self, rango_intervalos):
        contar_datos = self.__xi__.value_counts().reset_index()
        contar_datos.columns = [self.__repr_xi__, self.__repr_fa__]
        contar_datos.sort_values(self.__repr_xi__, inplace=True)

        if rango_intervalos == 0:
            
            tabla_intervalos_frecuencias = contar_datos

        else:
            intervalos = pandas.Series(self.__creacion_intervalos__(rango_intervalos), name='intervalos')
            
            ultimo_intervalo = intervalos[len(intervalos)-1]
            
            frecuencias = []

            for intervalo in intervalos:
                conteo = 0
                
                if intervalo == ultimo_intervalo:

                    intervalo_inferior = intervalo[0]
                    intervalo_superior = intervalo[1] + rango_intervalos
                    
                else:
                    intervalo_inferior = intervalo[0]
                    intervalo_superior = intervalo[1]
                    
                #recorriendo xi del conteo de datos
                for i in range(len(contar_datos)):
                    
                    xi = contar_datos.iloc[i][0]
                    fa = contar_datos.iloc[i][1]
                                        
                    if xi >= intervalo_inferior and xi < intervalo_superior:
                        conteo += fa

                total_fa = conteo
                
                #frecuencias.append((intervalo, total_fa))
                frecuencias.append((total_fa))

                #frecuencias_series = pandas.Series(frecuencias, name=self.__nombre_columna_xi__)
                frecuencias_series = pandas.Series(frecuencias, name=self.__repr_fa__)

                tabla_intervalos_frecuencias = pandas.concat([intervalos, frecuencias_series], axis=1)

        return tabla_intervalos_frecuencias

    def agrupar(self, rango_intervalos=0):
        ''''
        Agrupa los datos calculando sus frecuencias absolutas de acuerdo a un rango de intervalo determinado.

        Parametros:
            rango_intervalos.- distancia del intervalo deseado;
                                "0"   = cuenta los datos de cada "xi"
                                "> 0" = agrupa los datos en intervalos de acuerdo al rango especificado 

        '''
        try:
            self.__regresar_backup__()
            
        except:
            self.__crear_backup__()

        datos_intervalos = self.__calculo_frecuencias_absolutas__(rango_intervalos)
        
        self.datos = datos_intervalos

        if rango_intervalos == 0:
            self.__columna_xi__ = self.__repr_xi__
            self.__nombre_columna_xi__ = self.__repr_xi__
            self.__xi__.name = self.__repr_xi__
            self.__xi__ = datos_intervalos[self.__repr_xi__]

        else:
            self.__columna_xi__ = 'intervalos'
            self.__nombre_columna_xi__ = 'intervalos'
            self.__xi__.name = 'intervalos'            
            self.__xi__ = datos_intervalos['intervalos']

        self.datos = datos_intervalos
        self.__columna_fa__ = self.__repr_fa__
        self.__fa__.name = self.__repr_fa__
        self.__nombre_columna_fa__ = self.__repr_fa__
        self.__agrupados__ = True
        self.__fa__ = datos_intervalos[self.__repr_fa__]

        return self

    def _repr_html_(self):
        
        if self.__agrupados__ == False:
            return f'''
            <body>
                <h1>
                    {self.__titulo__}
                </h1>

                <p align="left">
                    <pre><strong><span style="font-size:110%">{'Datos Agrupados' if self.__agrupados__ ==True else 'Datos No Agrupados'}</span></strong></br></pre>
                    <pre><strong><span style="font-size:110%">{'Muestra' if self.__muestra__ ==True else 'Poblacion'}</span></strong></br></pre>
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
            {self.datos._repr_html_()}
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
            {self.datos._repr_html_()}'''

class DatosBivariada(DatosEstadisticos, TablaPivote):
    def __init__(self, datos, titulo, repr_xi, repr_yi, repr_fa, columna_xi, columna_yi, columna_fa=0, muestra=True, agrupados=False, xi_es_index=False, yi_en_columnas=False):
        super().__init__(datos, titulo, repr_xi, repr_fa, agrupados, columna_xi, columna_fa, xi_es_index, muestra)
        
        self.__repr_yi__ = repr_yi
        self.__columna_yi__ = columna_yi
        self.__yi_en_columnas__ = yi_en_columnas
        
        self.__dar_formato_datos__()
        self.__quitar_indices__()
        self.__obtener_nombre_columnas__()
        self.__obtener_xi_yi_fa__()
        self.__ordenar_datos__()

        self.__total_n__ = self.__total_n__()

    def agrupar(self):
        index = None
        totales = False
        tipo = None

        try:
            self.__regresar_backup__()
        
        except:
            self.__crear_backup__()

        tabla_pivote = self.__crear_tabla_pivote__(index= index, tipo=tipo, totales= totales)

        self.__agrupados__ = True

        self.datos = tabla_pivote

        return self

    def _repr_html_(self):

        if self.__agrupados__ == False:
            return f'''
            <body>
                <h1>
                    {self.__titulo__}
                </h1>

                <p align="left">
                    <pre><strong><span style="font-size:110%">{'Datos Agrupados' if self.__agrupados__ ==True else 'Datos No Agrupados'}</span></strong></br></pre>
                    <pre><strong><span style="font-size:110%">{'Muestra' if self.__muestra__ ==True else 'Poblacion'}</span></strong></br></pre>
                    <pre>Total n: <strong><span style="font-size:110%">{self.__total_n__}</span></strong> {self.__repr_fa__}</br></pre>
                </p>

                <table border="1" align="center" cellspacing="0" cellpadding="5">
                    <tr valign="bottom" align="center">
                        <th width="300"><pre><span style="font-size:110%">Variable Aleatoria (Xi)</span></br></pre></pre></th>
                        <th width="300"><pre><span style="font-size:110%">Variable Aleatoria (yi)</span></br></pre></pre></th>
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
                                <td> Representa:</td>
                                <td><strong> {self.__repr_yi__}</strong></td>
                                </tr>
                                <tr>
                                <td> Columna yi:</td>
                                <td><strong> {self.__nombre_columna_yi__}</strong></td>
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
            {self.datos._repr_html_()}
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
                        <th width="300"><pre><span style="font-size:110%">Variable Aleatoria (yi)</span></br></pre></pre></th>
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
                                <td><strong> {self.__repr_yi__}</strong></td>
                                </tr>
                                <tr>
                                <td> Columna Xi:</td>
                                <td><strong> {self.__nombre_columna_yi__}</strong></td>
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
            {self.datos._repr_html_()}'''




class Analisis(Backup):

    def __init__(self, datos):
        
        self.datos = datos

    def __copiar_backup__(self,datos):

        self.__datos_backup__ = datos.__datos_backup__
        self.__columna_xi_backup__ = datos.__columna_xi_backup__
        self.__nombre_columna_xi_backup__ = datos.__nombre_columna_xi_backup__
        self.__xi_name_backup__ = datos.__xi_name_backup__
        self.__columna_fa_backup__ = datos.__columna_fa_backup__
        self.__fa_name_backup__ = datos.__fa_name_backup__
        self.__nombre_columna_fa_backup__ = datos.__nombre_columna_fa_backup__
        self.__agrupados_backup__ = datos.__agrupados_backup__
        self.__xi_backup__ = datos.__xi_backup__
        self.__fa_backup__ = datos.__fa_backup__

        if type(self) == DatosBivariada or type(self) == AnalisisBivariada:
            
            self.__yi_en_columnas_backup__ = datos.__yi_en_columnas_backup__
            self.__columna_yi_backup__ = datos.__columna_yi_backup__
            self.__nombre_columna_yi_backup__ = datos.__nombre_columna_yi_backup__
            self.__yi_name_backup__ = datos.__yi_name_backup__
            self.__yi_backup__ = datos.__yi_backup__        

    def __copiar_parametros__(self,datos):
            
            try:
                self.__copiar_backup__()
            
            except:
                pass

            self.__datos__ = datos.datos
            self.__titulo__ = datos.__titulo__
            self.__agrupados__ = datos.__agrupados__
            self.__xi_es_index__ = datos.__xi_es_index__
            self.__muestra__ = datos.__muestra__
            self.__columna_xi__ = datos.__columna_xi__
            self.__repr_xi__ = datos.__repr_xi__
            self.__nombre_columna_xi__ = datos.__nombre_columna_xi__
            self.__xi__ = datos.__xi__
            self.__columna_fa__ = datos.__columna_fa__
            self.__repr_fa__ = datos.__repr_fa__
            self.__nombre_columna_fa__ = datos.__nombre_columna_fa__
            self.__fa__ = datos.__fa__
            self.__total_n__ = datos.__total_n__
            
            if type(self) == AnalisisUnivariada:

                pass                

            elif type(self) ==  AnalisisBivariada:
                
                self.__yi_en_columnas__ = datos.__yi_en_columnas__
                self.__repr_yi__ = datos.__repr_yi__
                self.__columna_yi__ = datos.__columna_yi__
                self.__nombre_columna_yi__ = datos.__nombre_columna_yi__
                self.__yi__ = datos.__yi__      

            else:
                raise ValueError('Type no reconocido')      

    def __crear_tabla_estadistica__(self):

        '''Crea tabla estadistica sin Xi en index'''

        self.tabla_estadistica = self.__datos__.reset_index().copy() if self.__xi_es_index__ == True else self.__datos__.copy()
        self.__xi_es_index__ = False

    def __establecer_nombres_columnas_estadisticas__(self):
        self.__nombres_columnas_estadisticas__ = {
                        'mc': 'MC', 
                        'faa': 'FAA', 
                        'fr': 'FR', 
                        'fra': 'FRA', 
                        'xi2': 'Xi2', 
                        'xi*ni': 'Xi*Ni', 
                        'xi2*ni': 'Xi2*Ni', 
                        'xi-media': 'Xi-Media', 
                        'ni*(xi-media)2': 'Ni*(Xi-Media)2', 
                        'ni*(xi-media)3': 'Ni*(Xi-Media)3', 
                        'ni*(xi-media)4': 'Ni*(Xi-Media)4',
                        'yi2': 'Yi2',
                        'xiyi': 'Xi*Yi',
                        'yi*ni': 'Yi*Ni',
                        'yi2*ni': 'Yi2*Ni',
                        'xi*yi*ni': 'Xi*Yi*Ni'

                        }

    def __creacion_columnas_estadisticas__(self):
            
        fa = self.__fa__
        total_n = self.__total_n__

        if type(self) == AnalisisUnivariada:
            self.__mc__ = self.__calculo_marcas_clase__()

            es_rango =   self.__es_rango__()            
            media =      self.media
            xi =         self.tabla_estadistica[self.__nombre_columna_xi__] if es_rango == False else self.tabla_estadistica[self.__nombres_columnas_estadisticas__['mc']]
            xi2 =        self.tabla_estadistica[self.__nombres_columnas_estadisticas__['xi2']] = xi ** 2
            xi_menos_media =        self.tabla_estadistica[self.__nombres_columnas_estadisticas__['xi-media']] = xi - media

            # Cuando son datos agrupados no existen frecuencias absolutas
            if self.__agrupados__ == False:
                faa =     None
                fr =      None
                fra =     None
                nixi =   None   
                nixi2 =  None
                xi_menos_media_por_ni_exp_2 = None
                xi_menos_media_por_ni_exp_3 = None
                xi_menos_media_por_ni_exp_4 = None

            # Columnas para datos agrupados
            else:
                faa =                   self.tabla_estadistica[self.__nombres_columnas_estadisticas__['faa']] = fa.cumsum()
                fr =                    self.tabla_estadistica[self.__nombres_columnas_estadisticas__['fr']] = fa / total_n
                fra =                   self.tabla_estadistica[self.__nombres_columnas_estadisticas__['fra']] = fr.cumsum()
                nixi =                  self.tabla_estadistica[self.__nombres_columnas_estadisticas__['xi*ni']] = xi * fa
                nixi2 =                 self.tabla_estadistica[self.__nombres_columnas_estadisticas__['xi2*ni']] = xi2 * fa
                

                # Dataframe de xi-media y ni para formula .apply
                xi_menos_media_ni_df = self.tabla_estadistica[[self.__nombres_columnas_estadisticas__['xi-media'], self.__nombre_columna_fa__]]
                
                xi_menos_media_por_ni_exp_2 = self.tabla_estadistica[self.__nombres_columnas_estadisticas__['ni*(xi-media)2']] = xi_menos_media_ni_df.apply(self.__xi_menos_media_por_ni_exponencial__, args=[2], axis='columns')
                xi_menos_media_por_ni_exp_3 = self.tabla_estadistica[self.__nombres_columnas_estadisticas__['ni*(xi-media)3']] = xi_menos_media_ni_df.apply(self.__xi_menos_media_por_ni_exponencial__, args=[3], axis='columns')
                xi_menos_media_por_ni_exp_4 = self.tabla_estadistica[self.__nombres_columnas_estadisticas__['ni*(xi-media)4']] = xi_menos_media_ni_df.apply(self.__xi_menos_media_por_ni_exponencial__, args=[4], axis='columns')
            
            
            self.__faa__ = faa
            self.__fr__ = fr
            self.__fra__ = fra
            self.__xi2__ = xi2
            self.__nixi__ = nixi
            self.__nixi2__ = nixi2
            self.__xi_menos_media__ = xi_menos_media
            self.__xi_menos_media2_por_ni__ = xi_menos_media_por_ni_exp_2
            self.__xi_menos_media3_por_ni__ = xi_menos_media_por_ni_exp_3
            self.__xi_menos_media4_por_ni__ = xi_menos_media_por_ni_exp_4
        
        elif type(self) == AnalisisBivariada:
            xi =         self.tabla_estadistica[self.__nombre_columna_xi__]
            yi =         self.tabla_estadistica[self.__nombre_columna_yi__]
            
            # el Try es por si los datos de xi y yi no son numericos
            try:
                
                xi2 =           self.tabla_estadistica[self.__nombres_columnas_estadisticas__['xi2']] = xi ** 2
                yi2 =           self.tabla_estadistica[self.__nombres_columnas_estadisticas__['yi2']] = yi ** 2
                xiyi =          self.tabla_estadistica[self.__nombres_columnas_estadisticas__['xiyi']] = xi * yi
                
                

                if self.__agrupados__ == True:

                    xi_ni =         self.tabla_estadistica[self.__nombres_columnas_estadisticas__['xi*ni']]     = xi * fa
                    xi_ni2 =        self.tabla_estadistica[self.__nombres_columnas_estadisticas__['xi2*ni']]    = xi2 * fa

                    yi_ni =         self.tabla_estadistica[self.__nombres_columnas_estadisticas__['yi*ni']]     = yi * fa
                    yi_ni2 =        self.tabla_estadistica[self.__nombres_columnas_estadisticas__['yi2*ni']]    = yi2 * fa
                    
                    xi_yi_ni =      self.tabla_estadistica[self.__nombres_columnas_estadisticas__['xi*yi*ni']]  = xi * yi * fa
                    




            except:
                print('No se pudieron calcular columnas de frecuencias por contener datos no numericos')
                pass
        
        else:
            raise ValueError('El type recibido no es DatosUnivariada ni DatosBivariada, revisar')

    @property
    def media(self):
        try: 
            xi = self.__xi__
            ni = self.__fa__        
            total_n = self.__total_n__

            if self.__agrupados__ == False:

                media_xi = xi.mean()

            else:
                
                #Si los datos estan agrupados por rangos
                if type(self) == AnalisisUnivariada:
                    if self.__mc__ is not None:
                        xi = self.__mc__

                sumatoria_ni_xi = (ni * xi).sum()

                media_xi = sumatoria_ni_xi / total_n
                
            if type(self) == AnalisisUnivariada:
                return media_xi
            
            if type(self) == AnalisisBivariada:
                yi = self.__yi__

                if self.__agrupados__ == False:
                    media_yi = yi.mean()
                
                else:

                    sumatoria_ni_yi = (ni* yi).sum()

                    media_yi = sumatoria_ni_yi / total_n

                return media_xi, media_yi
        
        except:
            
            raise ValueError('No se puede calcular la media de datos no numericos.')

    @property
    def varianza(self):
        muestra = self.__muestra__
        
        xi =            self.tabla_estadistica[self.__nombre_columna_xi__]
        
        n =             self.__total_n__
        media =         self.media

        if type(self) == AnalisisBivariada:
            media_xi =  media[0]
            media_yi =  media[1]
            yi =        self.tabla_estadistica[self.__nombre_columna_yi__]
            
            if self.__agrupados__ == True:
                #raise ValueError('Aun no se crea la formula para varianza para datos agrupados para AnalisisBivariada.')
                nixi2 = self.tabla_estadistica[self.__nombres_columnas_estadisticas__['xi2*ni']]
                niyi2 = self.tabla_estadistica[self.__nombres_columnas_estadisticas__['yi2*ni']]

                varianza_xi = ((nixi2.sum() / n) - (media_xi ** 2))
                varianza_yi = ((niyi2.sum() / n) - (media_yi ** 2))

            else:
                if muestra == True:
                    varianza_xi = variance(xi)
                    varianza_yi = variance(yi)
                else:
                    varianza_xi = pvariance(xi)
                    varianza_yi = pvariance(yi)

            return varianza_xi, varianza_yi

        else:            

            if self.__agrupados__ == True:

                
                nixi2 =     self.tabla_estadistica[self.__nombres_columnas_estadisticas__['xi2*ni']]
                varianza_xi =  ((nixi2.sum() / n) - (media ** 2))
                

            else:
                if muestra == True:
                    varianza_xi = variance(xi)
                else:
                    varianza_xi = pvariance(xi)
        

            return varianza_xi


    @property
    def desviacion_estandar(self):
        if type(self) == AnalisisBivariada:
            stdev_xi = self.varianza[0] ** .5
            stdev_yi = self.varianza[1] ** .5

            return stdev_xi, stdev_yi
        
        else:
            stdev_xi = self.varianza ** .5

            return stdev_xi


class AnalisisUnivariada(Analisis):
    def __init__(self, datos):
        
        super().__init__(datos)

        self.__copiar_parametros__(datos)

        self.__establecer_nombres_columnas_estadisticas__()

        self.__crear_tabla_estadistica__()

        self.__creacion_columnas_estadisticas__()

        self.__ordenar_datos__()

        self.__ordenar_columnas__()

    def __ordenar_datos__(self):

        if self.__xi_es_index__ == True:
            self.tabla_estadistica.sort_index(inplace=True)

        else:
            self.tabla_estadistica.sort_values(self.__nombre_columna_xi__, inplace=True)

    def __ordenar_columnas__(self):
        agrupados = self.__agrupados__
        es_rango = self.__es_rango__()

        # Datos agrupados
        if agrupados == True:

            # No es rango
            if es_rango == True:
                self.tabla_estadistica = self.tabla_estadistica[[
                    self.__nombre_columna_xi__, 
                    self.__nombre_columna_fa__,
                    self.__nombres_columnas_estadisticas__['faa'],
                    self.__nombres_columnas_estadisticas__['fr'],
                    self.__nombres_columnas_estadisticas__['fra'],
                    self.__nombres_columnas_estadisticas__['mc'],
                    self.__nombres_columnas_estadisticas__['xi2'],
                    self.__nombres_columnas_estadisticas__['xi*ni'],
                    self.__nombres_columnas_estadisticas__['xi2*ni'],
                    self.__nombres_columnas_estadisticas__['xi-media'],
                    self.__nombres_columnas_estadisticas__['ni*(xi-media)2'],
                    self.__nombres_columnas_estadisticas__['ni*(xi-media)3'],
                    self.__nombres_columnas_estadisticas__['ni*(xi-media)4']
                ]]

            # Es rango
            else:
                self.tabla_estadistica = self.tabla_estadistica[[
                    self.__nombre_columna_xi__, 
                    self.__nombre_columna_fa__,
                    self.__nombres_columnas_estadisticas__['faa'],
                    self.__nombres_columnas_estadisticas__['fr'],
                    self.__nombres_columnas_estadisticas__['fra'],
                    self.__nombres_columnas_estadisticas__['xi2'],
                    self.__nombres_columnas_estadisticas__['xi*ni'],
                    self.__nombres_columnas_estadisticas__['xi2*ni'],
                    self.__nombres_columnas_estadisticas__['xi-media'],
                    self.__nombres_columnas_estadisticas__['ni*(xi-media)2'],
                    self.__nombres_columnas_estadisticas__['ni*(xi-media)3'],
                    self.__nombres_columnas_estadisticas__['ni*(xi-media)4']
                ]]
        
        # Datos no agrupados
        else:
            self.tabla_estadistica = self.tabla_estadistica[[
                    self.__nombre_columna_xi__,                    
                    self.__nombres_columnas_estadisticas__['xi2'],
                    self.__nombres_columnas_estadisticas__['xi-media'],
                ]]
                
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

    def __es_rango__(self):
        
        xi = self.__xi__
        
        try:
            es_rango = True if (type(xi.iloc[0]) is list or type(xi.iloc[0]) is tuple) else False
            
        except:
            es_rango = True if (type(xi[0]) is list or type(xi[0]) is tuple) else False

        return es_rango

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
            
            self.tabla_estadistica[self.__nombres_columnas_estadisticas__['mc']] = xi
            
            self.tabla_estadistica[self.__nombres_columnas_estadisticas__['mc']] = self.tabla_estadistica[self.__nombres_columnas_estadisticas__['mc']].apply(self.__marca_clase__)

            marcas_de_clase = self.tabla_estadistica[self.__nombres_columnas_estadisticas__['mc']]

        else:
            marcas_de_clase = None
        
        return marcas_de_clase

    def __encontrar_index_mediana_datos_agrupados__(self):
        
        mitad_faa = self.__total_n__ / 2

        index_clase_mediana = 0
        
        while True:
            if self.tabla_estadistica.iloc[index_clase_mediana].loc[self.__nombres_columnas_estadisticas__['faa']] < mitad_faa:
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
                if self.tabla_estadistica.iloc[index_clase_cuantil].loc[self.__nombres_columnas_estadisticas__['faa']] < cuantil_a_buscar:
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
            
            fisher = self.tabla_estadistica[[self.__nombres_columnas_estadisticas__['mc'], self.__nombre_columna_fa__]].apply(self.__sumatoria_xi_menos_media_por_ni_al_cubo__, args=[self.media], axis='columns')
        
        else:
            
            fisher = self.tabla_estadistica[[self.__nombre_columna_xi__, self.__nombre_columna_fa__]].apply(self.__sumatoria_xi_menos_media_por_ni_al_cubo__, args=[self.media], axis='columns')
        
        fisher = sum(fisher) / (N * (s ** 3))
        
        return fisher

    def __xi_menos_media_por_ni_exponencial__(self, dataframe, exponente):
        xi_menos_media = dataframe[0]
        
        ni = dataframe[1]
        
        resultado = (xi_menos_media ** exponente) * ni
        
        return resultado


    '''@property
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
            sumatoria_ni_xi = (ni * xi).sum()

            media = sumatoria_ni_xi / sumatoria_ni
        
        return media'''

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
                if index_mediana == 0:
                    faa_intervalo_mediana_anterior = 0
                else:                    
                    faa_intervalo_mediana_anterior = self.tabla_estadistica.iloc[index_mediana-1].loc[self.__nombres_columnas_estadisticas__['faa']]
                
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
                if index_moda ==0:
                    fa_intervalo_modal_anterior = 0
                else:
                    fa_intervalo_modal_anterior = self.tabla_estadistica.iloc[iloc_moda-1].loc[self.__nombre_columna_fa__]
                
                if index_moda == len(self.tabla_estadistica.index)-1:
                    fa_intervalo_modal_siguiente = 0
                else:
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

    '''@property
    def varianza(self):
        muestra = self.__muestra__
        
        xi = self.__xi__
        nixi2 = self.__nixi2__
        n = self.__total_n__
        media = self.media

        if self.__agrupados__ == True:
            varianza = ((sum(nixi2) / n) - (media ** 2))
            

        else:
            if muestra == True:
                varianza = variance(xi)
            else:
                varianza = pvariance(xi)
        
        return varianza'''

    '''@property
    def desviacion_estandar(self):

        stdev = self.varianza ** .5

        return stdev'''

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
            
            As = sumatoria_xi_menos_media_al_cubo / (n * (s**3))
        
        # Datos Agrupados
        else:
            
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
        muestra = self.__muestra__

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
            <pre><strong><span style="font-size:120%">{'Muestra' if muestra == True else 'Poblacion'}</span></strong></br></pre>
            <pre>Total n : <strong><span style="font-size:90%">{total_n} {self.__repr_fa__}</span></strong></br></pre>
            </br>
            <pre><strong><span style="font-size:120%">Variable Aleatoria "Xi": ({self.__repr_xi__})</span></strong></br></pre>
            <pre>media:                        <strong><span style="font-size:90%">{round(media, 4)}</span></strong></br></pre>
            <pre>mediana:                      <strong><span style="font-size:90%">{round(mediana, 4)}</span></strong></br></pre>
            <pre>moda:                         <strong><span style="font-size:90%">{round(moda, 4)}</span></strong></br></pre>
            <pre>rango recorrido:              <strong><span style="font-size:90%">{rango_recorrido if type(rango_recorrido) == str else round(rango_recorrido, 4)}</span></strong></br></pre>
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
                    if index_cuantiles[nombre_index_cuantil] == 0:
                        faa_intervalo_cuantil_anterior = 0
                    else:
                        faa_intervalo_cuantil_anterior = self.tabla_estadistica.iloc[index_cuantiles[nombre_index_cuantil]-1].loc[self.__nombres_columnas_estadisticas__['faa']]
                    
                    
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
            mascara = self.tabla_estadistica[self.__nombres_columnas_estadisticas__['fra']] > percentil_objetivo
            index_resultado = self.tabla_estadistica[mascara].index.min()

            resultado = self.tabla_estadistica.loc[index_resultado][[self.__nombre_columna_xi__, self.__nombres_columnas_estadisticas__['faa'], self.__nombres_columnas_estadisticas__['fra']]]

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
        <pre>El <strong>25%</strong> de "{titulo}" se encuentran entre <strong>{round(bigote_inferior, 4)}</strong> y <strong>{round(q1, 4)} {self.__repr_xi__}</strong></br></pre>
        <pre>El <strong>50%</strong> de "{titulo}" se encuentran entre <strong>{round(bigote_inferior, 4)}</strong> y <strong>{round(q2, 4)} {self.__repr_xi__}</strong></br></pre>
        <pre>El <strong>75%</strong> de "{titulo}" se encuentran en menos de <strong>{round(q3, 4)} {self.__repr_xi__}</strong></br></pre>
        </br>
        <pre><strong><span style="font-size:120%">Centro de datos:</span></strong></br></pre>
        <pre>El <strong>50%</strong> de "{titulo}" se encuentran entre <strong>{round(q1, 4)}</strong> y <strong>{round(q3, 4)} {self.__repr_xi__}</strong></br></pre>
        </br>
        <pre>El <strong>75%</strong> de "{titulo}" se encuentran en mas de <strong>{round(q1, 4)} {self.__repr_xi__}</strong></br></pre>
        <pre>El <strong>50%</strong> de "{titulo}" se encuentan en mas de <strong>{round(q2, 4)} {self.__repr_xi__}</strong></pre>
        <pre>El <strong>25%</strong> de "{titulo}" se encuentran entre <strong>{round(q3, 4)}</strong> y <strong>{round(bigote_superior, 4)} {self.__repr_xi__}</strong></br></pre>
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
                    <pre><strong><span style="font-size:110%">{'Muestra' if self.__muestra__ ==True else 'Poblacion'}</span></strong></br></pre>
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
                    <pre><strong><span style="font-size:110%">{'Muestra' if self.__muestra__ ==True else 'Poblacion'}</span></strong></br></pre>
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

class AnalisisBivariada(Analisis, TablaPivote):

    def __init__(self, datos):
        
        super().__init__(datos)

        self.__copiar_parametros__(datos)
        
        self.__crear_tabla_estadistica__()

        self.__establecer_nombres_columnas_estadisticas__()

        self.__creacion_columnas_estadisticas__()

        
    def tabla_pivote(self, index, totales=False, tipo=None):
        
        try:
            self.__regresar_backup__()
        
        except:
            self.__crear_backup__()

        tabla_pivote = self.datos.__crear_tabla_pivote__(index= index, tipo= tipo , totales= totales)

        self.__agrupados__ = True

        self.tabla_estadistica = tabla_pivote

        
        return self

    @property
    def covarianza(self):
        n =          self.__total_n__

        if self.__agrupados__ == False:
            xi =         self.tabla_estadistica[self.__nombre_columna_xi__]
            yi =         self.tabla_estadistica[self.__nombre_columna_yi__]
            xiyi =       self.tabla_estadistica[self.__nombres_columnas_estadisticas__['xiyi']]
            

            media_xi =  self.media[0]
            media_yi =  self.media[1]

            suma_xiyi = xiyi.sum()
        
        else:

            xi_yi_ni =      self.tabla_estadistica[self.__nombres_columnas_estadisticas__['xi*yi*ni']]

            suma_xiyi =    xi_yi_ni.sum()
            media_xi = self.media[0]
            media_yi = self.media[1]

        covarianza = (suma_xiyi / n) - (media_xi * media_yi)

        return covarianza
    @property
    def correlacion(self):
        
        covarianza = self.covarianza
        stdev_xi = self.desviacion_estandar[0]
        stdev_yi = self.desviacion_estandar[1]

        correlacion = covarianza / (stdev_xi * stdev_yi)

        return correlacion


    def _repr_html_(self):

        if self.__agrupados__ == False:
            return f'''
            <body>
                <h1>
                    {self.__titulo__}
                </h1>

                <p align="left">
                    <pre><strong><span style="font-size:110%">{'Datos Agrupados' if self.__agrupados__ ==True else 'Datos No Agrupados'}</span></strong></br></pre>
                    <pre><strong><span style="font-size:110%">{'Muestra' if self.__muestra__ ==True else 'Poblacion'}</span></strong></br></pre>
                    <pre>Total n: <strong><span style="font-size:110%">{self.__total_n__}</span></strong> {self.__repr_fa__}</br></pre>
                </p>

                <table border="1" align="center" cellspacing="0" cellpadding="5">
                    <tr valign="bottom" align="center">
                        <th width="300"><pre><span style="font-size:110%">Variable Aleatoria (Xi)</span></br></pre></pre></th>
                        <th width="300"><pre><span style="font-size:110%">Variable Aleatoria (yi)</span></br></pre></pre></th>
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
                                <td> Representa:</td>
                                <td><strong> {self.__repr_yi__}</strong></td>
                                </tr>
                                <tr>
                                <td> Columna yi:</td>
                                <td><strong> {self.__nombre_columna_yi__}</strong></td>
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
                        <th width="300"><pre><span style="font-size:110%">Variable Aleatoria (yi)</span></br></pre></pre></th>
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
                                <td><strong> {self.__repr_yi__}</strong></td>
                                </tr>
                                <tr>
                                <td> Columna Xi:</td>
                                <td><strong> {self.__nombre_columna_yi__}</strong></td>
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



class PruebasCajaCristal(unittest.TestCase):
    
    # No agrupados
    def test_media_no_agrupados(self):
        resultado = ae_longitud.media
        self.assertEqual(round(resultado,4), 13.4498)
    
    def test_mediana_no_agrupados(self):
        resultado = ae_longitud.mediana
        self.assertEqual(round(resultado,4), 13.453)

    def test_moda_no_agrupados(self):
        resultado = ae_longitud.moda
        self.assertEqual(round(resultado,4), 13.455)

    def test_varianza_no_agrupados(self):
        resultado = ae_longitud.varianza
        self.assertEqual(round(resultado,4), 0.0002)
    
    def test_desviacion_estandar_no_agrupados(self):
        resultado = ae_longitud.desviacion_estandar
        self.assertEqual(round(resultado,4), 0.0136)

    def test_rango_recorrido_no_agrupados(self):
        resultado = ae_longitud.rango_recorrido
        self.assertEqual(round(resultado,4), 0.061)

    def test_cuartil1_no_agrupados(self):
        resultado = ae_longitud.cuantiles()['Q1']
        self.assertEqual(round(resultado,3), 13.445)

    def test_cuartil3_no_agrupados(self):
        resultado = ae_longitud.cuantiles()['Q3']
        self.assertEqual(round(resultado,3), 13.457)

    def test_decil9_no_agrupados(self):
        resultado = ae_longitud.cuantiles(n=10)['Q9']
        self.assertEqual(round(resultado,4), 13.4615)


    # Agrupados sin Intervalos
    def test_media_agrupados(self):
        resultado = ae_longitud_agrupados.media
        self.assertEqual(round(resultado,4), 13.4498)
    
    def test_asimetria_pearson_agrupados(self):
        resultado = ae_longitud_agrupados.coeficiente_pearson
        self.assertEqual(round(resultado,4), -0.3975)
    
    def test_medida_fisher_agrupados(self):
        resultado = ae_longitud_agrupados.medida_fisher
        self.assertEqual(round(resultado,4), -2.4338)


    # Agrupados con Intervalos
    def test_media_intervalos(self):
        resultado = ae_ejemplo_intervalos.media
        self.assertEqual(round(resultado,2), 21.88)

    def test_varianza_intervalos(self):
        resultado = ae_ejemplo_intervalos.varianza
        self.assertEqual(round(resultado,2), 59.12)

    def test_desviacion_estandar_intervalos(self):
        resultado = ae_ejemplo_intervalos.desviacion_estandar
        self.assertEqual(round(resultado,2), 7.69)

    def test_mediana_intervalos(self):
        resultado = ae_ejemplo_intervalos.mediana
        self.assertEqual(round(resultado,4), 21.0625)
    
    def test_cuartil1_intervalos(self):
        resultado = ae_ejemplo_intervalos.cuantiles()['Q1']
        self.assertEqual(round(resultado,2), 16.21)

    def test_cuartil3_intervalos(self):
        resultado = ae_ejemplo_intervalos.cuantiles()['Q3']
        self.assertEqual(round(resultado,2), 24.97)

    def test_percentil10_intervalos(self):
        resultado = ae_ejemplo_intervalos.cuantiles(n=100)['Q10']
        self.assertEqual(round(resultado,2), 12.60)

    def test_asimetria_fisher_intervalos(self):
        resultado = ae_ejemplo_intervalos.medida_fisher
        self.assertEqual(round(resultado,2), 1.03)

if '__main__' == __name__:

    # Ejemplo sin intervalos
    longitud = pandas.Series(
        [13.404, 13.443, 13.445, 13.447, 13.449, 13.450, 13.453, 13.455, 
        13.457, 13.460, 13.460, 13.465, 13.455, 13.453, 13.445, 13.455], name='metros')

    longitud = DatosUnivariada(longitud, 'Mediciones de la longitud de dos puntos', repr_xi='metros', repr_fa='mediciones')
    ae_longitud = AnalisisUnivariada(longitud)
    ae_longitud_agrupados = AnalisisUnivariada(longitud.agrupar(0))

    # Ejemplo con intervalos
    intervalos_ejemplo = pandas.Series([(10,15), (15, 20), (20, 25), (25, 30), (30, 35), (35, 40), (40, 45), (45, 50)], name= 'Intervalos')
    ni_ejemplo = pandas.Series([48, 60, 80, 30, 13, 10, 6, 3], name= 'ni')
    ejemplo_intervalos = pandas.concat([intervalos_ejemplo, ni_ejemplo], axis='columns')
    de_ejemplo_intervalos = DatosUnivariada(ejemplo_intervalos, 'Ejemplo Intervalos', repr_xi='rango intervalos', repr_fa='ni', columna_xi='Intervalos', columna_fa='ni', agrupados=True)
    ae_ejemplo_intervalos = AnalisisUnivariada(de_ejemplo_intervalos)



    unittest.main()