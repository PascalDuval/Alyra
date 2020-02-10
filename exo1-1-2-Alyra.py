#!/usr/bin/python
# -*- coding: utf-8 -*-

#fonction factorielle

import math

def fact (n):
    if n<2:
        return 1
    else:
        return n*fact(n-1)

def factalter(n):
    x=1
    for i in range(2,n+1):
        x= x*i
    return x


while True:
    nombre = int(input("Tapez un nombre entier (méthode récursive puis methode range puis math.factorial ) : "))
    print (fact(nombre))
    print (factalter(nombre))
    print (math.factorial(nombre))
    break

#lancer python -m cProfile -s cumtime exo1-1-2.py en ligne de commande
#Le rapport fournit présente plusieurs champs intéressants :
#ncalls : le nombre d’appels de la fonction
#tottime : founit le temps total en secondes passé dans la fonction en excluant les sous-fonctions
#percall : est égal à tottime/ncalls
#cumtime : est le temps passé dans la fonction et les sous-fonctions
#filename :lineno(function) : donne l’information sur la fonction testée ainsi que sa position (fichier + numéro de ligne)
#ex : 950!
#957 function calls (8 primitive calls) in 2.370 seconds
#Ordered by: cumulative time
#   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#        1    0.000    0.000    2.370    2.370 exo1-1-2-Alyra.py:6(<module>)
#        1    2.369    2.369    2.369    2.369 {input}
#    950/1 0.001    0.000    0.001    0.001 exo1-1-2-Alyra.py:8(fact)
#        1    0.000    0.000    0.000    0.000 exo1-1-2-Alyra.py:14(factalter)
#        1    0.000    0.000    0.000    0.000 {math.factorial}
#        1    0.000    0.000    0.000    0.000 {range}
#        1    0.000    0.000    0.000    0.000 <string>:1(<module>)
#        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

# la méthode range est plus rapide que la fonction récursive, aussi rapide que la méthode native et surtout elle n'est pas limité en mémoire 
# fact(n) plante au bout de 1000 appels successifs
