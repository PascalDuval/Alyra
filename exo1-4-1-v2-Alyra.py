#!/usr/bin/python
# -*- coding: utf-8 -*

def IntobytesBE(Nbre):
    BytesForHexBE = Nbre.to_bytes((Nbre.bit_length() + 7) // 8, 'big')
    return   BytesForHexBE  
     
 
def IntobytesLE(Nbre):
    BytesForHexBE = Nbre.to_bytes((Nbre.bit_length() + 7) // 8, 'little')
    return   BytesForHexBE  
 
     
def bytestohex(data):     
    res = ''.join(format(x, '02x') for x in data) 
    resdef = ("0x" + res)
    return resdef
     
if __name__ == "__main__":
    Nbre = int(input('Entrez un nombre : '))
    print("----------")
    print("représentation du nombre en bytes pour conversion big-endian : ",  IntobytesBE(Nbre))
    print("----------")
    print("conversion big-endian en hexa : ",  bytestohex(IntobytesBE(Nbre)))
    print("----------")
    print("réaffichage du nombre de départ à partir de bigendian : ", int. from_bytes (IntobytesBE(Nbre), "big"))
    print("----------")
    print("représentation du nombre en bytes pour conversion little-endian : ",  IntobytesLE(Nbre))
    print("----------")
    print("conversion little-endian en hexa : ",  bytestohex(IntobytesLE(Nbre)))
    print("----------")
    print("réaffichage du nombre de départ à partir de bigendian : ", int. from_bytes(IntobytesBE(Nbre), "big"))

    print("----------")
    print("réaffichage du nombre de départ à partir de littlendian : ", int. from_bytes(IntobytesLE(Nbre), "little"))


