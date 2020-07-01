#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import der notwendigen Bibliotheken
import time

# Funktion zum berechnen der Zeitdauer
def ermittlerzeitdauer(seconds):
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	if days == 0:
		if hours == 0:
			zeitdauer = "%s Minuten" %minutes
		elif hours == 1 and minutes == 0:
			zeitdauer = "1 Stunde"
		elif hours != 1 and minutes == 0:
			zeitdauer = "%s Stunden" %hours
		elif hours == 1 and minutes == 1:
			zeitdauer = "1 Stunde und 1 Minute"
		elif hours == 1 and minutes != 1:
			zeitdauer = "1 Stunde und %s Minuten" %minutes
		elif hours != 1 and minutes == 1:
			zeitdauer = "%s Stunden und 1 Minute" %hours
		else:
			zeitdauer = "%s Stunden und %s Minuten" %(hours,minutes)	
	else:
		if days == 1:
			if hours == 0 and minutes == 0:
				zeitdauer = "1 Tag"
			elif hours == 0:
				zeitdauer = "1 Tag und %s Minuten" %minutes
			elif hours == 1 and minutes == 0:
				zeitdauer = "1 Tag und 1 Stunde"
			elif hours != 1 and minutes == 0:
				zeitdauer = "1 Tag und %s Stunden" %hours
			elif hours == 1 and minutes == 1:
				zeitdauer = "1 Tag, 1 Stunde und 1 Minute"
			elif hours == 1 and minutes != 1:
				zeitdauer = "1 Tag, 1 Stunde und %s Minuten" %minutes
			elif hours != 1 and minutes == 1:
				zeitdauer = "1 Tag, %s Stunden und 1 Minute" %hours
			else:
				zeitdauer = "1 Tag, %s Stunden und %s Minuten" %(hours,minutes)
		else:
			if hours == 0 and minutes == 0:
				zeitdauer = "%s Tage" %days
			if hours == 0:
				zeitdauer = "%s Tage und %s Minuten" %(days,minutes)
			elif hours == 1 and minutes == 0:
				zeitdauer = "%s Tage und 1 Stunde" %days
			elif hours != 1 and minutes == 0:
				zeitdauer = "%s Tage und %s Stunden" %(days,hours)
			elif hours == 1 and minutes == 1:
				zeitdauer = "%s Tage, 1 Stunde und 1 Minute" %days
			elif hours == 1 and minutes != 1:
				zeitdauer = "%s Tage, 1 Stunde und %s Minuten" %(days,minutes)
			elif hours != 1 and minutes == 1:
				zeitdauer = "%s Tage, %s Stunden und 1 Minute" %(days,hours)
			else:
				zeitdauer = "%s Tage, %s Stunden und %s Minuten" %(days,hours,minutes)		
	return zeitdauer