#!/usr/bin/python
# -*- coding: utf-8 -*
#Écrire une fonction cibleAtteinte qui prend pour paramètre l’exposant et le cœfficient de la cible et un hash sur 256 bits et qui retourne vrai si ce hash est inférieur à la cible.
#cibleAtteinte(cœfficient, exposant, hash) -> true

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
    hash_object = hashlib.sha256(data)  #on hashe le tout
    HashmotHexa = hash_object.hexdigest() 
    print ("Valeur du hash aléatoire :  " ,  HashmotHexa)    
    scale = 16 ## hexadecimal
    num_of_bits = 256
    MotBin = bin(int(HashmotHexa, scale))[2:].zfill(num_of_bits)
    print ("chaine en binaire équivalente à ce hash dans laquelle on recherche :  " ,  MotBin)
    MotDecimalFromBin = int(MotBin, 2)  # Conversion en decimal à partir du bin 
    print ("chaine en decimal équivalente à ce hash dans laquelle on recherche  :  " ,  MotDecimalFromBin)
    return MotBin

def cibleAtteinte(coefficient, exposant, hash):
    #calcul de l'exposant hexa to Dec
    exposantdecimal = int(exposant, 16)
    chaineremplissage = '0' *  ((exposantdecimal * 2) - len(coefficient)) #6 est la longueur du coefficient
    chainecoefexposant =   coefficient + chaineremplissage #construction de la chaine coefficient exposant
    coefficientdecimal = int(coefficient, 16) 
    coefexposant = coefficientdecimal * pow(2,  8 * (exposantdecimal -3)) 
    Hashint = int(hash,  16)
    print ("comparons en appliquant la formule  hash < cœfficient * 2^(8*(exposant-3)) " )
    print (Hashint)
    print (coefexposant)
    print ("ou encore simplement en convertissant en int la chaine dé-condensée [nonce]: " ,  chainecoefexposant  )
    print (int(hash,  16))
    print(int(chainecoefexposant,  16))
    Test = int(hash,  16) < int(chainecoefexposant,  16) #On fait le test en int
    return Test    

if __name__ == "__main__":
    print ("Le programme vérifie la validité d'une preuve de travail")
    coefficient = str(input("Entrez un coefficient en Hexa dont le  swap endianess a déjà été réalisé [ex: a51832] : ")) 
    exposant = str(input("Entrez un exposant en Hexa [ex: 17] : ")) 
    hash = str(input("Entrez un hash en Hexa : 00000000000000000019b2634066a100e56ed58a0ae40ca5a4e2d1dba6a4be22] : ")) 
    print ("coefficient : ",  coefficient)
    print ("exposant : ",  exposant)
    print("il s'agit de trouver de vérifier que hash < nonce ")
    print("--------------")
    print(cibleAtteinte(coefficient, exposant, hash))
    

