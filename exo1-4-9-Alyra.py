#!/usr/bin/python
# -*- coding: utf-8 -*
from datetime import datetime
import time
import calendar

#print ("date du jour : ", datetime.date.fromtimestamp(time.time()) )
print("Maintenant en secondes :",   time.time())
 
def convtime(strtime):
    moment = datetime.strptime(strtime, '%Y-%m-%d %H:%M')
    return calendar.timegm(moment.timetuple())
 
print("Nombre de secondes au début [premier bloc] : ",  convtime('2009-01-03 18:15')) #Premier bloc : 3 janvier 2009 à 18h15

IntervalSecondes =  time.time() - convtime('2009-01-03 18:15')
print ("Interval de secondes : ",  IntervalSecondes)

PoidsOctets =  (IntervalSecondes /  (10 * 60)) * 80
print ("Poids en octets : ",  PoidsOctets)
PoidsEnMegOctets =  PoidsOctets * pow(10,  -6)
print ("Poids en méga octets : ",  PoidsEnMegOctets)


# 80 bytes * 6 * 24 * 365 = 4.2MB per year
