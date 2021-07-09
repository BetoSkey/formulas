# importar de un directorio paralelo
# *** se tiene que crear un archivo __init__.py en blanco dentro del directorio buscado para que lo considere como un paquete a importar.
import sys
sys.path.append('../Estadistica Computacional con Python/Formulas Estadisticas/')

from math import ceil, floor
import unittest

def ceiling_to_a_number(numero, multiplo):
    '''
    Regresa el siguiente multiplo determinado del numero dado
    '''
    ceiling_number = ceil(numero / multiplo) * multiplo
    
    return ceiling_number

def floor_to_a_number(numero, multiplo):
    '''
    Regresa el anterior multiplo determinado del numero dado
    '''
    floor_number = floor(numero / multiplo) * multiplo

    return floor_number


def remover_duplicados(datos):
    '''
    Remueve valores duplicados de una lista o de un diccionario de datos
    '''
    if type(datos) == dict:
        temp_datos = {val: key for key, val in datos.items()}
        datos_numeros_unicos = {val: key for key, val in temp_datos.items()}

    else:
        temp_datos = {val:key for key, val in enumerate(datos)}
        datos_numeros_unicos = [key for key in temp_datos.keys()]

    return datos_numeros_unicos




class Pruebas_caja_cristal(unittest.TestCase):

    def test_ceiling_to_a_number(self):
        formula_ceiling_to_a_number = ceiling_to_a_number(6, 10)

        self.assertEqual(formula_ceiling_to_a_number, 10)

    def test_floor_to_a_number(self):
        formula_floor_to_a_number = floor_to_a_number(6, 10)

        self.assertEqual(formula_floor_to_a_number, 0)

    def test_remover_duplicados_dict(self):
        formula_remover_duplicados_dict = remover_duplicados(dict([(1,2), (2,2), (3,1)]))

        self.assertEqual(formula_remover_duplicados_dict, {2: 2, 3: 1})

    def test_remover_duplicados_list(self):
        formula_remover_duplicados_list = remover_duplicados([1, 2, 3, 3, 4, 5])

        self.assertEqual(formula_remover_duplicados_list, [1, 2, 3, 4, 5])



if '__main__' == __name__:

    unittest.main()
