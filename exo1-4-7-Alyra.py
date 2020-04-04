#!/usr/bin/python
# -*- coding: utf-8 -*


#Écrire une fonction en mesure d’interpréter la validité d’une transaction Pay-to-pubkey-hash en prenant en paramètre ScriptSig et ScriptPubSig. On pourra considérer OP_CHECKSIG toujours vrai.
#Exemple:
#verificationP2PKH(“0x483045022100d544eb1ede691f9833d44e5266e923dae058f702d2891e4ee87621a433ccdf4f022021e40 5c26b0483cd7c5636e4127a9510f3184d1994015aae43a228faa608362001210372cc7efb1961962bba20db0c6a3eebdde0ae60698 6bf76cb863fa460aee8475c”, “0x76a9147c3f2e0e3f3ec87981f9f2059537a355db03f9e888ac”) -> True


import hashlib

# 0x76 OP_DUP Duplique l’item en haut de la pile
# 0xa9 OP_HASH160 Effectue un SHA-256 puis un RIPEMD-160 sur l’élément en haut de la pile

# 0x88 OP_EQUALVERIFY Retourne vrai si les deux premiers éléments de la pile sont égaux (bit à bit) et puis dépile cette valeur si elle est vraie. Sinon le script termine avec une erreur (la transaction est donc invalide)
# 0xac OP_CHECKSIG Prend en paramètre une signature et une clé publique. 
#Hash160 de l’ensemble de la transaction, puis vérifie que la signature correspond bien à la signature de ce hash par la clé publique

# Ces codes se trouve dans scriptPubKey au début et à la fin 
# >0x76 >a9 147c3f2e0e3f3ec87981f9f2059537a355db03f9e8 >88 >ac

#Il faut déjà décomposer scriptSign 0x483045022100d544eb1ede691f9833d44e5266e923dae058f702d2891e4ee87621a433ccdf4f022021e405c26b0483cd7c5636e4127a9510f3184d1994015aae43a228faa608362001210372cc7efb1961962bba20db0c6a3eebdde0ae606986bf76cb863fa460aee8475c
#Pour Obtenir la signature d'un côté et la clé publique de l'autre000000000

operators = {"0x76": "OP_DUP",
            "0xa9": "OP_HASH160",
            "0x88": "OP_EQUALVERIFY", 
            "0xac": "OP_CHECKSIG"
             } #type dictionnaire qui nous sera utile plus tard dans les autres exercices 

def bytestohex(data):     
    res = ''.join(format(x, '02x') for x in data) 
    return res


def extractionSignature (ScriptSign):
    SizeSignature = ScriptSign[0] + ScriptSign[1]  #La longueur de la signature est dans le premier octet
    print ("longueur Signature",  int(SizeSignature,  16))
    TabScriptSign = bytearray.fromhex(ScriptSign)
    v = memoryview(TabScriptSign)
    BDepart = 1
    BFin = BDepart +  int(SizeSignature,  16) 
    Signature = bytes(v[BDepart:BFin])  #La signature est ici
    print("[Raw Signature] :", Signature)
    print("longueur de cette Signature :", len(Signature))
    SignatureHexa =  bytestohex(Signature)
    print("Signature en hexa : ",  SignatureHexa)
    print("--------------------")         
    return SignatureHexa


def extractionpubKey (ScriptSign):
    TabScriptSign = bytearray.fromhex(ScriptSign)
    SizeSignature = ScriptSign[0] + ScriptSign[1]  # On a besoin de savoir la longueur de la signature
    print ("longueur Signature [bis]",  int(SizeSignature,  16))
    SizePubKey = bytestohex(TabScriptSign[int(SizeSignature,  16) + 1: int(SizeSignature,  16) + 2])
    print("longueur Clé publique en hexa : ",  SizePubKey)
    v = memoryview(TabScriptSign)    
    BDepart = int(SizeSignature,  16) + 2 #+ 2 car la longueur de la clé publique est codée après la valeur de la signature
    BFin = BDepart +  int(SizePubKey, 16) 
    pubKey = bytes(v[BDepart:BFin])  #pubKey
    print("[Raw Clé Publique] :", pubKey)
    print("longueur de cette Clé Publique :", len(pubKey))
    pubKeyHexa =  bytestohex(pubKey)
    print("Clé publique en hexa : ",  pubKeyHexa)     
    print("--------------------")
    return pubKeyHexa




def double_hash(PubKey):
    b1= bytearray.fromhex(PubKey)
    m = hashlib.sha256()
    m.update(b1)
#  print("m.digest : ",  m.digest())
    first_hash = hashlib.sha256(m.digest()).hexdigest()
    print("first hash en hexa : ",  first_hash)
    b2= m.digest()
    h = hashlib.new('ripemd160')
    h.update(b2)
