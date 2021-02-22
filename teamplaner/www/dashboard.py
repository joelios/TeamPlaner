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
	context['next_event'] = {}
	all_events = frappe.db.sql("""SELECT `name` FROM `tabTP Event` ORDER BY `event_date` ASC LIMIT 1""", as_list=True)
	if len(all_events) == 1:
		context['next_event'] = frappe.get_doc("TP Event", all_events[0][0])
	return context