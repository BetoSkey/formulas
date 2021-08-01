# Archivo terminado con una clase para realizar metodos binarios 
# y utilizarlos en diferentes formulas por ejemplo las formulas etadisticas.


import unittest


class Metodo_binario:
    '''Clase para aplicar metodos binarios:
        *** Recibe una lista de numeros ***
        
    Metodos:
    
        * ordenar = ordena los datos con el metodo de ordenamiento por insercion binaria
        * ubicar = regresa la ubicacion de la posicion donde se encuentra o deberia encontrarse algun numero
        * buscar = regresa True or False en caso que el numero se encuentre o no se encuentre
    '''
    def __init__(self, datos):
        self.datos = datos

    def __verificacion_ubicacion__(self, objetivo, datos, ubicacion_a_verificar):
        '''Verifica si el numero encontrado es =, < o > que el numero en la ubicacion'''
        
        # si el numero buscado es mayor al de la ubicacion encontrada pero 
        # la ubicacion encontrada es el ultimo dato de la lista
        if objetivo > datos[ubicacion_a_verificar] and ubicacion_a_verificar == len(datos)-1:
            return ubicacion_a_verificar
        
        # si el objetivo es mayor que que la ubicacion encontrada
        elif objetivo > datos[ubicacion_a_verificar]:
            return ubicacion_a_verificar +1
        
        # si el objetivo es menoro igual que la ubicacion encontrada
        else:
            return ubicacion_a_verificar
    
    def ubicacion(self, objetivo, datos=None, comienzo=0, final=None, ubicacion_meta=0):
        '''Regresa la posicion donde deberia encontrarse el numero objetivo'''
        if final == None:
            datos = self.ordenar()
            final = len(datos)

        if final-comienzo == 1:  # Si la datos se acoto a dos ubicaciones
            
            try:
                if objetivo > datos[final]:

                    if final + 1 > len(datos)-1:
                        ubicacion_meta = len(datos)-1
                    else:
                        ubicacion_meta = final

                    return self.__verificacion_ubicacion__(objetivo, datos, ubicacion_meta)

                elif objetivo < datos[comienzo]:
                    ubicacion_meta = comienzo

                    return self.__verificacion_ubicacion__(objetivo, datos, ubicacion_meta)
            
            except:
                
                if objetivo > datos[final-1]:

                    if final + 1 > len(datos)-1:
                        ubicacion_meta = len(datos)-1
                    else:
                        ubicacion_meta = final

                    return self.__verificacion_ubicacion__(objetivo, datos, ubicacion_meta)

                elif objetivo < datos[comienzo]:
                    ubicacion_meta = comienzo

                    return self.__verificacion_ubicacion__(objetivo, datos, ubicacion_meta)
                
                else:
                    ubicacion_meta = comienzo
                    return self.__verificacion_ubicacion__(objetivo, datos, ubicacion_meta)
                
        if comienzo == final:  # Si la datos llego al final de su acote y solo nos indica una ubicacion

            # Si el objetivo no se encontro y es mayor que el acotamiento final
            if objetivo > datos[final]:
                # Si la ubicacion meta es mas grande que la datos completa
                if final + 1 > len(datos)-1:
                    ubicacion_meta = len(datos)-1

                else:
                    
                    ubicacion_meta = final + 1

            # Si estamos al principio de la datos o el objetivo es igual que el acotamiento final
            elif comienzo == 0 or objetivo == datos[final]:
                pass

            else:
                ubicacion_meta += 1

            return self.__verificacion_ubicacion__(objetivo, datos, ubicacion_meta)

        # Aqui empieza a acotar la buscar
        medio = (comienzo + final) // 2  # Se acota la datos a la mitad

        if objetivo == datos[medio]:  # Si el objetivo se encontro en la mitad
            return medio

        elif objetivo > datos[medio]:  # Si el objetivo es mayor que la mitad
            ubicacion_meta = medio
            return self.ubicacion(datos=datos, comienzo=medio + 1, final=final, objetivo=objetivo, ubicacion_meta=ubicacion_meta)

        else:  # Si el objetivo es menor que la mitad
            return self.ubicacion(datos=datos, comienzo=comienzo, final=medio - 1, objetivo=objetivo, ubicacion_meta=ubicacion_meta)

    def ordenar(self):
        '''Regresa la lista ordenada por medio de ordenamiento de insercion binaria'''
        datos = self.datos
        lista_ordenada = [datos[0]]
        lista_desordenada = datos[1:]
        n_lista_ordenada = len(lista_ordenada)-1
        n_lista_desordenada = len(lista_desordenada)-1

        # Por cada ubicacion de la datos desordenada
        for ubicacion_en_lista_desordenada in range(n_lista_desordenada+1):

            # Encuentra la ubicacion en la datos ordenada
            ubicacion = self.ubicacion(
                datos=lista_ordenada, comienzo=0, final=n_lista_ordenada, objetivo=lista_desordenada[ubicacion_en_lista_desordenada])

            # Si el numero desordenado es mayor que el de la ubicacion encontrada
            if lista_desordenada[ubicacion_en_lista_desordenada] > lista_ordenada[ubicacion]:

                # Si la ubicacion encontrada es igual que el final de la datos, se agrega al final
                if ubicacion == n_lista_ordenada:
                    lista_ordenada.append(
                        lista_desordenada[ubicacion_en_lista_desordenada])

                # Si el numero no esta al final de la datos, se inserta en la siguiente ubicacion encontrada
                else:
                    lista_ordenada.insert(
                        ubicacion + 1, lista_desordenada[ubicacion_en_lista_desordenada])
                n_lista_ordenada += 1

            # Si el numero desordenado es menor o igual que el de la ubicacion encontrada
            else:
                lista_ordenada.insert(
                    ubicacion, lista_desordenada[ubicacion_en_lista_desordenada])
                n_lista_ordenada += 1

        return lista_ordenada

    def buscar(self, objetivo, comienzo=0, final=None):
        '''Regresa True or False si el numero objetivo se encuentra dentro de la lista'''
        if final == None:
            final = len(self.datos)

        lista_ordenada = self.ordenar()

        if comienzo > final:
            return False
        medio = (comienzo + final) // 2
        if lista_ordenada[medio] == objetivo:
            return medio
        elif lista_ordenada[medio] < objetivo:
            return self.buscar(objetivo, comienzo=medio + 1, final=final)
        else:
            return self.buscar(objetivo, comienzo=comienzo, final=medio - 1)


class Pruebas_caja_cristal(unittest.TestCase):

    def test_ubicacion_binaria(self):
        formula_ubicacion_binaria = busqueda1.buscar(62)

        self.assertEqual(formula_ubicacion_binaria, 2)

    def test_ordenar_lista(self):
        formula_ordenar_lista = busqueda1.ordenar()

        self.assertEqual(formula_ordenar_lista, [55, 59, 62, 70, 74, 82, 87])

    def test_buscar_ubicacion(self):
        formula_buscar_ubicacion = busqueda1.buscar(87)

        self.assertEqual(formula_buscar_ubicacion, 6)
    
    def test_ubicacion_binaria2(self):
        formula_ubicacion_binaria = busqueda_lista2_ordenada.ubicacion(24)
        
        self.assertEqual(formula_ubicacion_binaria, 2)


if '__main__' == __name__:

    lista1 = [55, 87, 74, 70, 82, 62, 59]
    busqueda1 = Metodo_binario(lista1)
    
    lista2 = [39, 50, 3, 19, 49]
    busqueda2 = Metodo_binario(lista2)
    lista2_ordenada = busqueda2.ordenar()
    busqueda_lista2_ordenada = Metodo_binario(lista2_ordenada)
    
    
    unittest.main()
