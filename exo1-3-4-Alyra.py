#!/usr/bin/python
# -*- coding: utf-8 -*

#Ajouter à la classe courbe elliptique une fonction qui permette de comparer si deux courbes sont égales ( En Python __eq__ permettra d'utiliser l'opérateur d'égalité == )
#Ajouter une fonction testPoint(self,x, y )(en python) ou testPoint(x,y) (en javascript) qui  vérifie si un point appartient à la courbe
# Ajouter une fonction qui retourne une chaîne de caractères avec les paramètres de la courbe


class Point:
    def __init__(self, x, y): #initialise un point sur la courbe
        self.x = x
        self.y = y
        print("coordonnées du point à chercher sur la courbe : ",  (self.x,    self.y))


class CourbeElliptique:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        if (4*a**3+27*b**2) == 0: 
            raise ValueError('({}, {}) n\'est pas une courbe valide'.format(a, b))
        if ((a < 0) or (b < 0)): 
            raise ValueError('({}, {}) les coordonnées de la courbe doivent être positives'.format(a, b))

    def isOn(self, p):
        y_square = (p.x**3 + self.a*p.x + self.b)
        return y_square == p.y**2 #True si le point est sur la courbe

    def __str__(self):
        return "La fonction est : Y^2 = X^3 + (%d)X + (%d)" % (self.a, self.b)

def menu():
    print("1- Afficher les paramètres d'une fonction ")
    print("2- Vérification de la présence d'un point sur une courbe elliptique définie par une foncton")
    print("3- Egalité de deux courbes ?")
    print("4- Quitter")
    choix = int(input("Votre choix : "))
    if (choix == 1):
        print(creation_courbe())
    if (choix == 2):
        test_Point()
    if (choix == 3):
        verif_egalite()
    if (choix == 4):
        exit()

def creation_courbe():
    CoeffA = int(input("Entrez un coefficient A pour la fonction : "))
    CoeffB = int(input("Entrez un coefficient B pour la fonction : "))
    curve = CourbeElliptique(CoeffA, CoeffB)
    return curve

def test_Point():
    Coordx = int(input("Coordonnées en X : "))
    CoordY = int(input("Coordonnées en Y : "))
    M = Point(Coordx, CoordY)
    curve = creation_courbe()
    isOn = CourbeElliptique.isOn(curve, M)
    
    print(isOn)

def verif_egalite():
    print("je n'ai pas compris la question ...")


while 1:
    menu()


