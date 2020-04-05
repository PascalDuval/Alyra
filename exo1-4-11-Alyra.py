#!/usr/bin/python
# -*- coding: utf-8 -*

#Écrire une fonction qui tire aléatoirement une chaîne de n caractères (choisis parmi A…Z).

#chaineAlea(8) -> “AKEKUIOP”

#Écrire une fonction qui prend en paramètres une chaîne et lance la chaineAlea() jusqu’à ce que le début du résultat corresponde à cette chaîne.

#rechercheDebut(“AA”, 8) - >
#UEKOIPEO
#KEELJENE
#….
#AAKJEOFE
#Mesurer la durée de chaque recherche de solution en fonction de la longueur de la chaîne et de n

import random

def chaineAlea(longueur):
    caracteres = "AZERTYYUIOPQSDFGHJKLMWXCVBN" #dans l'ordre du clavier
    mot = "" #Variable mot 
    compteur = 0 #Compteur de lettres
    while compteur < longueur:
        lettre = caracteres[random.randint(0, len(caracteres)-1)] #On tire au hasard une lettre
        mot += lettre #On  ajoute la lettre au mot 
        compteur += 1 #On incrémente le compteur de lettres
    return mot


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
    print ("modèle de pow naîve : longueur du mot <= 8 - Debut du mot : [XY] ")
    longueur = int(input('Entrez une longueur [8 maxi] : '))
    Debut = str(input("Entrez un début de chaîne en majuscule [2 lettres maxi] : ")) 
    Debut = Debut.upper()
    rechercheDebut( Debut, longueur )
    
