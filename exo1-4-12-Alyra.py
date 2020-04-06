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

def rechercheDebut(Debut, longueur,  Essai) :
    chaine = chaineAlea(longueur)
    if chaine.find(Debut) ==-1: #tant que le nonce n'est pas dans la chaine 
        Essai +=1
        print("pas de présence du nonce dans la chaine ")
        print("--------------")
        rechercheDebut(Debut, longueur,  Essai)         
    else :
            if chaine.find(Debut) !=0 : #si le Debut n'est pas au début de la chaine
                Essai +=1
                Test = int(chaine, 2) <= chaineDecimale
                print("Le nonce est-il trouvé au début ? : ",  Test )
                print("--------------")
                rechercheDebut(Debut, longueur,  Essai)
            else :
                Test = int(chaine, 2) <= chaineDecimale
                print("Le nonce est-il trouvé au début ? : ",  Test )
                print("Cette dernière chaîne obtenue termine notre preuve de travail ; elle est bien inférieure à la valeur fixée au départ par notre nonce : ",  chaineDecimale )
                print("--------------")
                print("Nombre d'essais effectifs pour résoudre ce problème  : ",  Essai )
    

if __name__ == "__main__":
    print ("Le programme effectue une preuve de travail à partir de la recherche d'un certain début de chaine en binaire ne comprenant que des 0 dans une chaine aléatoire en binaire")
    Nonce = str(input("Entrez un début de chaîne binaire de longueur variable [nx ex: 0 - 00 - 000 - 00000000] : ")) 
    #ici on pourrait faire les vérifications d'usage
    Essai =1
    exposant = len(Nonce)
    print ("exposant : ",  exposant)
    chaineremplissage = '1' *  (256 - exposant)
    chaineborne = Nonce + chaineremplissage
    chaineDecimale = int(chaineborne, 2)
    print("il s'agit de trouver en fait la première chaîne aléatoire inférieure en décimal à : ",  chaineDecimale)

    Noncemaximal = '0' * 32
    chaineremplissagemax = '1' *  (256 - 32)
    chaineimaginaire = Noncemaximal  + chaineremplissagemax
    print("Notabene 1 : si le nonce était utilisé entièrement sur 4 octets, la pow consisterait à  trouver la première chaine aléatoire inférieure en décimal à ",   int(chaineimaginaire, 2))    
    print("Notabene 2 : La complexité étant exponentielle, il faudrait beaucoup plus d'essais, soit : ",   pow(2, 32))    

    print("--------------")
    print("Nombre d'essais en moyenne pour résoudre ce problème avec le nonce choisi : ",  pow(2, exposant) )
    rechercheDebut(Nonce, 8,  Essai)
    

