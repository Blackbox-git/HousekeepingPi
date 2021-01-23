#!/usr/bin/python3

# Import der notwendigen Bibliotheken
import time
import json
import datenbank
import zeitdauer
import subprocess as sub
import PyDect200

# PyDect200 initialisieren
p = PyDect200.PyDect200

# AVM Daten importieren
with open('./settings/settings.json') as content:    
	settings = json.load(content)

fritzboxbenutzername = settings['fritz']['user']
fritzboxpasswort = settings['fritz']['password']

# Telegram Daten
try:
	Bot = settings['telegram']['bot']
	groupid = settings['telegram']['groupid']
except:
	print("No Telegramm bot configured")
	Bot = None
	groupid = None
	exit(1)

# Allgemeine Hilfsvariablen anlegen
verbindungsversuch = 0
endzeitzaehler = 3
verbindung = None

# Funktion om Telegram Nachricht zu versenden
def sendMessage(Bot, Groupid, Name, Text):
	parse_mode = "HTML" #MarkdownV2
	now = time.strftime("%H:%M")
	message = """<u><b>%s %s</b></u>:
%s""" %(now, Name, Text)

	uri = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&parse_mode=%s" %(Bot, Groupid, parse_mode)    
	print("%s \n%s" %(uri, message))
	try:
		sub.call (["curl --data 'text=%s' -X POST '%s'" %(message, uri)], shell=True)
	except:
		print("Error sending message:\n%s" %(message))

# Funktion um eine Verbindung zur Fritzbox herzustellen
def verbinden(AIN):
	global verbindungsversuch
	global verbindung
	while verbindungsversuch == 0:
		try:
			verbindung = p(fritzboxpasswort,fritzboxbenutzername)
		except:
			print('Failed to connect to fritzbox')
			time.sleep(5)
			continue
		if not verbindung.login_ok():
			print('Failed to connect to fritzbox. Next try.')
			time.sleep(5)
			continue
		else:
			test = verbindung.get_device_name(AIN)
			test = test.encode('ascii', 'ignore')
			if test == "inval":
				time.sleep(5)
				continue
			else:
				print("Verbindung zur FritzBox hergestellt.")
				print("")
				verbindungsversuch = 1
	verbindungsversuch = 0

# Funktion um zu testen ob die Verbindung zur Fritzbox noch besteht
def verbindungstest(AIN):
	global verbindung
	if not verbindung.login_ok():
		verbinden(AIN)
		print("Call function verbinden\n")
	else:
		test = None
		test = verbindung.get_device_name(AIN)
		if test == "inval" or test == "" or test == None:
			verbinden(AIN)
			print("Funktion Verbinden aufgerufen, da die Fritzbox nicht mehr erreichbar ist.")
		else:
			print("Verbindungstest erfolgreich.")
			pass
				
# Funktion zum ermitteln des aktuellen Schaltstatus
def ermittlestatus(device):
	status = "NULL"
	cb = 0
	while status == "NULL":
		status = verbindung.get_state(device)
		status = status.encode('ascii', 'ignore')
		if status == "inval" or status == "":
			status = "NULL"
		elif status == "0":
			return 0
		else:
			try:
				status = int(status)
				return status
			except:
				status = "NULL"

		cb += 1
		if cb > 10:
			return "NULL"
		else:
			time.sleep(60)

# Funktion zum ermitteln des aktuellen Verbrauches in Milliwatt
def ermittlestrom(device):
	strom = "NULL"
	cb = 0
	while strom == "NULL":
		strom = verbindung.get_power_single(device)
		strom = strom.encode('ascii', 'ignore')
		if strom == "inval" or strom == "":
			strom = "NULL"
		elif strom == "0":
			return 0
		else:
			try:
				strom = int(strom)
				return strom
			except:
				strom = "NULL"

		cb += 1
		if cb > 10:
			return "NULL"
		else:
			time.sleep(60)
	
# Funktion zum ermitteln der aktuellen Temperatur
def ermittletemp(device):
	try:
		temp = verbindung.get_temperature_single(device)
		return temp
	except:
		return -99

def startdatenbanklesen(device):
	datenbank.CreateTables(("dev_%s" %(device['AIN'])))
	device['runningAIN'] = datenbank.lesen(("dev_%s" %(device['AIN'])), "running")	
	if device['runningAIN'] == None:
		device['runningAIN'] = 0
	elif device['runningAIN'] == 0 or device['runningAIN'] == 2:
		device['runningAIN'] = 0
	elif device['runningAIN'] == 1:
		device['runningAIN'] = 1
		device['startzeitAIN'] = datenbank.lesen(("dev_%s" %(device['AIN'])), "starttimestamp", 1)

# Hauptprogramm	
for device in settings['devices']:
	startdatenbanklesen(device)
	verbinden(device['AIN'])

