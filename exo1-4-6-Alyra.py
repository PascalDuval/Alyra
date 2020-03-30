#!/usr/bin/python
# -*- coding: utf-8 -*

#Calculatrice en notation polonaise

# Une pile n'est rien d'autre qu'une liste
# On ajoute le nombre "1" au sommet de la pile par pile.append(1).On a pile = [1]
# On ajoute "2" au sommet de la pile par pile.append(2). Nous ne pouvons plus accéder à "1" car il est en dessous.
# On a pile = [1,2]
# La méhode pop retourne l'objet en sommet de pile (ici 2) et le supprime de la liste. 
# si sommet = pile.pop() on a donc sommet = 2 et pile = [1]

# même chose que L'exercice précédne

import operator

operators = {"+": operator.add,
             "-": operator.sub,
             "*": operator.mul,
             "/": operator.truediv, 
             "<": operator.lt, 
             ">": operator.gt, 
             "=": operator.gt
             } #type dictionnaire qui nous sera utile plus tard dans les autres exercices 
           
def read():
    return input("Entrez une suite de termes espacés par des blancs, par exemple |12 4 - 2 *| ou ce qui revient au même |2 12 4 - *| : ").split() # Je récupère directement la liste des mots

def eval(expr):
    print("Expression à calculer  : ",  expr)
    result = [] # result est une pile vide au départ
    for terme in expr:
        if terme in operators.keys():
            print("Le terme est un opérateur")
            op1 = result.pop()  #On depile
            print("Sommet de la pile operande1 : ", op1)
            print("On depile -> pile restante  : ", result)

            op2 = result.pop()  #On depile
            print("Sommet de la pile operande2  : ", op2)
            print("On depile -> pile restante :  ", result)

          # On utilise le dictionnaire 
            result.append(operators[terme](op2,op1))
            # On Calcule et on empile
            print("on calcule %d %s %d : " %(op2,  terme,  op1)) 
            print(" .. et on empile le resultat de ce calcul au dessus de la pile restante  : ",  result)
        else:
            result.append(int(terme)) 
            print("on empile successivement   : ",  result) #on empile successivement les nombres
    return result[0] #le résultat est le premier et dernier élément de la pile

if __name__ == "__main__":
    Expression = input("Entrez une suite de termes espacés par des blancs, par exemple |12 4 - 2 *| ou ce qui revient au même |2 12 4 - *| : ").split() 
    print("Le resultat est : ",  eval(Expression))
