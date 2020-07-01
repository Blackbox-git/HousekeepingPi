#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import der notwendigen Bibliotheken
import os
import sys
import json
import subprocess as sub

# Prüfen ob Programm bereits installiert wurde
if not os.path.isfile('/home/pi/.credentials/schwellenwerte.json'):
	print("")
	print("Programm abgebrochen. Bitte installieren Sie das Projekt zuerst.")
	print("")
	sys.exit(0)
	
# Zugangsdaten AVM importieren
with open('/home/pi/.credentials/avm.json') as creds:    
	credentials = json.load(creds)

# Setzen der AVM Daten
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

# Hilfsvariablen anlegen
AIN1start = ""
AIN1stop = ""
AIN2start = ""
AIN2stop = ""
AIN3start = ""
AIN3stop = ""

# Leerzeile ausgeben
print("")
print("WILLKOMMEN ZUM EINTRAGEN DER SCHWELLENWERTE")
print("")
# Anbfrage der Start-Schwellenwert Geräte 1
while True:
	try:
		AIN1start = input("Bitte geben Sie den START-Schwellenwert von '%s' in Milliwatt (mW) ein: " %(Name1))
		try:
			AIN1start = int(AIN1start)
			print("")
			break
		except: 
			print("Fehler bei der Eingabe. Es sind nur Zahlen erlaubt.")
			print("")
			continue
	except:
		print("")
		print("")
		print("Das Programm wurde beendet. Keine Schwellenwerte eingetragen.")
		print("")
		sys.exit(0)		
		
# Anbfrage der Stop-Schwellenwert Geräte 1
while True:
	try:
		AIN1stop = input("Bitte geben Sie den STOPP-Schwellenwert von '%s' in Milliwatt (mW) ein: " %(Name1))
		try:
			AIN1stop = int(AIN1stop)
			print("")
			break
		except: 
			print("Fehler bei der Eingabe. Es sind nur Zahlen erlaubt.")
			print("")
			continue
	except:
		print("")
		print("")
		print("Das Programm wurde beendet. Keine Schwellenwerte eingetragen.")
		print("")
		sys.exit(0)	
		
# Anbfrage der Start-Schwellenwert Geräte 2 (wenn vorhanden)
if AIN2 != None:
	while True:
		try:
			AIN2start = input("Bitte geben Sie den START-Schwellenwert von '%s' in Milliwatt (mW) ein: " %(Name2))
			try:
				AIN2start = int(AIN2start)
				print("")
				break
			except: 
				print("Fehler bei der Eingabe. Es sind nur Zahlen erlaubt.")
				print("")
				continue
		except:
			print("")
			print("")
			print("Das Programm wurde beendet. Keine Schwellenwerte eingetragen.")
			print("")
			sys.exit(0)		
		
	# Anbfrage der Stop-Schwellenwert Geräte 1
	while True:
		try:
			AIN2stop = input("Bitte geben Sie den STOPP-Schwellenwert von '%s' in Milliwatt (mW) ein: " %(Name2))
			try:
				AIN2stop = int(AIN2stop)
				print("")
				break
			except: 
				print("Fehler bei der Eingabe. Es sind nur Zahlen erlaubt.")
				print("")
				continue
		except:
			print("")
			print("")
			print("Das Programm wurde beendet. Keine Schwellenwerte eingetragen.")
			print("")
			sys.exit(0)	

# Anbfrage der Start-Schwellenwert Geräte 3 (wenn vorhanden)
if AIN3 != None:
	while True:
		try:
			AIN3start = input("Bitte geben Sie den START-Schwellenwert von '%s' in Milliwatt (mW) ein: " %(Name3))
			try:
				AIN3start = int(AIN3start)
				print("")
				break
			except: 
				print("Fehler bei der Eingabe. Es sind nur Zahlen erlaubt.")
				print("")
				continue
		except:
			print("")
			print("")
			print("Das Programm wurde beendet. Keine Schwellenwerte eingetragen.")
			print("")
			sys.exit(0)	
			
	# Anbfrage der Stop-Schwellenwert Geräte 1
	while True:
		try:
			AIN3stop = input("Bitte geben Sie den STOPP-Schwellenwert von '%s' in Milliwatt (mW) ein: " %(Name3))
			try:
				AIN3stop = int(AIN3stop)
				print("")
				break
			except: 
				print("Fehler bei der Eingabe. Es sind nur Zahlen erlaubt.")
				print("")
				continue
		except:
			print("")
			print("")
			print("Das Programm wurde beendet. Keine Schwellenwerte eingetragen.")
			print("")
			sys.exit(0)	

# Eintragung der Schwellenwerte
with open('/home/pi/.credentials/schwellenwerte.json') as schwell:    
	schwellenwerte = json.load(schwell)

schwellenwerte["AIN1start"] = AIN1start
schwellenwerte["AIN1stop"] = AIN1stop
schwellenwerte["AIN2start"] = AIN2start
schwellenwerte["AIN2stop"] = AIN2stop
schwellenwerte["AIN3start"] = AIN3start
schwellenwerte["AIN3stop"] = AIN3stop

with open('/home/pi/.credentials/schwellenwerte.json', "w") as schwell:
	json.dump(schwellenwerte, schwell, indent=0)
print("")
print("Die neuen Schwellenwerte wurden eingetragen.")
print("")
print("")

# Anbfrage der Neustart des Dienstes
while True:
	try:
		reboot = input("Neustart des Dienstes haushalt.service notwendig. Soll dieser durchgeführt werden? (y/n): ")
		if reboot == 'y':
			sub.call (['sudo systemctl restart haushalt.service'], shell=True)
			print("")
			print("")
			print("Das Programm wurde beendet. Der Neustart des Dienstes haushalt.service wurde durchgeführt.")
			print("")		
			break
		elif reboot == 'n': 
			print("")
			print("")
			print("Das Programm wurde beendet. Es wird kein Neustart des Dienstes haushalt.service durchgeführt.")
			print("")
			break
		else:
			print("Fehler bei der Eingabe. Es ist nur 'y' oder 'n' erlaubt.")
			print("")
			continue
	except:
		print("")
		print("")
		print("Das Programm wurde beendet. Kein Neustart durchgeführt.")
		print("")
		sys.exit(0)		