sendMessage(Bot, groupid, "Service", "Service gestartet")
try:
	while True:
		for device in settings['devices']:
			verbindungstest(device['AIN'])
			now = time.strftime("%H:%M")
			device['statusAIN'] = ermittlestatus(device['AIN'])
			device['stromAIN'] = ermittlestrom(device['AIN'])
			temp = ermittletemp(device['AIN'])
			if temp < 4:
				text = "<i><b>Temperaturwarnung:</b></i> %s Grad Celcius" %(temp)
				sendMessage(Bot, groupid, "Raum", text)

			device['datenbankfehlerAIN'] = datenbank.lesen('failure', ("dev_%s" %(device['AIN'])))
			if device['statusAIN'] == "NULL" or device['stromAIN'] == "NULL":
				device['runningAIN'] = 0
				datenbankrunningAIN = datenbank.lesen(("dev_%s" %(device['AIN'])), 'running')
				if datenbankrunningAIN == 1:
					datenbank.update(("dev_%s" %(device['AIN'])), 'running', 2, "endtimestamp", "CURRENT_TIMESTAMP")

				if device['datenbankfehlerAIN'] == 0:
					datenbank.update('failure', ("dev_%s" %(device['AIN'])), 1)
					text = 'Es ist ein Fehler aufgetreten. Die Steckdose ist nicht mehr erreichbar. Das Programn wurde reinitialisiert'
					sendMessage(Bot, groupid, device['Name'], text)

				print("Es ist ein Fehler aufgetreten. Die Steckdose '%s' ist nicht mehr erreichbar. Das Programn wurde zuruckgesetzt." %(device['Name']))
				print("Der aktuelle Status der Steckdose '%s': %s" %(device['Name'], device['statusAIN']))
				print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(device['Name'], device['stromAIN']))
			elif device['statusAIN'] == 0 and device['runningAIN'] == 0:
				if device['datenbankfehlerAIN'] == 1:
					datenbank.update('failure', ("dev_%s" %(device['AIN'])), 0)
					text = 'Der Fehler ist behoben. Die Steckdose ist wieder erreichbar'
					sendMessage(Bot, groupid, device['Name'], text)

				print("Die Steckdose '%s' ist ausgeschaltet. Es kann kein Vorgang gestartet werden." %(device['Name']))
				print("Der aktuelle Status der Steckdose '%s': %s" %(device['Name'], device['statusAIN']))
				print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(device['Name'], device['stromAIN']))		
			elif device['runningAIN'] == 0:
				if device['datenbankfehlerAIN'] == 1:
					datenbank.update('failure', ("dev_%s" %(device['AIN'])), 0)
					text = 'Der Fehler ist behoben. Die Steckdose ist wieder erreichbar'
					sendMessage(Bot, groupid, device['Name'], text)

				if device['statusAIN'] == 1 and device['stromAIN'] > device['ThresholdStart']:
					device['startzeitAIN'] = time.time()
					sendMessage(Bot, groupid, device['Name'], "Wurde gestartet")
					print("'%s' wurde um %s gestartet." %(device['Name'], now))
					print("Der aktuelle Status der Steckdose '%s': %s" %(device['Name'], device['statusAIN']))
					print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(device['Name'], device['stromAIN']))
					device['runningAIN'] = 1
					datenbank.schreiben(("dev_%s" %(device['AIN'])),'running',1,'starttimestamp','CURRENT_TIMESTAMP')				
				else:
					print("Das Programm wartet bis ein Vorgang von '%s' gemacht wird." %(device['Name']))
					print("Der aktuelle Status der Steckdose '%s': %s" %(device['Name'], device['statusAIN']))
					print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(device['Name'], device['stromAIN']))
			elif device['runningAIN'] == 1:
				if device['datenbankfehlerAIN'] == 1:
					datenbank.update('failure', ("dev_%s" %(device['AIN'])), 0)
					text = 'Der Fehler ist behoben. Die Steckdose ist wieder erreichbar'
					sendMessage(Bot, groupid, device['Name'], text)

				if device['statusAIN'] == 0:
					device['zaehlerAIN'] = 0
					device['runningAIN'] = 0
					datenbank.update(("dev_%s" %(device['AIN'])), "running", 2, "endtimestamp", "CURRENT_TIMESTAMP")
					text = "Die Steckdose wurde ausgeschaltet."
					sendMessage(Bot, groupid, device['Name'], text)
					print("Die Steckdose wurde ausgeschaltet.")
					print("Der aktuelle Status der Steckdose '%s': %s" %(device['Name'], device['statusAIN']))
					print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(device['Name'], device['stromAIN']))
				elif device['stromAIN'] < device['ThresholdStop']:
					if device['zaehlerAIN'] < endzeitzaehler:
						device['zaehlerAIN'] = device['zaehlerAIN'] + 1
						print("Aktueller Endzeitzaehlerstand von '%s': %s" %(device['Name'], device['zaehlerAIN']))
						print("Der aktuelle Status der Steckdose '%s': %s" %(device['Name'], device['statusAIN']))
						print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(device['Name'], device['stromAIN']))

					if device['zaehlerAIN'] == endzeitzaehler:
						stopzeitAIN = time.time()
						dauerAIN = stopzeitAIN - device['startzeitAIN']
						dauerAIN = int(dauerAIN)
						dauerstringAIN = zeitdauer.ermittlerzeitdauer(dauerAIN)
						text = "Ist fertig. Die Vorgangsdauer betrug %s" %(dauerstringAIN)
						sendMessage(Bot, groupid, device['Name'], text)
						print("'%s' ist seit %s fertig. Die Vorgangsdauer betrug %s." %(device['Name'], now, dauerstringAIN))
						print("Der aktuelle Status der Steckdose '%s': %s" %(device['Name'], device['statusAIN']))
						print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(device['Name'], device['stromAIN']))
						device['zaehlerAIN'] = 0
						device['runningAIN'] = 0
						datenbank.update(("dev_%s" %(device['AIN'])), "running", 2, "endtimestamp", "CURRENT_TIMESTAMP")
				else:
					print("'%s' ist am laufen." %(device['Name']))
					print("Der aktuelle Status der Steckdose '%s': %s" %(device['Name'], device['statusAIN']))
					print("Der aktuelle Stromverbrauch der Steckdose '%s': %s" %(device['Name'], device['stromAIN']))
					device['zaehlerAIN'] = 0
		
		time.sleep(60)

finally:
	print("Service will be stoped")
	sendMessage(Bot, groupid, "Service", "Service wird gestoppt")
