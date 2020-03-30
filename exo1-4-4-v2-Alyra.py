#!/usr/bin/python
# -*- coding: utf-8 -*

# Étant donné la transaction brute suivante écrire dans le langage de votre choix un script qui extrait les différents champs de la transaction. 
#Par simplicité, on pourra dans un premier temps supposer que tous les varInt sont codés sur un octet.
#0100000001f129de033c57582efb464e94ad438fff493cc4de4481729b85971236858275c2010000006a4730440220155a2ea4a702cadf37052c87bfe46f0bd24809759acff8d8a7206979610e46f6022052b688b784fa1dcb1cffeef89e7486344b814b0c578133a7b0bce5be978a9208012103915170b588170cbcf6380ef701d19bd18a526611c0c69c62d2c29ff6863d501affffffff02ccaec817000000001976a9142527ce7f0300330012d6f97672d9acb5130ec4f888ac18411a000000000017a9140b8372dffcb39943c7bfca84f9c40763b8fa9a068700000000


#Sorties
#Les sorties ou outputs représentent les bitcoins qui peuvent être dépensés à l’issue de la transaction. On peut voir chaque sortie comme un montant de bitcoins prêt à être dépensé 
#sous réserve de remplir les conditions prévues.
# Sur la forme, le premier champ désigne le nombre de sorties (au format varInt). Puis, pour chaque sortie on trouve les champs suivants:
#Le montant sous la forme d’un entier en satoshis (1 satoshi = 1 * 10⁻⁸ bitcoin), sur 8 octets
#La taille du Script ( varInt )
#ScriptPubKey qui détermine les conditions auxquelles le montant pourra être dépensé 

import struct

NBYTES_NUMVERSION = 4 #Nombre de Bytes du numéro de Version
NBYTES_INPUTCOUNT = 1 #Nombre de Bytes du compte de inputs en théorie
NBYTES_OUTPUTCOUNT = 1
NBYTES_TXID = 32 #Nombre de Bytes du Txid
NBYTES_VOUT = 4 #Nombre de Bytes de l'Index de sortie
NBYTES_SCRIPTSIGSIZE = 1  #Nombre de Bytes la taille du ScriptSig Size = 1 en théorie ...
NBYTES_SEQUENCE = 4 #Nombre de Bytes d'une séquence

NBYTES_VALUE = 8  #Nombre de Bytes du champ Value pour boucle
NBYTES_SCRIPTPUBKEYSIZE = 1 # #Nombre de Bytes du champ ScriptPubKey Size 

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


TransactionBlock = '0100000001f129de033c57582efb464e94ad438fff493cc4de4481729b85971236858275c2010000006a4730440220155a2ea4a702cadf37052c87bfe46f0bd24809759acff8d8a7206979610e46f6022052b688b784fa1dcb1cffeef89e7486344b814b0c578133a7b0bce5be978a9208012103915170b588170cbcf6380ef701d19bd18a526611c0c69c62d2c29ff6863d501affffffff02ccaec817000000001976a9142527ce7f0300330012d6f97672d9acb5130ec4f888ac18411a000000000017a9140b8372dffcb39943c7bfca84f9c40763b8fa9a068700000000'

#Premier champ
Tabresult = bytearray.fromhex(TransactionBlock)
print ("Transaction à décomposer :",  Tabresult)
print("Nombre de bytes de cette transaction :", len(Tabresult))
v = memoryview(Tabresult)
print("------------------------------") 

BDepart = 0
BFin = BDepart + NBYTES_NUMVERSION   
NumVer = bytes(v[BDepart:BFin])  #le premier champ est le numéro de version
print("[Raw Version] :", NumVer)
NumVerHexa =  bytestohex(NumVer)
print("Valeur de ce numéro de version en hexa : ",  NumVerHexa)     
print("-------------------------------------")

#Deuxiemechamp 
BDepart = BFin
BFin = BDepart + NBYTES_INPUTCOUNT    
InputCount = bytes(v[BDepart:BFin])
print("[Raw InputCount] :", InputCount)
print("Nombre de bytes de ce champ :", len(InputCount))
InputCountHexa = bytestohex(InputCount)
print("Varint du nombre de INPUTS en hexa : ",  InputCountHexa)     
print("Varint du nombre de INPUTS en int  : ",  int(InputCountHexa , 16))
print("-------------------------------------")

