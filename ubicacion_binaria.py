import random
import unittest


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


class prueba_caja_de_cristal(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
