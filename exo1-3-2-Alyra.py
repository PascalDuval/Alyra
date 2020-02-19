#!/usr/bin/python
# -*- coding: utf-8 -*

# Ecrire une fonction qui prend en entrée un texte et retourne le nombre d'occurrences de chaque caractère dans le texte

# POUR Chaque Lettre dans une liste donnée de caractères alphabétiques
#   SI son nombre d'occurences est > 0 
#       La mettre dans un dico (tableau d'association lettre : frequence)
#   FSI
# FIN POUR
# Retourner le dico au format string

#Les codes 65 à 90 représentent les majuscules
#Les codes 97 à 122 représentent les minuscules
#Les codes 192 à 255 représentent les caractères accentués

# Il vaudrait mieux faire des extend successifs ... 

def Frequence(chaine):
    listeLettre = map(chr, range(65,255)) #lettre dont la valeur ascii va de  65 à 255
# listeLettre = map(chr, range(65,90)) + map(chr, range(97,122)) + map(chr, range(192,255)) #lettre dont la valeur ascii va de  65 à 255
# non exhaustif : listeLettre = ("a","à","â","b","c","d","e","é", "è", "ê","ë","f","g","h","i","ï","j","k","l","m","n","o","p","q","r","s","t","u","ù","ü","v","w","x","y","z", "A","B","C","D","E","Ê","F","G","H","I","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z") 
    dicoNbrLettre = {} 
    for lettre in listeLettre:
            if chaine.count(lettre) != 0:
                dicoNbrLettre[lettre] = chaine.count(lettre)
    return(str(dicoNbrLettre))
 
phrase = input("Votre message : ")
chaine = phrase

print("Fréquence : " + Frequence(chaine))

