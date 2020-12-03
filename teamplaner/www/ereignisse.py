# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

no_cache = 1

def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
		
	context['events'] = []
	all_events = frappe.db.sql("""SELECT `name` FROM `tabTP Event` ORDER BY `event_date` ASC""", as_list=True)
	for event in all_events:
		context['events'].append(frappe.get_doc("TP Event", event[0]))
	return context
	
@frappe.whitelist()
def anmelden(event_name):
	frappe.db.sql("""UPDATE `tabTP Event Teilnehmer` SET `status` = 'Anwesend' WHERE `parent` = '{event_name}' AND `user` = '{user}'""".format(event_name=event_name, user=frappe.session.user), as_list=True)
	return 'ok'

@frappe.whitelist()
def abmelden(event_name):
	frappe.db.sql("""UPDATE `tabTP Event Teilnehmer` SET `status` = 'Abwesend' WHERE `parent` = '{event_name}' AND `user` = '{user}'""".format(event_name=event_name, user=frappe.session.user), as_list=True)
	return 'ok'

@frappe.whitelist()
def komme_zu_spaet(event_name):
	frappe.db.sql("""UPDATE `tabTP Event Teilnehmer` SET `status` = 'Verspätet' WHERE `parent` = '{event_name}' AND `user` = '{user}'""".format(event_name=event_name, user=frappe.session.user), as_list=True)
	return 'ok'