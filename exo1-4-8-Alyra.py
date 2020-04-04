#!/usr/bin/python
# -*- coding: utf-8 -*


from datetime import datetime

timestamp = pow(2, 32)
datebug = datetime.fromtimestamp(timestamp)

print("Nombre de secondes depuis 1970 [2³² car la date est codée sur 4 octets]: " ,  timestamp)
print("Sachant qu’il s’agit d’une date en seconde depuis 1970, cette taille posera problème le : ", datebug)

