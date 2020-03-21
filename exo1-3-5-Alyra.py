#!/usr/bin/python
# -*- coding: utf-8 -*

#Écrire un programme qui génère une adresse type bitcoin à partir d’un nombre:
#Calculer le hash SHA 256 puis RIPEMD160
#Ajouter l’identifiant au début, et le contrôle à la fin
#Convertir le nombre en base 58


#Clé publique
#À partir d’un nombre aléatoire, clé_privée, la clé publique est, en cryptographie à courbe elliptique, la multiplication d’un point générateur G par ce nombre.
#clé_publique = clé_privée * G (modulo n)
#La clé publique est donc constituée de deux nombres, généralement représentés sur 256 bits. Pour présenter ces nombres sous forme hexadécimale, par convention on place 04 devant.

#Une fois obtenue la clé publique, il reste à la convertir en une adresse utilisable aisément.
#La première étape consiste à prendre le hash du hash de la clé publique. 
#On utilise SHA-256 comme premier algorithme, puis la fonction RIPEMD160. On obtient alors un hash sur 20 octets ( 160 bits) de la clé publique.
#La seconde étape consiste à ajouter un préfixe qui permet d’identifier le type d’adresse. 
# En notation hexadécimale on ajoute 0x00 pour les adresses du réseau principal  et 0x6f pour les adresses du réseau testnet.

#L’étape suivante consiste à sécuriser l’adresse en ajoutant quatre octets de contrôle. 
# Pour ce faire, on effectue un double hash (SHA-256) de l’adresse de l’étape précédente, et on place à la fin les 4 premiers octets de cette opération. 
# Comme pour les numéros de sécurité sociale, cela évite les erreurs de frappes.

#La dernière étape consiste à convertir le résultat en base 58. 

#Vous connaissez les nombres en base 10 depuis l’école primaire. 
#Nous avons vu en détail les nombres en base 2, binaires, et 16, hexadécimaux. 
#La représentation en base 58 se fait avec un alphabet de 58 lettres minuscules, majuscules et chiffres, sans le chiffre 0, la lettre O majuscule,
#L minuscule et i majuscule, en ce qu’ils sont susceptibles de porter à confusion.

import hashlib

def good_public_key():   # on place x04 devant une clé ad hoc de 32 Bytes
    good =  b"\x04" + b"%U\x87\x9az\xb2\xa4\x9e@\xa0\xf2\x0b~\xdfX\xdb\xf8\xec\x89\xdb\x9b\x1c\xdeE\xd8\xdd]\xc6\xef'&\xf6"
    return good

def sha256(data):
    firsthash = hashlib.new("sha256")
    firsthash.update(data)
    return firsthash.digest()

def ripemd160(data):
    secondhash = hashlib.new("ripemd160") 
    secondhash.update(data)
    return  (b"\x00" + secondhash.digest())  # et on place x00 devant pour une adresse mainnet
#  return  (b"\x00" + secondhash.digest()).hex()

#L’étape suivante consiste à sécuriser l’adresse en ajoutant quatre octets de contrôle. 
# Pour ce faire, on effectue un double hash (SHA-256) de l’adresse de l’étape précédente, et on place à la fin les 4 premiers octets de cette opération. . 
#on doit extraire les 4 premiers octets de cette opération

def checksum(data):
    adressehashee1 = sha256(data)
    adressehashee2 = sha256(adressehashee1)
    return adressehashee2[:4]
 
def b58(data):
    B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz" #La représentation en base 58 se fait avec un alphabet de 58 lettres minuscules, majuscules et chiffres, sans le chiffre 0, la lettre O majuscule,
    if data[0] == 0:
        return "1" + b58(data[1:])
    x = sum([v * (256 ** i) for i, v in enumerate(data[::-1])])
    ret = ""
    while x > 0:
        ret = B58[x % 58] + ret
        x = x // 58
    return ret


if __name__ == "__main__":
    print("----------")
    print("On fixe une clé publique avec x04 devant (en l absence d algo pour l instant) : ",  good_public_key ())
    print("----------")
    print("Premier hash avec sha256 de cette clé publique : ",  sha256(good_public_key()))
    print("----------")
    print("Second hash avec ripemd160 qu on a correctement préfixé avec X00: ",  ripemd160(sha256(good_public_key())))
    print("----------")
    print("Calcul du checksum de l adresse obtenue par double sha256 qu on mettra à la fin : ", checksum(ripemd160(sha256(good_public_key()))))
    print("----------")    
    print("Représentation de l adresse complète en base B58 : ",  b58((ripemd160(sha256(good_public_key())))+ checksum(ripemd160(sha256(good_public_key()))) ))