#Troisièmechamp 
BDepart = BFin
BFin = BDepart + NBYTES_TXID    
Txid = bytes(v[BDepart:BFin])
print("[Raw TXID se référant à la transaction en INPUT] :", Txid)
print("Nombre de bytes de ce champ :", len(Txid))
TxidHexa = bytestohex(Txid)
print("TXID en hexa non renversé : ",  TxidHexa)     
print("------ il faut renverser (cf. https://learnmeabitcoin.com/guide/input) ------ ")     
TxidForReverse = Txid
TxidReverse =  TxidForReverse[::-1]
TxidReverseHexa = bytestohex(TxidReverse)
print("TXID en hexa renversé : ",  TxidReverseHexa)     
print("------------------------------")     

#quatrièmechamp
BDepart = BFin
BFin = BDepart + NBYTES_VOUT    
Vout = bytes(v[BDepart:BFin])
print("[Raw de cet index de l'OUTPUT] :", Vout)
print("Nombre de bytes de ce champ :", len(Vout))
VoutHexa = bytestohex(Vout)
print("OUTPUT en hexa non renversé : ",  VoutHexa)     
print("------ il faut renverser (cf. https://learnmeabitcoin.com/guide/input) ------ ")     
VoutForReverse = Vout
VoutReverse =  VoutForReverse[::-1]
VoutReverseHexa = bytestohex(VoutReverse)
print("OUTPUT en hexa renversé : ",  VoutReverseHexa)     
print("------------------------------")     

#cinquièmechamp 
BDepart = BFin
BFin = BDepart + NBYTES_SCRIPTSIGSIZE    
ScriptSigSize = bytes(v[BDepart:BFin]) #Indicates the upcoming size of the unlocking code
print("VarInt ScriptSig :", ScriptSigSize)
print("Nombre de bytes de ce Varint :", len(ScriptSigSize))
ScriptSigHexa = bytestohex(ScriptSigSize)
print("ScriptSig Size en hexa : ",  ScriptSigHexa)     
ScriptSigInt = int(ScriptSigHexa,  16)
print("ScriptSig Size en int : ",  ScriptSigInt)     
print("------------------------------")     

#sixièmechamp 
BDepart = BFin
BFin = BDepart + ScriptSigInt #variable
ScriptSig = bytes(v[BDepart:BFin])
print("[Raw ScriptSig] :", ScriptSig)
print("Nombre de bytes de ce champ :", len(ScriptSig))
ScriptSigHexa = bytestohex(ScriptSig)
print("ScriptSig en hexa : ",  ScriptSigHexa)     
print("------------------------------")     

#septièmechamp
BDepart = BFin
BFin = BDepart + NBYTES_SEQUENCE #sur 4 bytes
Sequence = bytes(v[BDepart:BFin])
print("[Raw Séquence]:", Sequence)
print("Nombre de bytes de ce champ :", len(Sequence))
SequenceHexa = bytestohex(Sequence)
print("Séquence en hexa : ",  SequenceHexa)     
print("on extrait les bons octets de ce varint little endian", restitutionfromLE(SequenceHexa,  4))
print("on remet tout à l'endroit : ", bytestohex(restitutionfromLE(SequenceHexa,  4)))
print("------------------------------")     

#huitièmechamp 
BDepart = BFin
BFin = BDepart + NBYTES_OUTPUTCOUNT 
OutputCount = bytes(v[BDepart:BFin])
#OutputCount = bytes(v[46+ScriptSigInt:47+ScriptSigInt])

print("[Raw OutputCount] :", OutputCount)
print("Nombre de bytes de ce champ :", len(OutputCount))
OutputCountHexa = bytestohex(OutputCount)
print("OutPut Count en hexa : ",  OutputCountHexa)     
print("OutPut Count en int  : ",  int(OutputCountHexa , 16))
print("-------------------------------------")


NbreOutputs = int(OutputCountHexa , 16)

BDepart = BFin
BFin = BDepart + NBYTES_VALUE 


