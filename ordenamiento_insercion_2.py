import random
import unittest
from ubicacion_binaria import ubicacion_binaria


def ordenamiento_insercion(lista):
    inicio_acote_ordenado = 0
    final_acote_ordenado = 0
    inicio_acote_desordenado = 1
    final_lista = len(lista)-1

    # Por cada ubicacion de la lista desordenada
    for ubicacion_en_lista_desordenada in range(inicio_acote_desordenado, len(lista)):
        # Encuentra la ubicacion en la lista ordenada

        ubicacion = ubicacion_binaria(
            lista, inicio_acote_ordenado, final_acote_ordenado, lista[inicio_acote_desordenado])

        # Si el numero desordenado es mayor que el de la ubicacion encontrada
        if lista[inicio_acote_desordenado] > lista[ubicacion]:

            lista.insert(ubicacion + 1, lista[ubicacion_en_lista_desordenada])
            lista.pop(ubicacion_en_lista_desordenada+1)

        # Si el numero desordenado es menor o igual que el de la ubicacion encontrada
        else:
            lista.insert(
                ubicacion, lista[ubicacion_en_lista_desordenada]
            )
            lista.pop(ubicacion_en_lista_desordenada+1)
        final_acote_ordenado += 1
        inicio_acote_desordenado += 1

    return lista


class prueba_caja_cristal(unittest.TestCase):
    def test_ordenamiento_lista(self):
        TAMANO_DE_LISTA = 10000
        lista = [
            random.randint(0, TAMANO_DE_LISTA)
            for i in range(TAMANO_DE_LISTA)
        ]

        resultado = ordenamiento_insercion(lista)

        self.assertEqual(resultado, sorted(lista))


if __name__ == '__main__':
    unittest.main()
    '''TAMANO_DE_LISTA = 10
    lista = [
        random.randint(0, TAMANO_DE_LISTA)
        for i in range(TAMANO_DE_LISTA)
    ]
    print(lista)
    resultado = ordenamiento_insercion(lista)
    print(resultado)'''
