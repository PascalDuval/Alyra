#Construire un jeu qui pour tire aléatoirement un nombre entre 1 et 100 et demande à l'utilisateur de le deviner. 
#Pour chaque entrée de l'utilisateur le programme affiche si la bonne réponse est supérieure ou inférieure. 
#Il affiche aussi si la réponse est très proche (<=5), proche ( 6 à 10) ou supérieur.
#ex : Devinez un nombre entre 1 et 100
#> 50
#C'est beaucoup plus
#> 89
#C'est un tout petit peu moins
#> 86
#Exact !
#
#TIRAGE d'un Nombre'
#TANT_QUE l'utilisateur n'a pas saisi le bon Nombre
#proposer de saisir un nombre ou sortir
#SELON le nombre saisi  AFFICHER message
#FIN TANT_QUE


from random import *
alea = randrange(1, 100)
# print(alea) pour debug

MessageUnPeuPlus = "C'est un peu plus"
MessageUnPeuMoins = "C'est un peu moins"
MessageSup = "C'est supérieur"
MessageProcheSup = "C'est plus"
MessageProcheMoins = "C'est moins"
MessageInf = "C'est inférieur"

while 1: # 1 est toujours vrai -> boucle infinie
    nombre = float(input("Tapez un nombre entre 1 et 100 : "))
    if nombre == alea:
        print("Exact !")
        break
    elif (alea - nombre) <=  5 and (nombre < alea)  :
        print(MessageUnPeuPlus)
    elif (alea - nombre) >=  6 and (alea - nombre) <=  10 and nombre < alea:
         print(MessageProcheSup)
    elif (alea - nombre) >  10 and nombre < alea:
         print(MessageSup)
    elif (nombre - alea) <= 5 and nombre > alea:
         print(MessageUnPeuMoins)
    elif (nombre - alea) >= 6 and (nombre - alea) <= 10 and nombre > alea :
         print(MessageProcheMoins)
    elif (nombre - alea) > 10 and nombre > alea :
         print(MessageInf)
    else:
         print("Il n' y pas d'autre cas ... debug ..")