i = 0
while i < NbreOutputs:
#Prendre le champ Value (montant) sur 8 bytes et l'afficher
    numOutput = i+1
    ChampValue = bytes(v[BDepart:BFin]) #au premier tour    
    print(f'Montant du OUPUT numéro {numOutput} {ChampValue}')
    print("Nombre de bytes de ce champ :", len(ChampValue))
    print("Raw Montant non inversé : ",  ChampValue)
    ChampValueHexa = bytestohex(ChampValue)
    print("Montant de cet OUTPUT en hexa non renversé : ",  ChampValueHexa)     

    MontantenIntLE = struct.unpack("<Q", ChampValue)   # < is little endian Q = 8
    Montant = MontantenIntLE[0]
    print("MONTANT de cet OUTPUT en SATOSHIS : ",  Montant)  
    print("MONTANT de cet OUTPUT en BITCOIN : ",  Montant * pow(10, -8) )     


#    hexbyte1 = ChampValueHexa[0] + ChampValueHexa[1]
#    hexbyte2 = ChampValueHexa[2] + ChampValueHexa[3]
#    hexbyte3 = ChampValueHexa[4] + ChampValueHexa[5]
#   hexbyte4 = ChampValueHexa[6] + ChampValueHexa[7]
#    hexbyte5 = ChampValueHexa[8] + ChampValueHexa[9]
#   hexbyte6 = ChampValueHexa[10] + ChampValueHexa[11]
#    hexbyte7 = ChampValueHexa[12] + ChampValueHexa[13]
#   hexbyte8 = ChampValueHexa[14] + ChampValueHexa[15]
#    ChampValueReverseHexa = hexbyte8 + hexbyte7 + hexbyte6 + hexbyte5 + hexbyte4 + hexbyte3 + hexbyte2 + hexbyte1
#    print("Montant de cet OUTPUT en hexa renversé (bis) : ",  ChampValueReverseHexa)     
#    print("Montant de cet OUTPUT en SATOSHI : ",  int(ChampValueReverseHexa , 16))
#    print("Montant de cet OUTPUT en BITCOIN : ",  pow (int(ChampValueReverseHexa , 16),  -8))

    print("------------------------------")     
#Prendre le champ ScriptPubKey Size sur un byte - c'est un varint
    BDepart = BFin
    BFin = BFin  + NBYTES_SCRIPTPUBKEYSIZE #le champ ScriptPubKeySize est sur un byte
    ScriptPubKeySize = bytes(v[BDepart:BFin]) #Indicates the upcoming size of the ScriptPubKey
    print("VarInt ScriptPubKey Size :", ScriptPubKeySize)
    print("Nombre de bytes de ce Varint :", len(ScriptPubKeySize))
    ScriptPubKeySizeHexa = bytestohex(ScriptPubKeySize)
    print("ScriptPubKey Size en hexa : ",  ScriptPubKeySizeHexa)     
    ScriptPubKeySizeInt = int(ScriptPubKeySizeHexa,  16)
    print("ScriptPubKey Size en int : ",  ScriptPubKeySizeInt)     
    print("------------------------------")     
#Prendre le champ ScriptPubKey  sur la longueur de ScriptPubKey Size
    BDepart = BFin
    BFin = BFin  + ScriptPubKeySizeInt
    ScriptPubKey = bytes(v[BDepart:BFin])
    print("[Raw ScriptPubKey] :", ScriptPubKey)
    print("Nombre de bytes de ce champ :", len(ScriptPubKey))
    ScriptPubKeyHexa = bytestohex(ScriptPubKey)
    print("ScriptPubKey en hexa : ",  ScriptPubKeyHexa)     
    print("------------------------------")     

    BDepart = BFin
    BFin = BFin + NBYTES_VALUE    
    i = i+1

DernierChamp = bytes(v[len(Tabresult)-4:len(Tabresult)])
# DernierChamp = bytes(v[219:223])
print("Dernier Champ [Séquence]:", DernierChamp)
print("Nombre de bytes de ce champ :", len(DernierChamp))
DernierChampHexa = bytestohex(DernierChamp)
print("Séquence en hexa : ",  DernierChampHexa)     
#print("on extrait les bons octets de ce varint little endian", restitutionfromLE(DernierChamp,  4))
#print("on remet tout à l'endroit : ", bytestohex(restitutionfromLE(DernierChamp,  4)))
#if bytestohex(restitutionfromLE(DernierChampHexa,  4)) == "ffffff":
#print("Cette séquence n' est pas utilisée")


