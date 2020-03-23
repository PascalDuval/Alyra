#!/usr/bin/python
# -*- coding: utf-8 -*


#Écrire un programme qui convertisse un nombre décimal en sa version hexadécimal little endian et hexadécimal big endian sans avoir recours aux fonctions de conversion du langage utilisé
#conversion(466321)
#466321 → 0x 07 1d 91 (big endian)
#             → 0x 91 1d 07 (little endian)
#On va procéder en deux étapes
#1 récupérer le int eb bytes InttoBytes()
# Puis
#2  faire un BytestoHex en big-endian
#2' faire un BytestoHex en little-endian



import struct

def IntobytesBE(data):
     BytesForHexBE = struct.pack(">I", data)
     return   BytesForHexBE 
     
     
def IntobytesLE(data):
     BytesForHexBE = struct.pack("<I", data)
     return   BytesForHexBE  
     
     
def bytestohex(data):     
    res = ''.join(format(x, '02x') for x in data) 
    resdef = ("0x" + res)
    return resdef

#int("FFFF", 16)
#int("0xFFFF", 16)

     
if __name__ == "__main__":
    Nbre = int(input('Entrez un nombre : '))
    print("----------")
    print("représentation du nombre en bytes pour conversion big-endian : ",  IntobytesBE(Nbre))
    print("Calcul de la taille : ",  )
    print("----------")
    print("représentation du nombre en bytes pour conversion little-endian : ",  IntobytesLE(Nbre))
    print("----------")
    print("conversion big-endian en hexa : ",  bytestohex(IntobytesBE(Nbre)))
    print("----------")
    print("conversion little-endian en hexa : ",  bytestohex(IntobytesLE(Nbre)))
    print("----------")
    print("réaffichage du nombre de départ : ", int(bytestohex(IntobytesBE(Nbre)), 16) )


