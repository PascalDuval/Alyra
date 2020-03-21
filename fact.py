#!/usr/bin/python
# -*- coding: utf-8 -*-
#fonction factorielle

def fact (n):
    if n<2:
        return 1
    else:
        return n*fact(n-1)

while True:
    nombre = int(input("Tapez un nombre entier (méthode récursive) : "))
    print  (fact(nombre))
    break

    
#python -m cProfile fact.py en ligne de commande
#Le rapport fournit présente plusieurs champs intéressants :
#ncalls : le nombre d’appels de la fonction
#tottime : founit le temps total en secondes passé dans la fonction en excluant les sous-fonctions
#percall : est égal à tottime/ncalls
#cumtime : est le temps passé dans la fonction et les sous-fonctions1
#filename :lineno(function) : donne l’information sur la fonction testée ainsi que sa position (fichier + numéro de ligne)
