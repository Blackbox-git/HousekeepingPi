#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import der notwendigen Bibliotheken
import os
import sys
import time
import json
import datenbank
import subprocess as sub
try: 
	from PyDect200 import PyDect200
except:
	print("Programm abgebrochen. Bitte installieren Sie das Projekt zuerst.")
	sys.exit(0)

# PyDect200 initialisieren
PyDect200 = PyDect200.PyDect200

# Zugangsdaten AVM importieren
with open('/home/pi/.credentials/avm.json') as creds:    
	credentials = json.load(creds)

# Setzen der Fritzbox Daten
fritzboxbenutzername = credentials['fritzboxbenutzername']
fritzboxpasswort = credentials['fritzboxpasswort']
Name1 = credentials['Name1']
AIN1 = credentials['AIN1']
try:
	Name2 = credentials['Name2']
	AIN2 = credentials['AIN2']
except:
	Name2 = None
	AIN2 = None
try:
	Name3 = credentials['Name3']
	AIN3 = credentials['AIN3']
except:
	Name3 = None
	AIN3 = None

# Allgemeine Hilfsvariablen anlegen
mysql = 0
verbindung = None
verbindungsversuch = 0
root = os.path.expanduser("~")
aufzeichnungsinterval = 10

# Funktion um eine Verbindung zur Fritzbox herzustellen
def verbinden():
	global verbindungsversuch
	global verbindung
	while verbindungsversuch == 0:
		try:
			verbindung = PyDect200(fritzboxpasswort,fritzboxbenutzername)
		except:
			# print('Fehler aufgetreten. Neuer Versuch.')
			time.sleep(1)
			continue
		if not verbindung.login_ok():
			# print('Verbindung nicht okay. Neuer Versuch.')
			time.sleep(1)
			continue
		else:
			test = verbindung.get_device_name(AIN)
			test = test.encode('ascii', 'ignore')
			if test == "inval":
				time.sleep(1)
				continue
			else:
				print("Verbindung zur FritzBox hergestellt.")
				verbindungsversuch = 1
	verbindungsversuch = 0

# Funktion um zu testen ob die Verbindung zur Fritzbox noch besteht
def verbindungstest():
	global verbindung
	if not verbindung.login_ok():
		verbinden()
		# print("Funktion Verbinden aufrufen, da kein gültiger Login vorliegt.")
		# print("")
	else:
		test = verbindung.get_device_name(AIN)
		if test == "inval" or test == "" or test == None:
			verbinden()
			# print("")
			# print("Funktion Verbinden aufgerufen, da die Fritzbox nicht mehr erreichbar ist.")
			# print("")
		else:
			# print("")
			# print("Verbindungstest erfolgreich.")
			# print("")
			pass

# Funktion zum ermitteln des aktuellen Schaltstatus
def ermittlestatus(device):
	status = verbindung.get_state(device)
	status = status.encode('ascii', 'ignore')
	if status == "inval" or status == "":
		status = "NULL"
	elif status == "0":
		status = 0
	else:
		try:
			status = int(status)
		except:
			status = "NULL"
	return status

# Funktion zum ermitteln des aktuellen Verbrauches in Milliwatt
def ermittlestrom(device):
	strom = verbindung.get_power_single(device)
	strom = strom.encode('ascii', 'ignore')
	if strom == "inval" or strom == "":
		strom = "NULL"
	elif strom == "0":
		strom = 0
	else:
		try:
			strom = int(strom)
		except:
			strom = "NULL"
	return strom

# Benutzereingaben anfordern
if AIN3 == None and AIN2 == None:
	auswahl = [1]
if AIN3 == None and AIN2 != None:
	auswahl = [1,2]
if AIN3 != None:
	auswahl = [1,2,3]
print("")
print("WILLKOMMEN ZUM AUFZEICHNUNGSPROZESS")
print("")
while True:
	try:
		eingabe = input("Bitte wählen Sie die Steckdose aus, welche aufgezeichnet werden soll %s: " %auswahl)
		try:
			eingabe = int(eingabe)
			if eingabe in auswahl:
				if eingabe == 1:
					AIN = AIN1
					Name = Name1
				elif eingabe == 2:
					AIN = AIN2
					Name = Name2
				elif eingabe == 3:
					AIN = AIN3
					Name = Name3
				break
			else:
				print("Die Eingabe ist nicht erlaubt.")
				print("")
				continue
		except: 
			print("Es sind nur die angezeigten Zahlen erlaubt.")
			print("")
			continue
	except:
		print("")
		print("")
		print("Das Programm wurde beendet.")
		print("")
		sys.exit(0)

# Temporäre Datenbank erstelle
print("")
print("Lösche ggf. vorhandene alte temporäre Datenbank Tabelle.")
meldung = datenbank.loeschetemp()
print("")
print("Lege neue temporäre Datenbank Tabelle an.")
meldung = datenbank.erstelletemp()
if meldung == 1:
	print("Die Datenbank kann nicht erstellt werden. Bitte installieren Sie das Projekt zuerst.")
	sys.exit(0)
else:
	print("")

# Verbindung zur Fritzbox aufbauen
verbinden()
print("")
print("Starte die Aufzeichnung für %s:" %(Name))
print("")

# Aufzeichnung inkl. Fehlerbehandlung
try:
	while True:
		verbindungstest()
		status = ermittlestatus(AIN)
		strom = ermittlestrom(AIN)
		if status == 0:
			print('Die Steckdose ist ausgeschaltet. Es erfolgt keine Aufzeichnung.')
			continue
		elif status == "NULL" or strom == "NULL":
			print('Die Steckdose ist nicht erreichbar. Er erfolgt keine Aufzeichnung.')
		else:
			print("Die Aufzeichnung läuft und kann mit ctrl-c beendet werden.")
			datenbank.schreiben('temp','strom',strom)
		time.sleep(aufzeichnungsinterval)
except KeyboardInterrupt:
	meldung = datenbank.exporttemp()
	if meldung == 0:
		print("")
		print("Erstelle die Textdatei der Aufzeichnung.")
		datum = (time.strftime("%Y-%m-%d-%H-%M-%S"))
		sub.call (['cp /tmp/aufzeichnung.txt %s/%s-%s.txt' %(root,Name,datum)], shell=True)
		sub.call (['sudo rm /tmp/aufzeichnung.txt'], shell=True)
		print("")
		print("Die Textdatei %s/%s-%s.txt wurde erstellt." %(root,Name,datum))
	else:
		print("")
		print("Die Outputdatei der Aufzeichnung konnte nicht erstellt werden.")
		sys.exit(0)
	print("")
	print("Versuche die Datenbank Tabelle zu löschen.")
	meldung = datenbank.loeschetemp()
	if meldung == 0:
		print("")	
		print("Die Datenbank Tabelle wurde gelöscht.")
		print("")
	else:
		print("")
		print("Datenbank Tabelle konnte nicht gelöscht weden.")	
		print("")		
except:
	meldung = datenbank.loeschetemp()
	if meldung == 1:
		print("")
		print("Es ist ein Fehler aufgetreten. Die Datenbank Tabelle konnte nicht gelöscht weden.")
		print("")
	else:
		print("")
		print("Es ist ein Fehler aufgetreten. Die Datenbank Tabelle wurde gelöscht.")
		print("")
