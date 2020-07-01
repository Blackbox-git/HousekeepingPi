#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import der notwendigen Bibliotheken
import time
import json
import datenbank
import zeitdauer
import subprocess as sub
from PyDect200 import PyDect200

# PyDect200 initialisieren
PyDect200 = PyDect200.PyDect200

# AVM Daten importieren
with open('/home/pi/.credentials/avm.json') as creds:    
	credentials = json.load(creds)

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

# Schwellenwerte importieren
try:
	with open('/home/pi/.credentials/schwellenwerte.json') as creds:    
		credentials = json.load(creds)

	AIN1start = credentials['AIN1start']
	if AIN1start == "":
		AIN1start = 3600000	
	AIN1stop = credentials['AIN1stop']
	if AIN1stop == "":
		AIN1stop = 3600000	
	AIN2start = credentials['AIN2start']
	if AIN2start == "":
		AIN2start = 3600000
	AIN2stop = credentials['AIN2stop']
	if AIN2stop == "":
		AIN2stop = 3600000
	AIN3start = credentials['AIN3start']
	if AIN3start == "":
		AIN3start = 3600000
	AIN3stop = credentials['AIN3stop']
	if AIN3stop == "":
		AIN3stop = 3600000
except:
	AIN1start = 3600000
	AIN1stop = 3600000
	AIN2start = 3600000
	AIN2stop = 3600000
	AIN3start = 3600000
	AIN3stop = 3600000
	
# Telegram Daten importieren
with open('/home/pi/.credentials/telegram.json') as creds:    
	credentials = json.load(creds)

Bot1 = credentials['Bot1']
try:
	Bot2 = credentials['Bot2']
except:
	Bot2 = None
try:
	Bot3 = credentials['Bot3']
except:
	Bot3 = None
groupid = credentials['groupid']


# Hilfsvariablen für Gerät 1 deklarieren und initialisieren
AIN1 = AIN1
NameAIN1 = Name1
runningAIN1 = 0
startstromAIN1 = AIN1start 
stopstromAIN1 = AIN1stop
zaehlerAIN1 = 0
statusAIN1 = None
stromAIN1 = None
startzeitAIN1 = None
stopzeitAIN1 = None
dauerAIN1 = None
dauerstringAIN1 = None

# Hilfsvariablen für Gerät 2 deklarieren und initialisieren
AIN2 = AIN2
NameAIN2 = Name2
runningAIN2 = 0
startstromAIN2 = AIN2start
stopstromAIN2 = AIN2stop
zaehlerAIN2 = 0
statusAIN2 = None
stromAIN2 = None
startzeitAIN2 = None
stopzeitAIN2 = None
dauerAIN2 = None
dauerstringAIN2 = None

# Hilfsvariablen für Gerät 3 deklarieren und initialisieren
AIN3 = AIN3
NameAIN3 = Name3
runningAIN3 = 0
startstromAIN3 = AIN3start 
stopstromAIN3 = AIN3stop
zaehlerAIN3 = 0
statusAIN3 = None
stromAIN3 = None
startzeitAIN3 = None
stopzeitAIN3 = None
dauerAIN3 = None
dauerstringAIN3 = None

# Allgemeine Hilfsvariablen anlegen
verbindungsversuch = 0
endzeitzaehler = 3
verbindung = None
aktivegeraete = None

# Funktion zur Ermittlung wieviele Steckdosen überwacht werden sollen
def ermittleaktivegeraete():
	global NameAIN2
	global NameAIN3
	global aktivegeraete
	if NameAIN2 == None:
		aktivegeraete = 1
		return
	if NameAIN3 == None:
		aktivegeraete = 2
		return
	else:
		aktivegeraete = 3
		return

