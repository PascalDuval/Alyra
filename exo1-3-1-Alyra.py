#!/usr/bin/python
# -*- coding: utf-8 -*

# Cette nouvelle version du code de Cesar consiste à aller chercher pur chaque caractère x dans la table ascii le caractère ayant la valeur x + n
# TANT QUE on n'a pas atteint la fin de la chaine à crypter
# On prend la valeur ASCII de chaque lettre
# On concatène à la chaîne cryptée le caractère correspondant à cette valeur auquel on ajoute le décalage souhaité
# On append un tableau de chaque morceau ainsi crypté
#   SI on est arrivé à la fin de la châine à crypter
#   On retourne dernier élement du tableau
#   FSI
#FIN TANT QUE

def Cesar(chaine,  number):
    longueur=len(chaine)
    N= number # peut être négatif ou positif     
    Tab=[]
    k=""  #groupe de lettres concaténées
    i=0
    while i <longueur:
        a=ord(chaine[i]) #ord(c) renvoie le nombre entier représentant le code  du caractère représenté par la chaîne donnée. Par exemple, ord('a') renvoie le nombre entier 97 et ord('€') (symbole Euro) renvoie 8364. Il s'agit de l'inverse de chr()
        k = k+chr((a) + N) #char est l'inverse de ord  - on concatène
        Tab.append(k)  #on append un tableau 
        i =i+1 
        if i == longueur:
           return(Tab[i-1])

phrase = input("Votre phrase : ")
decalage = int(input("Votre décalage : "))
chaine = phrase
number = decalage

print("Le message codé est : " + Cesar (chaine,  number))

print("-----------------")

print("Le message décodé est : " + Cesar(Cesar (chaine,  number), number * -1))