#    print("h.digest : ",  h.digest())
    second_hash = h.hexdigest()
    print("second hash en hexa : ", second_hash)
    return second_hash




def verification2P2PKH(ScriptSign, ScriptPubKey):
    ExpressionAcalculer = extractionSignature (ScriptSign)
    ExpressionAcalculer += " "
    ExpressionAcalculer += extractionpubKey (ScriptSign) 
    ExpressionAcalculer += " "    
    
    TailleScriptPubKey = len(ScriptPubKey)
    print("Taille du ScriptPubKey : ",  TailleScriptPubKey )
    Operateur1 = ScriptPubKey[0] + ScriptPubKey[1]
    ExpressionAcalculer += "0x" + Operateur1    
    ExpressionAcalculer += " "    
    Operateur2 = ScriptPubKey[2] + ScriptPubKey[3]
    ExpressionAcalculer += "0x" + Operateur2    
    ExpressionAcalculer += " "    
    ExpressionAcalculer += ScriptPubKey[6:TailleScriptPubKey-4]   #ad hoc il y a deux octets dont on ne veut pas
    ExpressionAcalculer += " "    
    Operateur3 = ScriptPubKey[TailleScriptPubKey -4] + ScriptPubKey[TailleScriptPubKey -3]
    ExpressionAcalculer += "0x"+ Operateur3
    ExpressionAcalculer += " "        
    Operateur4 = ScriptPubKey[TailleScriptPubKey -2] + ScriptPubKey[TailleScriptPubKey -1]
    ExpressionAcalculer += "0x"+ Operateur4    
    ExpressionAcalculer =  ExpressionAcalculer.split()
    
    print("Expression à calculer  : ",  ExpressionAcalculer)
    result = [] # result est une pile vide au départ
    for terme in ExpressionAcalculer:
        if terme in operators.keys():
            print("Le terme est l'opérateur -> ",  terme)
            if terme == "0x76": # OP_DUP->  on pop et on réempile deux fois de suite
                elem = result.pop()
                print ("element au dessus de la pile" ,  elem)
                print("on dépile .... ")
                print("on ré-empile une première fois ..... ")
                result.append(elem) 
                print("on ré-empile une deuxième fois ..... ")
                result.append(elem)
                print("OP_DUP -> OK")
                print("ETAT DE LA PILE :",  result)
                print("---------------------")
            if terme == "0xa9": # OP_HASH160 Effectue un SHA-256 puis un RIPEMD-160 sur l’élément en haut de la pile
                elem = result.pop()
                print ("element au dessus de la pile" ,  elem)
                print("on dépile .... ")

                result.append(double_hash(elem))
                print("on empile le double hash de cet element au sommet de la pile ")
                print("OP_HASH160 -> OK")
                print("ETAT DE LA PILE :",  result)
                print("---------------------")
            if terme ==  "0x88": # OP_EQUALVERIFY Retourne vrai si les deux premiers éléments de la pile sont égaux (bit à bit) et puis dépile cette valeur si elle est vraie. 
                #Sinon le script termine avec une erreur (la transaction est donc invalide)
                elem1 = result.pop()
                print("on dépile .... ")
                elem2 = result.pop()
                print("on dépile .... ")
                print ("Comparons les deux éléments en haut de la pile",  elem1 + " et "  + elem2)
                print ("Est-ce que les deux élements au-dessus de la pile sont égaux [bits à bits] ?")
                if (elem1 != elem2):
                    print (" ERREUR !")
                    break
                else:
                    print ("Ils sont bien égaux : VICTOIRE")
                    print("EQUALVERIFY -> OK")
            if terme ==  "0xac": # OP_EQUALVERIFY Retourne vrai si les deux premiers éléments de la pile sont égaux (bit à bit) et puis dépile cette valeur si elle est vraie. 
                print("OP_CHECKSIG -> OK")
        else:
            result.append(terme) 
            print("tant qu'on ne tombe pas sur un opérateur on empile ....   : ") #on empile successivement 
    return result[0] #le résultat est le premier et dernier élément de la pile

ScriptSign = '483045022100d544eb1ede691f9833d44e5266e923dae058f702d2891e4ee87621a433ccdf4f022021e405c26b0483cd7c5636e4127a9510f3184d1994015aae43a228faa608362001210372cc7efb1961962bba20db0c6a3eebdde0ae606986bf76cb863fa460aee8475c'
ScriptPubKey = '76a9147c3f2e0e3f3ec87981f9f2059537a355db03f9e888ac'

print("ETAT DE LA PILE FINALE : ",  verification2P2PKH(ScriptSign, ScriptPubKey))
