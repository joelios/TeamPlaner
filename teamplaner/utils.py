# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def get_user_profile():
	user_profile_name = frappe.db.sql("""SELECT `name` FROM `tabMitglied` WHERE `user_id` = '{user}'""".format(user=frappe.session.user), as_list=True)
	try:
		user_profile = frappe.get_doc("Mitglied", user_profile_name[0][0])
	except:
		user_profile = False
	return user_profile
	
def get_team_img():
	user_profile = get_user_profile()
	if user_profile:
		try:
			team_img = frappe.get_doc("Team", user_profile.team).bild
		except:
			team_img = False
		return team_img
	else:
		return False
		
def get_user_list():
	user = get_user_profile()
	users = frappe.db.sql("""SELECT `vorname`, `nachname`, `position`, `bild`, `nummer` FROM `tabMitglied` WHERE `team` = '{team}' ORDER BY `vorname` ASC""".format(team=user.team), as_dict=True)
	return users
	
def get_staff_img():
	user_profile = get_user_profile()
	if user_profile:
		try:
			staff_img = frappe.get_doc("Team", user_profile.team).staff_bild
		except:
			staff_img = False
		return staff_img
	else:
		return False
		
@frappe.whitelist()
def update_user_in_events():
	events = frappe.db.sql("""SELECT `name` FROM `tabTP Event`""", as_dict=True)
	print("{qty} events".format(qty=len(events)))
	for event in events:
		print("fetch event")
		event = frappe.get_doc("TP Event", event.name)
		for event_user in event.teilnehmer:
			mitglied = frappe.get_doc("Mitglied", event_user.mitglied)
			event_user.user = mitglied.user_id
			event_user.bild = mitglied.bild
			event_user.vorname = mitglied.vorname
			event_user.nachname = mitglied.nachname
		event.save()
		frappe.db.commit()
	print("done")
	return

@frappe.whitelist()
def add_all_user_to_all_events():
	users = frappe.db.sql("""SELECT `name` FROM `tabMitglied`""", as_dict=True)
	print("{qty} user found".format(qty=len(users)))
	for user in users:
		print("check user")
		events = frappe.db.sql("""SELECT `name` FROM `tabTP Event` WHERE `name` NOT IN (
									SELECT `parent` FROM `tabTP Event Teilnehmer` WHERE `mitglied` = '{user}')""".format(user=user.name), as_dict=True)
		for event in events:
			print("update event")
			event = frappe.get_doc("TP Event", event.name)
			row = event.append('teilnehmer', {})
			mitglied = frappe.get_doc("Mitglied", user.name)
			row.mitglied = mitglied.name
			row.status = "Anwesend"
			row.user = mitglied.user_id
			row.bild = mitglied.bild
			row.vorname = mitglied.vorname
			row.nachname = mitglied.nachname
			event.save()
			frappe.db.commit()
	print("done")
	return
