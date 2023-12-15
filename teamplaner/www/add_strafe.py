# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

no_cache = 1

def get_context(context):
    context['next_game'] = {}
    next_game = frappe.db.sql("""SELECT `name` FROM `tabTP Event` WHERE `typ` = 'Match' AND `event_date` > CURDATE() - INTERVAL 1 DAY ORDER BY `event_date` ASC LIMIT 1""", as_list=True)
    if len(next_game) == 1:
        context['next_game'] = frappe.get_doc("TP Event", next_game[0][0])