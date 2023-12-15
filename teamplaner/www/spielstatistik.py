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
    
    user_roles = frappe.get_roles(frappe.session.user) or []
    if "Staff" not in user_roles:
        frappe.throw("Hier haben nur Trainer Zugang.", frappe.PermissionError)
    
    context['user_roles'] = user_roles
    context['next_game'] = {}
    next_game = frappe.db.sql("""SELECT `name` FROM `tabTP Event` WHERE `typ` = 'Match' AND `event_date` > CURDATE() - INTERVAL 1 DAY ORDER BY `event_date` ASC LIMIT 1""", as_list=True)
    if len(next_game) == 1:
        context['next_game'] = frappe.get_doc("TP Event", next_game[0][0])
        context['game_id'] = context['next_game'].name
        tore = 0
        gegentore = 0
        for aktion in context['next_game'].spielverlauf:
            if aktion['aktion'] == 'Tor':
                tore += 1
            elif aktion['aktion'] == 'Gegentor':
                gegentore += 1
        context['tore'] = tore
        context['gegentore'] = gegentore