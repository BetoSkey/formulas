import unittest
import random


def ubicacion_binaria(lista, comienzo, final, objetivo, ubicacion_meta=0):

    if final-comienzo == 1:  # Si la lista se acoto a dos ubicaciones
        if objetivo > lista[final]:

            if final + 1 > len(lista)-1:
                ubicacion_meta = len(lista)-1
            else:
                ubicacion_meta = final

            return ubicacion_meta
        elif objetivo < lista[comienzo]:
            ubicacion_meta = comienzo

            return ubicacion_meta

    if comienzo == final:  # Si la lista llego al final de su acote y solo nos indica una ubicacion

        # Si el objetivo no se encontro y es mayor que el acotamiento final
        if objetivo > lista[final]:
            # Si la ubicacion meta es mas grande que la lista completa
            if final + 1 > len(lista)-1:
                ubicacion_meta = len(lista)-1

            else:
                ubicacion_meta = final + 1

        # Si estamos al principio de la lista o el objetivo es igual que el acotamiento final
        elif comienzo == 0 or objetivo == lista[final]:
            pass

        else:
            ubicacion_meta += 1

        return ubicacion_meta

    # Aqui empieza a acotar la busqueda
    medio = (comienzo + final) // 2  # Se acota la lista a la mitad

    if objetivo == lista[medio]:  # Si el objetivo se encontro en la mitad
        return medio

    elif objetivo > lista[medio]:  # Si el objetivo es mayor que la mitad
        ubicacion_meta = medio
        return ubicacion_binaria(lista, medio + 1, final, objetivo, ubicacion_meta)

    else:  # Si el objetivo es menor que la mitad
        return ubicacion_binaria(lista, comienzo, medio - 1, objetivo, ubicacion_meta)


def ordenamiento_insercion(lista):
    lista_ordenada = [lista[0]]
    lista_desordenada = lista[1:]
    n_lista_ordenada = len(lista_ordenada)-1
    n_lista_desordenada = len(lista_desordenada)-1

    # Por cada ubicacion de la lista desordenada
    for ubicacion_en_lista_desordenada in range(n_lista_desordenada+1):

        # Encuentra la ubicacion en la lista ordenada
        ubicacion = ubicacion_binaria(
            lista_ordenada, 0, n_lista_ordenada, lista_desordenada[ubicacion_en_lista_desordenada])

        # Si el numero desordenado es mayor que el de la ubicacion encontrada
        if lista_desordenada[ubicacion_en_lista_desordenada] > lista_ordenada[ubicacion]:

            # Si la ubicacion encontrada es igual que el final de la lista, se agrega al final
            if ubicacion == n_lista_ordenada:
                lista_ordenada.append(
                    lista_desordenada[ubicacion_en_lista_desordenada])

            # Si el numero no esta al final de la lista, se inserta en la siguiente ubicacion encontrada
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


def busqueda_binaria(lista, comienzo, final, objetivo, ordenar=True):
    lista_ordenada = []
    if ordenar == True:
        lista_ordenada = ordenamiento_insercion(lista)

    if comienzo > final:
        return False
    medio = (comienzo + final) // 2
    if lista_ordenada[medio] == objetivo:
        return True
    elif lista_ordenada[medio] < objetivo:
        return busqueda_binaria(lista_ordenada, medio + 1, final, objetivo)
    else:
        return busqueda_binaria(lista_ordenada, comienzo, medio - 1, objetivo)


