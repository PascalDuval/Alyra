#!/usr/bin/python
# -*- coding: utf-8 -*

#Compléter la fonction de l’exercice précédent pour convertir un nombre en sa notation variable little endian
#Par exemple:
#conversion(466321)
#466321→ 0x 07 1d 91 (big endian)
#→ 0x 91 1d 07 (little endian)
#→ 0x fe 91 1d 07 00 (notation variable)

#Si le premier octet est 0xfd : la valeur du VarInt est contenue dans les 2 octets suivants (little-endian)
#Si le premier octet est 0xfe : la valeur du VarInt est contenue dans les 4 octets suivants (little-endian)
#Si le premier octet est 0xff : la valeur du VarInt est contenue dans les 8 octets suivants (little-endian)
#Sinon : la valeur du VarInt est la valeur du premier octet.

#conversion(466321) -> 0xfe911d0700 ..



def IntobytesBE(Nbre):
    BytesForHexBE = Nbre.to_bytes((Nbre.bit_length() + 7) // 8, 'big')
    return   BytesForHexBE  
     
 
def IntobytesLE(Nbre):
    BytesForHexBE = Nbre.to_bytes((Nbre.bit_length() + 7) // 8, 'little')
    return   BytesForHexBE  
     
     
def bytestohex(data):     
    res = ''.join(format(x, '02x') for x in data) 
    return res

def bytestohexwithVarInt(data):     
    res = ''.join(format(x, '02x') for x in data) 
    if Nbre.bit_length() <= 8:     # sur un octet
        resdef = bytestohex(Nbre.to_bytes((Nbre.bit_length() + 7) // 8, byteorder='little')) #on ne fait rien de spécial
    elif  ((Nbre.bit_length() > 8) and (Nbre.bit_length() <= 16)):  # sur deux octets 
        resdef = ("fd" + res + "00") #on préfixe avec fd et on remplit à 00 donc sur trois
    elif  ((Nbre.bit_length()> 16)  and  (Nbre.bit_length() <=32 )):  # sur quatre octets 
        resdef = ("fe" + res + "00") #on préfixe avec fe et on remplit donc sur cinq
    elif ((Nbre.bit_length()> 32)  and  (Nbre.bit_length() <=64)): # sur huit octets
        resdef = ("ff" + res + "00") #on préfixe avec ff donc sur 9
    return resdef


def restitution(data):
    Tabresult = bytearray.fromhex(data)
    v = memoryview(Tabresult)
    Premierchamp = bytes(v[0:1])
    resultat = bytes(v[0:1])
    if Premierchamp == b'\xfd':
        resultat = bytes(v[1:4])
    if Premierchamp == b'\xfe':
        resultat = bytes(v[1:6])
    if Premierchamp == b'\xff':
        resultat = bytes(v[1:10])
    return resultat    


        
if __name__ == "__main__":
    Nbre = int(input('Entrez un nombre [ex : 466321]: '))
    print("----------")
    print("longueur du nombre en bits : ",  Nbre.bit_length())
    print("----------")
    print("représentation du nombre en bytes pour conversion big-endian : ",  IntobytesBE(Nbre))
    print("----------")    
    print("conversion big-endian en hexa sans notation variable",  bytestohex(IntobytesBE(Nbre)))
    print("----------")
    print("représentation du nombre en bytes pour conversion little-endian : ",  IntobytesLE(Nbre))
    print("----------")    
    print("conversion little-endian en hexa sans notation variable",  bytestohex(IntobytesLE(Nbre)))
    print("----------")
    print("conversion little-endian en hexa avec notation variable : ", bytestohexwithVarInt(IntobytesLE(Nbre)))
    print("----------")
    print("réaffichage du nombre de départ à partir de l'hexa sans notation variable : ", int(bytestohex(IntobytesBE(Nbre)),  16))
    print("----------")     
    print("réaffichage du nombre à partir de sa représentation en bytes : ", int. from_bytes(IntobytesLE(Nbre), "little"))
    print("----------")     
    print("On retient des bytes pertinents : ",  restitution(bytestohexwithVarInt(IntobytesLE(Nbre))))
    print("----------")
    print("réaffichage du nombre de départ à partir de ces bytes pertinents [little-endian] : ", int. from_bytes(restitution(bytestohexwithVarInt(IntobytesLE(Nbre))), "little"))
    print("----------")

     

     
     
