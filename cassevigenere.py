#!/usr/bin/python
# -*- coding: utf-8 -*


ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Calcul de l'indice de coincidence cf http://isn.irem.univ-mrs.fr/2012-2013/media/resources/Vigenere.pdf

def IC(texte) :
    occ = { }
    n = len(texte)
    for car in texte:
        if car in occ:
            occ[car] = occ[car] + 1
        else:
            occ[car] = 1
    ic = 0.0
    for car in occ.keys(): ic += occ[car]*(occ[car] - 1)/n/(n-1)
    return ic

def decal(car, d) :
    return chr((ord(car) - ord('A') + d) % 26 + ord('A'))

def convertCarCode(car) :
    return ord(car) - ord('A')

# Construction d'un texte avec un alphabet décalé de d. 

def cesar(texte, d) :
    texteDecale = ''
    for car in texte : texteDecale = texteDecale + decal(car, d)
    return texteDecale


def rechercheCle(texte, lgCle) :
# On va découper le texte en regroupant toutes les cinquième lettres (longueur de la clé) depuis la première, puis la deuxième et ainsi de suite
    texte0 = texte[0:len(texte):lgCle]
    decalages = [0]
    for k in range(1, lgCle) :
        IcMax = 0
        decalage = -1
        textek = texte[k:len(texte):lgCle]
        for d in range(0,26) :
            Ic = IC(texte0 + cesar(textek, d)) #et on calcule l'incidence sur chaque portion du texte ainsi obtenu auquel on fait subir un decalage à chaque fois d'une lettre
            if Ic > IcMax :
                IcMax = Ic
                decalage = d
        decalages.append(decalage)
# On reprend le texte et on applique tous les décalages; on cherche la lettre la plus fréquente
    occ = { }
    for i in range(0, len(texte)) :
        car = cesar(texte[i], decalages[i % lgCle])
        if car in occ:
            occ[car] = occ[car] + 1
        else:
            occ[car] = 1
    max = 0;
    for car in occ.keys():
        if occ[car] > max :
            max = occ[car];
            carE = car;
    delta = (26 + ord(carE) - ord('E') ) % 26

# Maintenant on connait la cle
    cle = ''
    for d in decalages :
        cle = cle + ALPHABET[(delta - d) % 26]
    return cle

# On decrypte Vigenere avec la cle

def decrypte(texte, cle) :
    lgCle = len(cle)
    clair = ''
    for i in range(0, len(texte)) :
        code = (convertCarCode(texte[i]) - convertCarCode(cle[i % lgCle])) % 26
        clair = clair + ALPHABET[code]
    return clair
    
# Debut du programme de cryptanalyse de Vigenere
#-----------------------------------------------
def casse(texte) :
    lgCle = 5 #on part du principe que la clé est de longueur 5
    print("On pars du principe que la longueur de la clé = ",lgCle)
    cle = rechercheCle(texte, lgCle)
    print("Cle = ", cle)
    clair = decrypte(texte, cle)
    print(clair)
texte = "PVADGHFLSHPJNPLUVAGXVVRBRUKCGXEVQINPVBXLVZLRMKFLSXEZQXOGCCHXEICIXUKSCXKEDDKORRXHPHSXGGJRRHPESTJWVBTJWVJFNGJSCLQLBJGUVSATNRJXFKKCBTKJOJXEVJJBQLATNZHSXECUCIBGELTGVGCJOGERPMQLRBHOVLIKGMCAXTCCHXEICIXUKYRVGJQXUNVYIHWJATLVSGTGRFSGJWFGXEARSCITFZAXOVBJLGTPTMEVOJBHRGIITFZAXOVBPGUCCHXEICIVGJRFNKCNTNVVRGXFZTJEILCIKCYGGXXVJTHGUGEXHZLXMRRPSXEYGUYTVPAXPZEBXFLQEAKEVHBXFSHOQLJTSRVPRXTCCHLGTPTMUTCHMNRRPVJVBTECIYXLQECCNPJCCLEVQIECKYRAGUCATRYGAHUFNWBGRSRHPKPPBTVJTFAJRTKGVQIICIBTYKEGIBQEBJGCLRGXQIBGXSLCAXRIMQEGDCXEGJRXGCTATLUZZAXCCYGTKJMCWCEQAXUDWHMGICHWGCYCMKHSXMGJCJEUUCGTTVQXGKKGTLRRPKBGELTGVRJPVQDNGXJVLHBQEBJFAJRTKGVRAXEYPXLVZYCBUDCTLVSCPNEFSEINLQGTFZAPEGEADKGCCBRUKCGXGJRRXSLGTLVRZHHNLKTGVZLPVEVQHBDCCPECIYXLQERWHORQSTSLGCEGGJJLIIYCWVYCDEQXGTGFVRDNVVJPVJICIBGERTFGUGTOCCCTMNRPTYGICCVGVLRHTVYJCQLPSAWZBTMQLRTECKFTHNFEXXEYPTMKVLCXKEQXLVVQJKNVDPBVHSTECIYIBQEYABVVQPKTVRTTWJCJBNUSBRUKCGXNVKNLVVPTXUKQPVTVQXOQLQEKGWCGXBZJTLVKPPGUTCCWCERXEGJRSBXZLPEQIQFNGCCHXEICIXUKNGHHRLTEGJCRKGKCHMKDKPGGERPECTMCWKKGDGJLKPBPVGAXUKFJFCZLTMEVQIIQLPFNQZDXWGCCPLCMMRTVZMCECGPDUNVKPMKJYIBQEJPKGWJTQKFLEAKCMHHRYGFNGZLIXTIMVXNVQTVTVRXGVVPGHIVJWNORLXMGUSHXEICILKTCITKKSCFAJRTKGVJAXPVJXGVVPGHIVPPBVGYHEGDWHMGICCXUKNPLWECRTVVEDKKVNWBNFQDIJZOJX"
casse(texte)