# Funktion Neustart Datenbanklesen
def startdatenbanklesen():
	global runningAIN1
	global runningAIN2
	global runningAIN3
	global startzeitAIN1
	global startzeitAIN2
	global startzeitAIN3
	global aktivegeraete
	if aktivegeraete == 1:
		runningAIN1 = datenbank.lesen("device1","running")	
		if runningAIN1 == None:
			runningAIN1 = 0
		elif runningAIN1 == 0 or runningAIN1 == 2:
			runningAIN1 = 0
		elif runningAIN1 == 1:
			runningAIN1 = 1
			startzeitAIN1 = datenbank.lesen("device1","starttimestamp", 1)
	elif aktivegeraete == 2:
		runningAIN1 = datenbank.lesen("device1","running")	
		if runningAIN1 == None:
			runningAIN1 = 0
		elif runningAIN1 == 0 or runningAIN1 == 2:
			runningAIN1 = 0
		elif runningAIN1 == 1:
			runningAIN1 = 1
			startzeitAIN1 = datenbank.lesen("device1","starttimestamp", 1)
		runningAIN2 = datenbank.lesen("device2","running")	
		if runningAIN2 == None:
			runningAIN2 = 0
		elif runningAIN2 == 0 or runningAIN2 == 2:
			runningAIN2 = 0
		elif runningAIN2 == 1:
			runningAIN2 = 1
			startzeitAIN2 = datenbank.lesen("device2","starttimestamp", 1)
	elif aktivegeraete == 3:
		runningAIN1 = datenbank.lesen("device1","running")	
		if runningAIN1 == None:
			runningAIN1 = 0
		elif runningAIN1 == 0 or runningAIN1 == 2:
			runningAIN1 = 0
		elif runningAIN1 == 1:
			runningAIN1 = 1
			startzeitAIN1 = datenbank.lesen("device1","starttimestamp", 1)
		runningAIN2 = datenbank.lesen("device2","running")	
		if runningAIN2 == None:
			runningAIN2 = 0
		elif runningAIN2 == 0 or runningAIN2 == 2:
			runningAIN2 = 0
		elif runningAIN2 == 1:
			runningAIN2 = 1
			startzeitAIN2 = datenbank.lesen("device2","starttimestamp", 1)
		runningAIN3 = datenbank.lesen("device3","running")	
		if runningAIN3 == None:
			runningAIN3 = 0
		elif runningAIN3 == 0 or runningAIN3 == 2:
			runningAIN3 = 0
		elif runningAIN3 == 1:
			runningAIN3 = 1
			startzeitAIN3 = datenbank.lesen("device3","starttimestamp", 1)

# Funktion um eine Verbindung zur Fritzbox herzustellen
def verbinden():
	global verbindungsversuch
	global verbindung
	while verbindungsversuch == 0:
		try:
			verbindung = PyDect200(fritzboxpasswort,fritzboxbenutzername)
		except:
			print('Fehler aufgetreten. Neuer Versuch.')
			time.sleep(1)
			continue
		if not verbindung.login_ok():
			print('Verbindung nicht okay. Neuer Versuch.')
			time.sleep(1)
			continue
		else:
			test = verbindung.get_device_name(AIN1)
			test = test.encode('ascii', 'ignore')
			if test == "inval":
				time.sleep(1)
				continue
			else:
				print("Verbindung zur FritzBox hergestellt.")
				print("")
				verbindungsversuch = 1
	verbindungsversuch = 0

# Funktion um zu testen ob die Verbindung zur Fritzbox noch besteht
def verbindungstest():
	global AIN1
	global AIN2
	global AIN3
	global verbindung
	global aktivegeraete
	if not verbindung.login_ok():
		verbinden()
		# print("Funktion Verbinden aufrufen, da kein gültiger Login vorliegt.")
		# print("")
	else:
		test = None
		if aktivegeraete == 1:
			test = verbindung.get_device_name(AIN1)
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
		elif aktivegeraete == 2:
			test = verbindung.get_device_name(AIN1)
			if test == "inval" or test == "" or test == None:
				test = verbindung.get_device_name(AIN2)
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
			else:
				# print("")
				# print("Verbindungstest erfolgreich.")
				# print("")
				pass		
		elif aktivegeraete == 3:
			test = verbindung.get_device_name(AIN1)
			if test == "inval" or test == "" or test == None:
				test = verbindung.get_device_name(AIN2)
				if test == "inval" or test == "" or test == None:
					test = verbindung.get_device_name(AIN3)
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
				else:
					# print("")
					# print("Verbindungstest erfolgreich.")
					# print("")
					pass	
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


