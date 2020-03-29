#!/usr/bin/python
# -*- coding: utf-8 -*

#Écrire un programme qui sépare sur une ligne différente chaque champ de l’entrée suivante : 941e985075825e09de53b08cdd346bb67075ef0ce5c94f98853292d4bf94c10d010000006b483045022100ab44ef425e6d85c03cf301bc16465e3176b55bba9727706819eaf07cf84cf52d02203f7dc7ae9ab36bead14dd3c83c8c030bf8ce596e692021b66441b39b4b35e64e012102f63ae3eba460a8ed1be568b0c9a6c947abe9f079bcf861a7fdb2fd577ed48a81Feffffff
#Cet exercice porte sur une entrée (“input”) alors que le suivant 1.4.4 porte sur une transaction complète.
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

#Dans ScriptSig, les données sont en big-endian (héritage d’OpenSSL), le format est donc [VARINT] [varint] [signature] [varint] [clé publique]


def bytestohex(data):     
    res = ''.join(format(x, '02x') for x in data) 
    return res


def restitutionfromLE(data, longueur):  #Restitution des bytes pertinents pour un varint little-endian de longueur donnée (1, 4, 8, 16)
    Tabresult = bytearray.fromhex(data)
    v = memoryview(Tabresult)
    debut = bytes(v[0:1])
    reste = bytes(v[0:1])
    if longueur==1:
        resultat = debut
        reste = resultat
    if longueur==4:
        resultat = bytes(v[1:4])
        reste=resultat[::-1]
    if longueur==8:
        resultat = bytes(v[1:8])
        reste=resultat[::-1]
    if longueur==16:
        resultat = bytes(v[1:16])
        reste=resultat[::-1]
    return reste    



Tabresult = bytearray.fromhex('941e985075825e09de53b08cdd346bb67075ef0ce5c94f98853292d4bf94c10d010000006b483045022100ab44ef425e6d85c03cf301bc16465e3176b55bba9727706819eaf07cf84cf52d02203f7dc7ae9ab36bead14dd3c83c8c030bf8ce596e692021b66441b39b4b35e64e012102f63ae3eba460a8ed1be568b0c9a6c947abe9f079bcf861a7fdb2fd577ed48a81Feffffff')
print ("Transaction à décomposer :",  Tabresult)
print("Nombre de bytes de cette transaction :", len(Tabresult))
v = memoryview(Tabresult)

Premierchamp = bytes(v[0:32])
print("Premier champ de ce bout de transaction [champ TXID se référant à une transaction en INPUT] :", Premierchamp)
print("Nombre de bytes de ce champ :", len(Premierchamp))
PremierchampHexa = bytestohex(Premierchamp)
print("TXID en hexa non renversé : ",  PremierchampHexa)     
print("------ il faut renverser (cf. https://learnmeabitcoin.com/guide/input) ------ ")     
PremierchampForReverse = Premierchamp
PremierchampReverse =  PremierchampForReverse[::-1]
PremierchampReverseHexa = bytestohex(PremierchampReverse)
print("TXID en hexa renversé : ",  PremierchampReverseHexa)     
print("------------------------------")     


Deuxiemechamp = bytes(v[32:36])
print("Deuxième champ de cette transaction [index de l'OUTPUT] :", Deuxiemechamp)
print("Nombre de bytes de ce champ :", len(Deuxiemechamp))
DeuxiemechampHexa = bytestohex(Deuxiemechamp)
print("OUTPUT en hexa non renversé : ",  DeuxiemechampHexa)     
print("------ il faut renverser (cf. https://learnmeabitcoin.com/guide/input) ------ ")     
DeuxiemechampForReverse = Deuxiemechamp
DeuxiemechampReverse =  DeuxiemechampForReverse[::-1]
DeuxiemechampReverseHexa = bytestohex(DeuxiemechampReverse)
print("OUTPUT en hexa renversé : ",  DeuxiemechampReverseHexa)     
print("------------------------------")     


ScriptSigSize = bytes(v[36:37]) #Indicates the upcoming size of the unlocking code
print("VarInt ScriptSig :", ScriptSigSize)
print("Nombre de bytes de ce Varint :", len(ScriptSigSize))
ScriptSigHexa = bytestohex(ScriptSigSize)
print("ScriptSig Size en hexa : ",  ScriptSigHexa)     
ScriptSigInt = int(ScriptSigHexa,  16)
print("ScriptSig Size en int : ",  ScriptSigInt)     
print("------------------------------")     

# en utilisant la fonction de décodages little endian
#ScriptSigSize = bytes(v[36:37]) #Indicates the upcoming size of the unlocking code
#print("VarInt ScriptSig :", ScriptSigSize)
#print("Nombre de bytes de ce champ :", len(ScriptSigSize))
#ScriptSigHexa = bytestohex(ScriptSigSize)
#print("on extrait les bons octets de ce varint little endian", restitutionfromLE(ScriptSigHexa,  1))
#print("on remet tout à l'endroit : ", bytestohex(restitutionfromLE(ScriptSigHexa,  1)))
#ScriptSigInt = int(bytestohex(restitutionfromLE(ScriptSigHexa,  1)),  16)
#print("ScriptSig Size en int : ",  ScriptSigInt)     



Troisiemechamp = bytes(v[37:37+ScriptSigInt])
print("Troisième champ de cette transaction [ScriptSig] :", Troisiemechamp)
print("Nombre de bytes de ce champ :", len(Troisiemechamp))
TroisiemechampHexa = bytestohex(Troisiemechamp)
print("ScriptSig en hexa : ",  TroisiemechampHexa)     
print("------------------------------")     

 
Quatriemechamp = bytes(v[37+ScriptSigInt:37+ScriptSigInt+4])
print("Quatrieme champ de cette transaction [Séquence]:", Quatriemechamp)
print("Nombre de bytes de ce champ :", len(Quatriemechamp))
QuatriemechampHexa = bytestohex(Quatriemechamp)
print("Séquence en hexa : ",  QuatriemechampHexa)     
print("on extrait les bons octets de ce varint little endian", restitutionfromLE(QuatriemechampHexa,  4))
print("on remet tout à l'endroit : ", bytestohex(restitutionfromLE(QuatriemechampHexa,  4)))
if bytestohex(restitutionfromLE(QuatriemechampHexa,  4)) == "ffffff":
    print("Cette séquence n' est pas utilisée")