class prueba_caja_cristal(unittest.TestCase):

    # Test Ubicacion binaria
    def test_encontrar_ubicacion_intermedia(self):
        lista = [1, 2, 3, 5, 5, 5, 5, 8, 9, 10]
        objetivo = 4

        resultado = ubicacion_binaria(lista, 0, 9, objetivo)

        self.assertEqual(resultado, 3)

    def test_encontrar_ubicacion_al_final(self):
        lista = [1, 3, 4]
        objetivo = 8

        resultado = ubicacion_binaria(lista, 0, 2, objetivo)

        self.assertEqual(resultado, 2)

    def test_encontrar_ubicacion_al_principio(self):
        lista = [1, 2, 3, 5, 5, 5, 5, 8, 9, 10]
        objetivo = 0

        resultado = ubicacion_binaria(lista, 0, 9, objetivo)

        self.assertEqual(resultado, 0)

    def test_prueba_manual(self):
        lista = [1,	3,	5,	5,	6,	7,	8,	10]
        objetivo = 1

        resultado = ubicacion_binaria(lista, 0, 7, objetivo)

        self.assertEqual(resultado, 0)

    def test_prueba_manual2(self):
        lista = [1, 7, 9]
        objetivo = 6

        resultado = ubicacion_binaria(lista, 0, 2, objetivo)

        self.assertEqual(resultado, 1)

    def test_encontrar_ubicacion_intermedia_numeros_repetidos(self):
        lista = [1, 2, 3, 5, 5, 5, 5, 8, 9, 10]
        objetivo = 5

        resultado = ubicacion_binaria(lista, 0, 9, objetivo)

        self.assertEqual(resultado, 4)

    def test_encontrar_ubicacion_lista_de_un_elemento(self):
        lista = [1]
        objetivo = 0

        resultado = ubicacion_binaria(lista, 0, 0, objetivo)

        self.assertEqual(resultado, 0)

    def test_encontrar_ubicacion_lista_dos_elementos(self):
        lista = [1, 3]
        objetivo = 2

        resultado = ubicacion_binaria(lista, 0, 1, objetivo)

        self.assertEqual(resultado, 1)

    def test_encontrar_ubicacion_lista_mil_elementos(self):
        lista = [
            0, 1, 3, 4, 5, 5, 5, 5, 5, 5, 7, 8, 9, 9, 10, 11, 11, 11, 14, 14, 16, 16, 16, 16, 17, 18, 18, 23, 24, 25,
            25, 27, 28, 28, 28, 31, 32, 34, 34, 35, 36, 36, 36, 37, 39, 39, 40, 40, 41, 41, 42, 42, 42, 43, 44, 45, 47,
            48, 48, 50, 50, 51, 51, 53, 53, 53, 53, 55, 56, 56, 56, 58, 59, 59, 60, 64, 64, 65, 65, 68, 68, 69, 69, 70,
            71, 71, 72, 75, 77, 78, 80, 81, 81, 83, 84, 86, 86, 87, 88, 88, 89, 89, 90, 91, 92, 92, 92, 95, 96, 96, 96,
            96, 97, 97, 98, 99, 101, 101, 102, 102, 106, 108, 109, 109, 110, 111, 113, 115, 117, 117, 117, 120, 121, 122,
            122, 124, 124, 124, 125, 126, 128, 128, 132, 132, 132, 132, 133, 133, 134, 137, 138, 138, 138, 139, 142, 143,
            144, 144, 147, 147, 150, 151, 151, 153, 154, 154, 154, 155, 156, 156, 159, 159, 160, 161, 163, 164, 164, 165,
            166, 167, 167, 168, 169, 169, 170, 172, 172, 173, 176, 177, 178, 178, 179, 179, 179, 180, 180, 181, 182, 183,
            184, 184, 185, 188, 190, 192, 194, 194, 198, 199, 200, 201, 202, 202, 202, 203, 205, 206, 209, 210, 211, 211,
            212, 212, 212, 212, 213, 213, 215, 216, 217, 217, 223, 224, 225, 225, 227, 227, 228, 231, 233, 234, 235, 236,
            236, 237, 239, 240, 241, 242, 243, 243, 243, 244, 244, 246, 247, 247, 248, 250, 250, 250, 255, 255, 256, 256,
            256, 257, 259, 260, 261, 262, 262, 263, 264, 264, 265, 265, 266, 266, 269, 271, 271, 272, 273, 274, 276, 276,
            277, 280, 280, 280, 282, 283, 285, 285, 285, 286, 287, 287, 288, 288, 288, 289, 289, 290, 293, 293, 294, 296,
            297, 297, 297, 297, 299, 301, 302, 304, 304, 304, 308, 309, 309, 309, 310, 312, 312, 313, 315, 316, 318, 320,
            320, 323, 324, 324, 325, 325, 325, 327, 328, 328, 328, 329, 329, 330, 331, 331, 332, 334, 335, 335, 336, 337,
            338, 340, 340, 342, 345, 346, 347, 348, 349, 351, 352, 352, 353, 356, 357, 357, 358, 360, 360, 360, 361, 363,
            363, 365, 368, 371, 373, 373, 374, 374, 375, 375, 376, 377, 379, 380, 381, 381, 382, 383, 383, 383, 384, 384,
            384, 387, 388, 389, 389, 391, 392, 393, 395, 396, 398, 398, 398, 403, 404, 404, 407, 407, 407, 408, 408, 409,
            409, 410, 410, 411, 413, 413, 414, 414, 416, 419, 421, 421, 422, 425, 426, 427, 427, 428, 429, 430, 430, 431,
            431, 432, 433, 434, 435, 436, 437, 437, 438, 438, 438, 439, 442, 443, 443, 447, 447, 448, 451, 452, 452, 453,
            453, 454, 454, 455, 455, 456, 457, 458, 459, 460, 462, 463, 464, 464, 465, 466, 467, 467, 468, 468, 469, 471,
            472, 474, 474, 477, 477, 477, 478, 478, 479, 481, 482, 483, 484, 486, 487, 487, 488, 488, 489, 489, 489, 490,
            490, 490, 491, 492, 492, 493, 494, 496, 501, 501, 503, 503, 504, 504, 505, 506, 506, 506, 507, 512, 513, 514,
            514, 514, 516, 517, 518, 518, 519, 521, 522, 522, 523, 523, 526, 526, 526, 527, 527, 528, 528, 528, 529, 531,
            536, 536, 538, 538, 539, 539, 540, 540, 542, 542, 543, 543, 546, 547, 547, 549, 551, 551, 551, 551, 552, 553,
            555, 556, 556, 556, 559, 559, 560, 561, 562, 562, 563, 566, 566, 567, 572, 574, 578, 578, 580, 581, 583, 584,
            585, 586, 587, 588, 589, 589, 590, 592, 593, 595, 596, 597, 597, 599, 600, 601, 601, 603, 603, 603, 604, 604,
            605, 608, 609, 612, 612, 612, 612, 613, 613, 613, 614, 616, 617, 618, 620, 621, 621, 622, 622, 623, 625, 629,
            629, 629, 629, 632, 632, 633, 634, 634, 634, 635, 636, 637, 637, 640, 641, 641, 641, 642, 642, 642, 642, 642,
            643, 644, 645, 651, 652, 653, 653, 653, 654, 655, 658, 658, 658, 659, 659, 662, 664, 665, 665, 666, 667, 670,
            673, 674, 674, 676, 676, 677, 678, 679, 680, 682, 683, 684, 685, 686, 687, 688, 688, 688, 689, 690, 690, 694,
            694, 696, 697, 701, 701, 702, 703, 703, 704, 705, 706, 707, 708, 709, 709, 713, 714, 715, 716, 716, 717, 720,
            721, 721, 722, 723, 723, 724, 724, 728, 728, 732, 734, 734, 735, 736, 736, 737, 738, 738, 739, 739, 740, 740,
            743, 744, 745, 746, 751, 752, 754, 754, 756, 756, 760, 761, 762, 763, 767, 767, 767, 769, 769, 771, 771, 772,
            775, 776, 779, 780, 780, 780, 781, 782, 783, 783, 784, 785, 785, 787, 787, 788, 789, 790, 790, 790, 791, 792,
            793, 793, 793, 795, 797, 799, 800, 800, 800, 802, 802, 803, 803, 804, 804, 804, 805, 806, 810, 814, 814, 815,
            817, 817, 817, 819, 821, 824, 827, 828, 829, 830, 831, 831, 832, 832, 834, 834, 836, 836, 838, 838, 840, 840,
            840, 842, 842, 844, 844, 844, 845, 850, 850, 853, 853, 853, 854, 854, 855, 855, 857, 858, 858, 859, 860, 867,
            868, 871, 873, 873, 873, 874, 875, 876, 877, 877, 878, 880, 880, 882, 883, 884, 884, 885, 887, 888, 888, 888,
            888, 889, 891, 892, 893, 893, 894, 897, 898, 899, 899, 900, 901, 902, 904, 904, 905, 906, 909, 909, 911, 915,
            917, 918, 919, 923, 923, 923, 923, 924, 924, 925, 927, 928, 929, 929, 930, 931, 934, 934, 934, 935, 936, 936,
            936, 937, 939, 939, 940, 940, 940, 942, 945, 946, 947, 948, 951, 952, 953, 954, 955, 955, 955, 956, 956, 956,
            957, 959, 960, 961, 962, 962, 962, 962, 963, 965, 966, 966, 966, 967, 967, 968, 970, 971, 972, 973, 973, 974,
            975, 976, 976, 977, 977, 977, 979, 979, 979, 980, 980, 984, 984, 985, 985, 986, 987, 987, 988, 989, 990, 991,
            991, 992, 992, 994, 995, 995, 996, 1000
        ]
        objetivo = 700

        resultado = ubicacion_binaria(lista, 0, 999, objetivo)

        self.assertEqual(resultado, 709)

    # Test Ordenamiento de insercion
    def test_ordenamiento_lista(self):
        TAMANO_DE_LISTA = 10000
        lista = [
            random.randint(0, TAMANO_DE_LISTA)
            for i in range(TAMANO_DE_LISTA)
        ]

        resultado = ordenamiento_insercion(lista)

        self.assertEqual(resultado, sorted(lista))

    # Test Busqueda binaria
    def test_lista_pequeña_encontrado(self):
        lista = [0, 5, 1]
        objetivo = 1

        resultado = busqueda_binaria(lista, 0, len(lista)-1, objetivo)

        self.assertEqual(resultado, True)

    def test_lista_pequeña_no_encontrado(self):
        lista = [2, 9, 4]
        objetivo = 7

        resultado = busqueda_binaria(lista, 0, len(lista)-1, objetivo)

        self.assertEqual(resultado, False)

    def test_lista_mil_elementos_encontrado(self):
        lista = lista = [
            774, 962, 329, 223, 30, 55, 584, 888, 924, 854, 799, 591, 723, 581, 660, 502, 53, 808, 951, 432,
            705, 659, 872, 7, 304, 390, 960, 100, 596, 363, 590, 918, 861, 100, 567, 48, 365, 818, 44, 988,
            287, 953, 604, 262, 411, 921, 91, 925, 266, 675, 287, 528, 296, 666, 300, 333, 498, 905, 990, 316,
            582, 992, 473, 515, 294, 176, 779, 759, 365, 97, 423, 594, 801, 128, 265, 594, 306, 125, 936, 374,
            214, 676, 743, 941, 731, 363, 780, 795, 873, 254, 655, 712, 7, 910, 769, 209, 264, 557, 791, 512,
            275, 124, 849, 576, 816, 858, 366, 816, 336, 916, 843, 365, 651, 114, 237, 686, 585, 92, 660, 619,
            645, 501, 138, 365, 223, 344, 475, 908, 596, 494, 23, 972, 576, 377, 639, 490, 199, 24, 996, 131,
            999, 993, 390, 27, 669, 969, 862, 757, 966, 460, 449, 215, 786, 413, 77, 644, 811, 245, 292, 451,
            163, 869, 565, 335, 926, 281, 269, 95, 69, 75, 612, 416, 59, 198, 393, 626, 481, 655, 774, 152, 432,
            302, 260, 100, 959, 320, 299, 82, 888, 794, 415, 411, 805, 639, 605, 226, 856, 796, 823, 398, 361, 215,
            801, 619, 698, 807, 24, 639, 407, 837, 897, 885, 243, 938, 852, 33, 784, 903, 409, 132, 992, 945, 772,
            779, 645, 279, 739, 604, 441, 448, 823, 857, 219, 884, 676, 918, 748, 484, 779, 45, 257, 487, 424, 598,
            539, 906, 626, 489, 1000, 356, 683, 85, 105, 539, 331, 922, 979, 591, 161, 802, 731, 135, 394, 890, 441,
            273, 410, 66, 787, 607, 223, 154, 386, 495, 761, 869, 154, 853, 708, 744, 376, 803, 694, 352, 306, 854,
            445, 361, 873, 191, 810, 427, 51, 530, 438, 624, 501, 916, 758, 84, 903, 770, 940, 397, 174, 164, 384,
            609, 931, 671, 420, 905, 786, 439, 794, 965, 669, 505, 107, 599, 230, 128, 417, 415, 12, 744, 732, 823,
            671, 341, 393, 716, 749, 100, 960, 140, 123, 849, 425, 855, 132, 590, 679, 728, 776, 650, 610, 867, 676,
            9, 547, 717, 861, 927, 308, 26, 159, 118, 411, 89, 363, 527, 544, 253, 147, 862, 658, 10, 741, 51, 121,
            383, 74, 154, 44, 848, 221, 137, 347, 457, 532, 538, 876, 265, 581, 782, 845, 568, 911, 537, 218, 440, 88,
            380, 269, 134, 667, 470, 53, 933, 329, 576, 622, 377, 586, 295, 289, 77, 981, 833, 374, 812, 791, 510, 267,
            545, 595, 426, 528, 34, 669, 63, 849, 76, 476, 596, 305, 706, 61, 304, 579, 860, 157, 201, 708, 908, 934,
            702, 936, 853, 672, 662, 282, 904, 89, 943, 814, 671, 167, 88, 438, 514, 681, 657, 327, 725, 648, 679, 51,
            14, 579, 241, 496, 9, 281, 987, 475, 796, 491, 138, 941, 850, 302, 621, 692, 108, 758, 269, 903, 64, 426,
            206, 423, 523, 538, 986, 494, 53, 901, 758, 214, 841, 588, 246, 765, 982, 266, 206, 907, 350, 276, 317, 155,
            554, 980, 295, 251, 264, 724, 837, 693, 529, 184, 708, 1, 44, 409, 37, 535, 871, 746, 657, 885, 252, 249, 311,
            983, 929, 815, 940, 47, 723, 968, 872, 429, 546, 86, 625, 194, 133, 344, 938, 605, 810, 451, 236, 162, 789,
            598, 368, 984, 612, 949, 63, 30, 191, 997, 943, 882, 240, 659, 572, 644, 954, 685, 682, 896, 694, 32, 267,
            341, 273, 557, 292, 180, 968, 740, 281, 174, 75, 640, 525, 629, 806, 580, 640, 596, 632, 643, 192, 694, 547,
            73, 529, 187, 618, 747, 311, 891, 901, 303, 492, 701, 885, 10, 745, 224, 52, 647, 454, 819, 3, 103, 447, 482,
            490, 271, 56, 159, 717, 968, 340, 266, 791, 335, 837, 25, 790, 677, 372, 91, 483, 435, 890, 951, 614, 645, 473,
            31, 625, 450, 786, 934, 952, 395, 256, 412, 543, 903, 932, 174, 314, 263, 20, 155, 655, 592, 629, 932, 770, 87,
            624, 589, 905, 778, 339, 366, 737, 134, 240, 511, 386, 884, 576, 446, 164, 116, 710, 958, 146, 600, 314, 692,
            685, 956, 256, 793, 455, 177, 70, 41, 859, 84, 750, 491, 509, 49, 829, 696, 531, 922, 798, 478, 544, 72, 811,
            422, 132, 0, 138, 831, 672, 337, 677, 223, 961, 557, 483, 565, 290, 321, 655, 560, 803, 582, 542, 599, 924,
            884, 278, 650, 4, 325, 155, 107, 802, 66, 732, 779, 275, 354, 616, 563, 869, 322, 700, 236, 632, 730, 302, 907,
            233, 713, 957, 737, 32, 285, 847, 322, 35, 487, 937, 979, 692, 531, 997, 442, 139, 938, 280, 688, 819, 564, 20,
            928, 129, 149, 619, 290, 303, 300, 578, 594, 595, 151, 876, 164, 64, 418, 743, 564, 414, 909, 866, 675, 386, 964,
            733, 741, 950, 962, 439, 228, 395, 87, 626, 912, 708, 293, 45, 900, 367, 736, 191, 146, 584, 61, 398, 358, 700,
            4, 24, 126, 658, 384, 131, 76, 737, 924, 653, 490, 169, 891, 587, 481, 474, 374, 821, 824, 40, 864, 615, 590,
            435, 10, 85, 695, 698, 738, 204, 811, 393, 236, 440, 98, 24, 444, 741, 274, 285, 529, 711, 860, 342, 8, 741,
            483, 955, 521, 557, 601, 165, 326, 270, 312, 959, 253, 205, 422, 145, 28, 590, 628, 272, 538, 901, 716, 451,
            658, 331, 532, 994, 554, 737, 936, 579, 68, 371, 790, 898, 727, 255, 524, 563, 26, 777, 368, 227, 293, 636,
            300, 742, 156, 404, 37, 547, 685, 358, 57, 801, 660, 656, 785, 9, 667, 478, 614, 629, 807, 915, 248, 778, 591,
            347, 819, 27, 640, 535, 82, 75, 863, 221, 527, 578, 301, 487, 117, 9, 602, 599, 280, 40, 160, 940, 938, 709,
            782, 812, 168, 415, 886, 242, 627, 399, 788, 282, 458, 615, 956, 402, 110, 306, 343, 345, 721, 10, 58, 3, 989,
            196, 558, 655, 993, 9, 512, 151, 577, 807, 539, 772, 443, 882, 138, 88, 537, 134, 571, 859, 257, 691
        ]
        objetivo = 415

        resultado = busqueda_binaria(lista, 0, len(lista)-1, objetivo)

        self.assertEqual(resultado, True)

    def test_lista_cien_elementos_no_encontrado(self):
        lista = [
            48, 64, 54, 74, 58, 75, 54, 9, 37, 86, 95, 84, 73, 12, 42, 45, 29, 21, 78, 85, 60, 60, 10, 95, 94,
            35, 53, 75, 87, 77, 38, 31, 82, 39, 42, 69, 77, 88, 37, 32, 48, 50, 0, 42, 20, 67, 39, 2, 45, 48,
            70, 9, 23, 29, 84, 60, 36, 33, 88, 19, 3, 12, 89, 17, 56, 65, 12, 37, 19, 19, 89, 11, 32, 56, 43,
            38, 66, 1, 100, 42, 23, 38, 86, 23, 43, 65, 46, 27, 77, 21, 100, 77, 39, 100, 51, 22, 7, 62, 82, 41
        ]
        objetivo = 101

        resultado = busqueda_binaria(lista, 0, len(lista)-1, objetivo)

        self.assertEqual(resultado, False)


if __name__ == '__main__':
    unittest.main()
