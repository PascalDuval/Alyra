#!/usr/bin/python
# -*- coding: utf-8 -*

#Écrire un programme qui sépare sur une ligne différente chaque champ de l’entrée suivante :
#941e985075825e09de53b08cdd346bb67075ef0ce5c94f98853292d4bf94c10d010000006b483045022100ab44ef425e6d85c03cf301bc16465e3176b55bba9727706819eaf07cf84cf52d02203f7dc7ae9ab36bead14dd3c83c8c030bf8ce596e692021b66441b39b4b35e64e012102f63ae3eba460a8ed1be568b0c9a6c947abe9f079bcf861a7fdb2fd577ed48a81Feffffff

#Chaque nouvelle entrée a elle-même 4 champs:

#Le hash de la transaction passée où sont les bitcoins à dépenser (sur 32 octets)

#L’index de la sortie (output) de cette transaction concernée (sur 4 octets)

#ScriptSig, essentiellement la signature et les informations qui correspondent aux conditions de dépense inscrites dans la transaction de départ (voir ci-dessous Script). 
#Le plus souvent, ce champs est composé d'une signature puis de la clé publique correspondante.

#Il vous faut rajouter un VarInt global devant le ScriptSig :

#VarInt ScriptSig
#VarInt signature
#Signature
#VarInt clé publique
#Clé publique
#...Aussi, les VarInt ne font pas toujours un octet.

#Séquence (sur 4 octets) : au départ ce nombre a été prévu pour permettre les transferts rapides à l’image de ce que permet aujourd’hui le lightning network. 
#Concrètement, on peut initialiser la séquence à 0 et définir un locktime (voir plus bas) de la transaction à une certaine distance en temps, par exemple 1008 blocs. 
#Des transactions intermédiaires sont échangées, numérotées par la séquence, et une dernière transaction permet de solder le compte. 
# Cette approche n’est plus utilisée, car elle comporte des défauts de conception. 
#Il est par exemple possible de faire miner une transaction qui ne serait par la dernière. Ce champ peut être désactivé avec la valeur 0xffffffff. Ce n'est pas le cas ici.


def bytestohex(data):     
    res = ''.join(format(x, '02x') for x in data) 
    return res


Tabresult = bytearray.fromhex('941e985075825e09de53b08cdd346bb67075ef0ce5c94f98853292d4bf94c10d010000006b483045022100ab44ef425e6d85c03cf301bc16465e3176b55bba9727706819eaf07cf84cf52d02203f7dc7ae9ab36bead14dd3c83c8c030bf8ce596e692021b66441b39b4b35e64e012102f63ae3eba460a8ed1be568b0c9a6c947abe9f079bcf861a7fdb2fd577ed48a81Feffffff')
print ("Transaction à décomposer :",  Tabresult)
print("Nombre de bytes de cette transaction :", len(Tabresult))
#premier champ  Le hash de la transaction passée où sont les bitcoins à dépenser (sur 32 octets)
v = memoryview(Tabresult)

Premierchamp = bytes(v[0:32])
print("Premier champ de cette transaction [hash] :", Premierchamp)
print("Nombre de bytes de ce champ :", len(Premierchamp))
PremierchampHexa = "0x" + bytestohex(Premierchamp)
print("Hash en hexa : ",  PremierchampHexa)     



Deuxiemechamp = bytes(v[32:36])
print("Deuxième champ de cette transaction [index de la sortie] :", Deuxiemechamp)
print("Nombre de bytes de ce champ :", len(Deuxiemechamp))
DeuxiemechampHexa = "0x" + bytestohex(Deuxiemechamp)
print("output de cette transaction en hexa : ",  DeuxiemechampHexa)     
print("output de cette transaction en int  : ",  int(DeuxiemechampHexa , 16))


Troisiemechamp = bytes(v[36:144])
print("Troisième champ de cette transaction [ScriptSig] :", Troisiemechamp)
print("Nombre de bytes de ce champ :", len(Troisiemechamp))
TroisiemechampHexa = "0x" + bytestohex(Troisiemechamp)
print("ScriptSig en hexa : ",  TroisiemechampHexa)     

Quatriemechamp = bytes(v[144:148])
print("Quatrieme champ de cette transaction [Séquence]:", Quatriemechamp)
print("Nombre de bytes de ce champ :", len(Quatriemechamp))
QuatriemechampHexa = "0x" + bytestohex(Quatriemechamp)
print("Séquence en hexa : ",  QuatriemechampHexa)     
print("Cette séquence n est pas utilisée")

