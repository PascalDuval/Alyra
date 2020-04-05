#!/usr/bin/python
# -*- coding: utf-8 -*
#Écrire le même programme en utilisant une fonction de hachage connue (comme SHA-256 par exemple)
#Mesurer les performances en fonction de la fonction de hachage utilisée et de la longueur de la chaîne recherchée.

import random
import hashlib


def chaineAlea(longueur):
    caracteres = "AZERTYYUIOPQSDFGHJKLMWXCVBN" #dans l'ordre du clavier
    mot = "" #Variable mot 
    compteur = 0 #Compteur de lettres
    while compteur < longueur:
        lettre = caracteres[random.randint(0, len(caracteres)-1)] #On tire au hasard une lettre
        mot += lettre #On  ajoute la lettre au mot 
        compteur += 1 #On incrémente le compteur de lettres
    data = ""
    data = mot.encode()
    hash_object = hashlib.sha256(data)
    HashmotHexa = hash_object.hexdigest() 
#    print ("HashmotHexa : ",  HashmotHexa)
    return HashmotHexa


def rechercheDebut(Debut, longueur) :
    chaine = chaineAlea(longueur)
    print("chaine : ",  chaine)
    if chaine.find(Debut) ==-1: #tant que le Debut n'est pas dans la chaine 
        print("pas de présence de Debut dans la chaine ",  chaine)
        rechercheDebut(Debut, longueur)  
    else :
            if chaine.find(Debut) !=0 : #si le Debut n'est pas au début de la chaine
                print("Debut est dans la chaine mais pas au début .. ",  chaine)
                rechercheDebut(Debut, longueur)
            else :
                print("La chaîne trouvée est : ",  chaine )


    

if __name__ == "__main__":
    print ("modèle de pow naîve : longueur du mot <= 8 - Debut de l'hexa : [nx ex: 7f - 00 - 2b] ")
    longueur = int(input('Entrez une longueur [8 maxi] : '))
    Debut = str(input("Entrez un début de chaîne Hexa [2 caractères maxi] : ")) 
    Debut = Debut.lower()
    rechercheDebut( Debut, longueur )
    
#python -m cProfile fact.py en ligne de commande
#Le rapport fournit présente plusieurs champs intéressants :
#ncalls : le nombre d’appels de la fonction
#tottime : founit le temps total en secondes passé dans la fonction en excluant les sous-fonctions
#percall : est égal à tottime/ncalls
#cumtime : est le temps passé dans la fonction et les sous-fonctions1
#filename :lineno(function) : donne l’information sur la fonction testée ainsi que sa position (fichier + numéro de ligne)


#Je n'ai pas d'outil pour mesurer les performances en fonction de la fonction de hachage utilisée et de la longueur de la chaîne recherchée à part python -m cProfile programme.py en ligne de commande .. mais j'avoue ne pas trop savoir interpréter les résultats.
#Suis preneur de la solution de cet exercice optionnel, y compris de la petite fonction de comparaison qui prend en entrée une fonction de hashage (md5, sha256, etc..)  :-)
