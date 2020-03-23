#!/usr/bin/python
# -*- coding: utf-8 -*

#Compléter la fonction de l’exercice précédent pour convertir un nombre en sa notation variable little endian
#Reprendre le programme de conversion de l’exercice précédent pour donner la notation hexadécimale en entier variable d’un nombre donné
#Par exemple:
#conversion(466321)
#466321→ 0x 07 1d 91 (big endian)
#→ 0x 91 1d 07 (little endian)
#→ 0x fe 91 1d 07 00 (notation variable)
#Si le premier octet est 0xfd : la valeur du VarInt est contenue dans les 2 octets suivants (little-endian)
#Si le premier octet est 0xfe : la valeur du VarInt est contenue dans les 4 octets suivants (little-endian)
#Si le premier octet est 0xff : la valeur du VarInt est contenue dans les 8 octets suivants (little-endian)
#Sinon : la valeur du VarInt est la valeur du premier octet.
#conversion(466321) -> 0xfe911d0700
# Si le nombre est supérieur à 253, le premier octet indique avec 0xfd, 0xfe ou 0xff, qu’il est suivi du nombre sur respectivement deux, quatre ou huit octets en notation little endian. Ce type de variable s’appelle VarInt ( pour entier variable)
#int.to_bytes(length, byteorder, *, signed=False)
#Renvoie un tableau d’octets représentant un nombre entier.
#(1024).to_bytes(2, byteorder='big')
#b'\x04\x00'
#(1024).to_bytes(10, byteorder='big')
#b'\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00'
#(-1024).to_bytes(10, byteorder='big', signed=True)
#b'\xff\xff\xff\xff\xff\xff\xff\xff\xfc\x00'
#x = 1000
#x.to_bytes((x.bit_length() + 7) // 8, byteorder='little')
#b'\xe8\x03'
#L’entier est représenté par length octets. Une exception OverflowError est levée s’il n’est pas possible de représenter l’entier avec le nombre d’octets donnés.
#L’argument byteorder détermine l’ordre des octets utilisé pour représenter le nombre entier. Si byteorder est "big", l’octet le plus significatif est au début du tableau d’octets. Si byteorder est "little", l’octet le plus significatif est à la fin du tableau d’octets. Pour demander l’ordre natif des octets du système hôte, donnez sys.byteorder comme byteorder.
#L’argument signed détermine si le complément à deux est utilisé pour représenter le nombre entier. Si signed est False et qu’un entier négatif est donné, une exception OverflowError est levée. La valeur par défaut pour signed est False.




import struct
import sys

def IntobytesBE(data):
     BytesForHexBE = struct.pack(">I", data)
     sys.byteorder = "big"
     return   BytesForHexBE 
     
     
def IntobytesLE(data):
     BytesForHexBE = struct.pack("<I", data)
     sys.byteorder = "little"
     return   BytesForHexBE  
     
     
def bytestohex(data):     
# res = ''.join(format(x, '02x') for x in data) 
    res = ''.join(format(x, '02x') for x in data) 
    resdef = ("0x" + res)
    return resdef

def bytestohexwithVarInt(data):     
# res = ''.join(format(x, '02x') for x in data) 
    res = ''.join(format(x, '02x') for x in data) 
    if Nbre.bit_length() == 8:
        resdef = ("0xfd" + res)
    elif  ((Nbre.bit_length()> 8)  and  (Nbre.bit_length() <=32 )):
        resdef = ("0xfe" + res)
    elif Nbre.bit_length() > 32:
        resdef = ("0xff" + res)
    elif Nbre.bit_length() < 8:      
        resdef = res + res
    return resdef


def reaffichage(data):
    result = bytes.fromhex(data)
    return result
#en entree : bytestohexwithVarInt(IntobytesLE(Nbre)) (=0xfe19284700)
#retenir 19284700
# int(bytestohex(IntobytesBE(Nbre)), 16)

        
if __name__ == "__main__":
    Nbre = int(input('Entrez un nombre : '))
    print("----------")
    print("longueur du nombre en bits : ",  Nbre.bit_length())
    print("----------")
    print("représentation du nombre en bytes pour conversion big-endian : ",  IntobytesBE(Nbre))
    print("----------")
    print("tableau pour big -endian (autre méthode) : ",  Nbre.to_bytes((Nbre.bit_length() + 7) // 8, byteorder='big'))
    print("----------")
    print("Byteorder : ",  sys.byteorder)
    print("----------")
    print("conversion big-endian en hexa sans notation variable : ",  bytestohex(IntobytesBE(Nbre)))
    print("----------")
    print("représentation du nombre en bytes pour conversion little-endian : ",  IntobytesLE(Nbre))
    print("----------")    
    print("tableau pour little-endian  (autre méthode) : ",  Nbre.to_bytes((Nbre.bit_length() + 7) // 8, byteorder='little'))
    print("----------")
    print("Byteorder : ",  sys.byteorder)    
    print("----------")
    print("conversion little-endian en hexa sans notation variable",  bytestohex(IntobytesLE(Nbre)))
    print("----------")
    print("conversion little-endian en hexa avec notation variable : ", bytestohexwithVarInt(IntobytesLE(Nbre)))
    print("----------")
    