# Hauptprogramm	
ermittleaktivegeraete()
startdatenbanklesen()	
verbinden()
while True:
	verbindungstest()
	
	if aktivegeraete >= 1:
		statusAIN1 = ermittlestatus(AIN1)
		stromAIN1 = ermittlestrom(AIN1)
		datenbankfehlerAIN1 = datenbank.lesen('failure','device1')
		if statusAIN1 == "NULL" or stromAIN1 == "NULL":
			runningAIN1 = 0
			datenbankrunningAIN1 = datenbank.lesen('device1','running')
			if datenbankrunningAIN1 == 1:
				datenbank.update("device1",'running',2,"endtimestamp","CURRENT_TIMESTAMP")
			if datenbankfehlerAIN1 == 0:
				datenbank.update('failure','device1',1)
				try:
					text = 'Es ist ein Fehler aufgetreten. Die Steckdose ist nicht mehr erreichbar. Das Programn wurde zurückgesetzt.'
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot1,groupid,text)], shell=True)
				except:
					continue
			print("Es ist ein Fehler aufgetreten. Die Steckdose '%s' ist nicht mehr erreichbar. Das Programn wurde zurückgesetzt." %(NameAIN1))
			print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN1,statusAIN1))
			print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN1,stromAIN1))
			print("")
		elif statusAIN1 == 0 and runningAIN1 == 0:
			if datenbankfehlerAIN1 == 1:
				datenbank.update('failure','device1',0)
				try:
					text = 'Der Fehler ist behoben. Die Steckdose ist wieder erreichbar.'
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot1,groupid,text)], shell=True)
				except:
					continue					
			print("Die Steckdose '%s' ist ausgeschaltet. Es kann kein Vorgang gestartet werden." %(NameAIN1))
			print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN1,statusAIN1))
			print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN1,stromAIN1))
			print("")		
		elif runningAIN1 == 0:
			if datenbankfehlerAIN1 == 1:
				datenbank.update('failure','device1',0)
				try:
					text = 'Der Fehler ist behoben. Die Steckdose ist wieder erreichbar.'
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot1,groupid,text)], shell=True)
				except:
					continue				
			if statusAIN1 == 1 and stromAIN1 > startstromAIN1:
				now = time.strftime("%d.%m.%Y um %H:%M")
				startzeitAIN1 = time.time()
				try:
					text = "Das Gerät %s wurde am %s gestartet." %(NameAIN1,now)
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot1,groupid,text)], shell=True)
				except:
					print("Ehrenrunde '%s'" &(NameAIN1))
					continue
				print("Das Gerät '%s' wurde am %s gestartet." %(NameAIN1,now))
				print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN1,statusAIN1))
				print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN1,stromAIN1))
				print("")
				runningAIN1 = 1
				datenbank.schreiben('device1','running',1,'starttimestamp','CURRENT_TIMESTAMP')				
			else:
				print("Das Programm wartet bis ein Vorgang von '%s' durchgeführt wird." %(NameAIN1))
				print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN1,statusAIN1))
				print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN1,stromAIN1))
				print("")
		elif runningAIN1 == 1:
			if datenbankfehlerAIN1 == 1:
				datenbank.update('failure','device1',0)
				try:
					text = 'Der Fehler ist behoben. Die Steckdose ist wieder erreichbar.'
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot1,groupid,text)], shell=True)
				except:
					continue	
			if statusAIN1 == 0:
				zaehlerAIN1 = 0
				runningAIN1 = 0
				datenbank.update('device1',"running",2,"endtimestamp","CURRENT_TIMESTAMP")
				now = time.strftime("%d.%m.%Y um %H:%M")
				try:
					text = "Die Steckdose wurde ausgeschaltet. Bitte prüfen."
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot1,groupid,text)], shell=True)
				except:
					print("Ehrenrunde '%s'" &(NameAIN1))
					continue
				print("Die Steckdose wurde ausgeschaltet.Bitte prüfen.")
				print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN1,statusAIN1))
				print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN1,stromAIN1))
				print("")
			elif stromAIN1 < stopstromAIN1:
				if zaehlerAIN1 < endzeitzaehler:
					zaehlerAIN1 = zaehlerAIN1 + 1
					print("Aktueller Endzeitzählerstand von '%s': %s" %(NameAIN1,zaehlerAIN1))
					print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN1,statusAIN1))
					print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN1,stromAIN1))
					print("")
				if zaehlerAIN1 == endzeitzaehler:
					now = time.strftime("%d.%m.%Y um %H:%M")
					stopzeitAIN1 = time.time()
					dauerAIN1 = stopzeitAIN1 - startzeitAIN1
					dauerAIN1 = int(dauerAIN1)
					dauerstringAIN1 = zeitdauer.ermittlerzeitdauer(dauerAIN1)
					try:
						text = "Das Gerät '%s' ist seit %s fertig. Die Vorgangsdauer betrug %s." %(NameAIN1,now,dauerstringAIN1)
						sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot1,groupid,text)], shell=True)
					except:
						print("Ehrenrunde '%s'" &(NameAIN1))
						continue
					print("Das Gerät '%s' ist seit %s fertig. Die Vorgangsdauer betrug %s." %(NameAIN1,now,dauerstringAIN1))
					print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN1,statusAIN1))
					print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN1,stromAIN1))
					print("")
					zaehlerAIN1 = 0
					runningAIN1 = 0
					datenbank.update('device1',"running",2,"endtimestamp","CURRENT_TIMESTAMP")
			else:
				print("Das Gerät '%s' läuft." %(NameAIN1))
				print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN1,statusAIN1))
				print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN1,stromAIN1))
				print("")
				zaehlerAIN1 = 0


	if aktivegeraete >= 2:
		statusAIN2 = ermittlestatus(AIN2)
		stromAIN2 = ermittlestrom(AIN2)
		datenbankfehlerAIN2 = datenbank.lesen('failure','device2')
		if statusAIN2 == "NULL" or stromAIN2 == "NULL":
			runningAIN2 = 0
			datenbankrunningAIN2 = datenbank.lesen('device2','running')
			if datenbankrunningAIN2 == 1:
				datenbank.update("device2",'running',2,"endtimestamp","CURRENT_TIMESTAMP")
			if datenbankfehlerAIN2 == 0:
				datenbank.update('failure','device2',1)
				try:
					text = 'Es ist ein Fehler aufgetreten. Die Steckdose ist nicht mehr erreichbar. Das Programn wurde zurückgesetzt.'
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot2,groupid,text)], shell=True)
				except:
					continue
			print("Es ist ein Fehler aufgetreten. Die Steckdose '%s' ist nicht mehr erreichbar. Das Programn wurde zurückgesetzt." %(NameAIN2))
			print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN2,statusAIN2))
			print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN2,stromAIN2))
			print("")
		elif statusAIN2 == 0 and runningAIN2 == 0:
			if datenbankfehlerAIN2 == 1:
				datenbank.update('failure','device2',0)
				try:
					text = 'Der Fehler ist behoben. Die Steckdose ist wieder erreichbar.'
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot2,groupid,text)], shell=True)
				except:
					continue					
			print("Die Steckdose '%s' ist ausgeschaltet. Es kann kein Vorgang gestartet werden." %(NameAIN2))
			print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN2,statusAIN2))
			print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN2,stromAIN2))
			print("")
		elif runningAIN2 == 0:
			if datenbankfehlerAIN2 == 1:
				datenbank.update('failure','device2',0)
				try:
					text = 'Der Fehler ist behoben. Die Steckdose ist wieder erreichbar.'
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot2,groupid,text)], shell=True)
				except:
					continue				
			if statusAIN2 == 1 and stromAIN2 > startstromAIN2:
				now = time.strftime("%d.%m.%Y um %H:%M")
				startzeitAIN2 = time.time()
				try:
					text = "Das Gerät %s wurde am %s gestartet." %(NameAIN2,now)
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot2,groupid,text)], shell=True)
				except:
					print("Ehrenrunde '%s'" &(NameAIN2))
					continue
				print("Das Gerät '%s' wurde am %s gestartet." %(NameAIN2,now))
				print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN2,statusAIN2))
				print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN2,stromAIN2))
				print("")
				runningAIN2 = 1
				datenbank.schreiben('device2','running',1,'starttimestamp','CURRENT_TIMESTAMP')				
			else:
				print("Das Programm wartet bis ein Vorgang von '%s' durchgeführt wird." %(NameAIN2))
				print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN2,statusAIN2))
				print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN2,stromAIN2))
				print("")
		elif runningAIN2 == 1:
			if datenbankfehlerAIN2 == 1:
				datenbank.update('failure','device2',0)
				try:
					text = 'Der Fehler ist behoben. Die Steckdose ist wieder erreichbar.'
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot2,groupid,text)], shell=True)
				except:
					continue	
			if statusAIN2 == 0:
				zaehlerAIN2 = 0
				runningAIN2 = 0
				datenbank.update('device2',"running",2,"endtimestamp","CURRENT_TIMESTAMP")
				now = time.strftime("%d.%m.%Y um %H:%M")
				try:
					text = "Die Steckdose wurde ausgeschaltet. Bitte prüfen."
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot2,groupid,text)], shell=True)
				except:
					print("Ehrenrunde '%s'" &(NameAIN2))
					continue
				print("Die Steckdose wurde ausgeschaltet.Bitte prüfen.")
				print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN2,statusAIN2))
				print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN2,stromAIN2))
				print("")
			elif stromAIN2 < stopstromAIN2:
				if zaehlerAIN2 < endzeitzaehler:
					zaehlerAIN2 = zaehlerAIN2 + 1
					print("Aktueller Endzeitzählerstand von '%s': %s" %(NameAIN2,zaehlerAIN2))
					print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN2,statusAIN2))
					print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN2,stromAIN2))
					print("")
				if zaehlerAIN2 == endzeitzaehler:
					now = time.strftime("%d.%m.%Y um %H:%M")
					stopzeitAIN2 = time.time()
					dauerAIN2 = stopzeitAIN2 - startzeitAIN2
					dauerAIN2 = int(dauerAIN2)
					dauerstringAIN2 = zeitdauer.ermittlerzeitdauer(dauerAIN2)
					try:
						text = "Das Gerät '%s' ist seit %s fertig. Die Vorgangsdauer betrug %s." %(NameAIN2,now,dauerstringAIN2)
						sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot2,groupid,text)], shell=True)
					except:
						print("Ehrenrunde '%s'" &(NameAIN2))
						continue
					print("Das Gerät '%s' ist seit %s fertig. Die Vorgangsdauer betrug %s." %(NameAIN2,now,dauerstringAIN2))
					print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN2,statusAIN2))
					print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN2,stromAIN2))
					print("")
					zaehlerAIN2 = 0
					runningAIN2 = 0
					datenbank.update('device2',"running",2,"endtimestamp","CURRENT_TIMESTAMP")
			else:
				print("Das Gerät '%s' läuft." %(NameAIN2))
				print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN2,statusAIN2))
				print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN2,stromAIN2))
				print("")
				zaehlerAIN2 = 0


	if aktivegeraete == 3:
		statusAIN3 = ermittlestatus(AIN3)
		stromAIN3 = ermittlestrom(AIN3)
		datenbankfehlerAIN3 = datenbank.lesen('failure','device3')
		if statusAIN3 == "NULL" or stromAIN3 == "NULL":
			runningAIN3 = 0
			datenbankrunningAIN3 = datenbank.lesen('device3','running')
			if datenbankrunningAIN3 == 1:
				datenbank.update("device3",'running',2,"endtimestamp","CURRENT_TIMESTAMP")
			if datenbankfehlerAIN3 == 0:
				datenbank.update('failure','device3',1)
				try:
					text = 'Es ist ein Fehler aufgetreten. Die Steckdose ist nicht mehr erreichbar. Das Programn wurde zurückgesetzt.'
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot3,groupid,text)], shell=True)
				except:
					continue
			print("Es ist ein Fehler aufgetreten. Die Steckdose '%s' ist nicht mehr erreichbar. Das Programn wurde zurückgesetzt." %(NameAIN3))
			print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN3,statusAIN3))
			print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN3,stromAIN3))
			print("")
		elif statusAIN3 == 0 and runningAIN3 == 0:
			if datenbankfehlerAIN3 == 1:
				datenbank.update('failure','device3',0)
				try:
					text = 'Der Fehler ist behoben. Die Steckdose ist wieder erreichbar.'
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot3,groupid,text)], shell=True)
				except:
					continue					
			print("Die Steckdose '%s' ist ausgeschaltet. Es kann kein Vorgang gestartet werden." %(NameAIN3))
			print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN3,statusAIN3))
			print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN3,stromAIN3))
			print("")
		elif runningAIN3 == 0:
			if datenbankfehlerAIN3 == 1:
				datenbank.update('failure','device3',0)
				try:
					text = 'Der Fehler ist behoben. Die Steckdose ist wieder erreichbar.'
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot3,groupid,text)], shell=True)
				except:
					continue				
			if statusAIN3 == 1 and stromAIN3 > startstromAIN3:
				now = time.strftime("%d.%m.%Y um %H:%M")
				startzeitAIN3 = time.time()
				try:
					text = "Das Gerät %s wurde am %s gestartet." %(NameAIN3,now)
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot3,groupid,text)], shell=True)
				except:
					print("Ehrenrunde '%s'" &(NameAIN3))
					continue
				print("Das Gerät '%s' wurde am %s gestartet." %(NameAIN3,now))
				print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN3,statusAIN3))
				print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN3,stromAIN3))
				print("")
				runningAIN3 = 1
				datenbank.schreiben('device3','running',1,'starttimestamp','CURRENT_TIMESTAMP')				
			else:
				print("Das Programm wartet bis ein Vorgang von '%s' durchgeführt wird." %(NameAIN3))
				print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN3,statusAIN3))
				print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN3,stromAIN3))
				print("")
		elif runningAIN3 == 1:
			if datenbankfehlerAIN3 == 1:
				datenbank.update('failure','device3',0)
				try:
					text = 'Der Fehler ist behoben. Die Steckdose ist wieder erreichbar.'
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot3,groupid,text)], shell=True)
				except:
					continue	
			if statusAIN3 == 0:
				zaehlerAIN3 = 0
				runningAIN3 = 0
				datenbank.update('device3',"running",2,"endtimestamp","CURRENT_TIMESTAMP")
				now = time.strftime("%d.%m.%Y um %H:%M")
				try:
					text = "Die Steckdose wurde ausgeschaltet. Bitte prüfen."
					sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot3,groupid,text)], shell=True)
				except:
					print("Ehrenrunde '%s'" &(NameAIN3))
					continue
				print("Die Steckdose wurde ausgeschaltet.Bitte prüfen.")
				print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN3,statusAIN3))
				print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN3,stromAIN3))
				print("")
			elif stromAIN3 < stopstromAIN3:
				if zaehlerAIN3 < endzeitzaehler:
					zaehlerAIN3 = zaehlerAIN3 + 1
					print("Aktueller Endzeitzählerstand von '%s': %s" %(NameAIN3,zaehlerAIN3))
					print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN3,statusAIN3))
					print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN3,stromAIN3))
					print("")
				if zaehlerAIN3 == endzeitzaehler:
					now = time.strftime("%d.%m.%Y um %H:%M")
					stopzeitAIN3 = time.time()
					dauerAIN3 = stopzeitAIN3 - startzeitAIN3
					dauerAIN3 = int(dauerAIN3)
					dauerstringAIN3 = zeitdauer.ermittlerzeitdauer(dauerAIN3)
					try:
						text = "Das Gerät '%s' ist seit %s fertig. Die Vorgangsdauer betrug %s." %(NameAIN3,now,dauerstringAIN3)
						sub.call (["curl -X  POST 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s=&text=%s'" %(Bot3,groupid,text)], shell=True)
					except:
						print("Ehrenrunde '%s'" &(NameAIN3))
						continue
					print("Das Gerät '%s' ist seit %s fertig. Die Vorgangsdauer betrug %s." %(NameAIN3,now,dauerstringAIN3))
					print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN3,statusAIN3))
					print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN3,stromAIN3))
					print("")
					zaehlerAIN3 = 0
					runningAIN3 = 0
					datenbank.update('device3',"running",2,"endtimestamp","CURRENT_TIMESTAMP")
			else:
				print("Das Gerät '%s' läuft." %(NameAIN3))
				print("Der aktuelle Status der Steckdose '%s': %s" %(NameAIN3,statusAIN3))
				print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(NameAIN3,stromAIN3))
				print("")
				zaehlerAIN3 = 0	
	print("")
	time.sleep(20)