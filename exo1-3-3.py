#!/usr/bin/python
# -*- coding: utf-8 -*

#1) Choisir deux nombres premiers p et q
#2) Calculer n = pq
#3) Calculer l’indicatrice d’Euler φ(n) = (p - 1)(q - 1)
#4) Choisir un entier c, premier avec  φ(n), et tel que 0<c< φ(n)
#5) Calculer d tel que cd = 1 (mod φ(n)) ( ce qui est équivalent à cd+k(p - 1)(q - 1)=1 )
#Le chiffrement d’un message M est alors obtenu en calculant : M^c  (mod n)
#Le déchiffrement du message C est réalisé au moyen du calcul suivant : C^d (mod n)



def egcd(b, n):
    """
    Given two integers (b, n), returns (gcd(b, n), a, m) such that
    a*b + n*m = gcd(b, n).
    
    Adapted from several sources:
      https://brilliant.org/wiki/extended-euclidean-algorithm/
      https://rosettacode.org/wiki/Modular_inverse
      https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
      https://en.wikipedia.org/wiki/Euclidean_algorithm
      
    >>> egcd(1, 1)
    (1, 0, 1)
    >>> egcd(12, 8)
    (4, 1, -1)
    >>> egcd(23894798501898, 23948178468116)
    (2, 2437250447493, -2431817869532)
    >>> egcd(pow(2, 50), pow(3, 50))
    (1, -260414429242905345185687, 408415383037561)
    """
    (x0, x1, y0, y1) = (1, 0, 0, 1)
    while n != 0:
        (q, b, n) = (b // n, n, b % n)
        (x0, x1) = (x1, x0 - q * x1)
        (y0, y1) = (y1, y0 - q * y1)
    return (b, x0, y0)


#1) Choisir deux nombres premiers p et q
#2) Calculer n = pq
#3) Calculer l’indicatrice d’Euler φ(n) = (p - 1)(q - 1)
#4) Choisir un entier c, premier avec  φ(n), et tel que 0<c< φ(n)
#5) Calculer d tel que cd = 1 (mod φ(n)) ( ce qui est équivalent à cd+k(p - 1)(q - 1)=1 )
#Le chiffrement d’un message M est alors obtenu en calculant : M^c  (mod n)
#Le déchiffrement du message C est réalisé au moyen du calcul suivant : C^d (mod n)

#1) Choisir deux nombres premiers p et q
# L'utilisateur entre p et on fait éventuellement les tests d'usage
p = int(input ('Entrez un nombre premier p  : '))
# L'utilisateur entre q et on fait éventuellement les tests d'usage
q = int(input('Entrez un nombre premier q  : '))


#2) Calculer n = pq (public)
n = p*q
print ("n = ",n)

#3) Calculer l’indicatrice d’Euler φ(n) = (p - 1)(q - 1)
phiden = (p-1)*(q-1)
print ("l'indicatrice d'Euler φ(n) = ", phiden)

#4) Alice choisit un entier c, premier avec  φ(n), et tel que 0<c< φ(n) et on fait éventuellement les tests d'usage
c = int(input('Entrez un nombre c, premier avec φ(n)  et tel que 0< c < φ(n) : '))

#5) Alice calcule d tel que cd = 1 (mod φ(n)) ( ce qui est équivalent à cd+k(p - 1)(q - 1)=1 ) grâce à la fonction egcd :-)
# egcd(c, φ(n)) retourne d et k, tel que d*c + k*φ(n) = pgcd(c,φ(n)) = 1 [puisqu'ils sont premiers entre eux]  - d est la clé.
# Ce sont les coefficients de Bezout

Liste = egcd(c, phiden)
print("Liste renvoyée par egcd ", Liste )
Cle = Liste[1]
print("Cle ", Cle )

#Alice peut communiquer n et c à ses correspondants mais elle garde sa clé privée (d)

#Bob veut envoyer un message secret à Alice. On fait abstraction ici de la transcription ascii.
MessageAChiffrer = int(input("Entrez un nombre [il faut prendre un nombre inférieur à n] : "))
#Le chiffrement d’un message M est alors obtenu en calculant : M^c  (mod n). Bob connaît c et n.
MessageChiffre = int((pow(MessageAChiffrer,  c)) %n) 
print("Le Message chiffré est : ",  MessageChiffre)

#Le déchiffrement du message est réalisé en calculant : C^Cle  (mod n). Seule Alice connaît la clé.
MessageDeChiffre = int((pow(MessageChiffre,  Cle)) %n)
print("Le Message déchiffré est : ",  MessageDeChiffre)
