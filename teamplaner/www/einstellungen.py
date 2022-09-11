# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from teamplaner.utils import get_user_profile

no_cache = 1

def get_context(context):
    if frappe.session.user=='Guest':
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
        
    context['user_stamm'] = get_user_profile()
    return context

@frappe.whitelist()
def change_noti(noti):
    mitglied = frappe.get_doc("Mitglied", get_user_profile().name)
    
    if noti == 'new_event':
        if mitglied.new_event:
            mitglied.new_event = 0
        else:
            mitglied.new_event = 1
    
    if noti == 'changed_event':
        if mitglied.changed_event:
            mitglied.changed_event = 0
        else:
            mitglied.changed_event = 1
    
    if noti == 'new_aufgebot':
        if mitglied.new_aufgebot:
            mitglied.new_aufgebot = 0
        else:
            mitglied.new_aufgebot = 1
    
    if noti == 'teilnehmer_mutation':
        if mitglied.teilnehmer_mutation:
            mitglied.teilnehmer_mutation = 0
        else:
            mitglied.teilnehmer_mutation = 1
    
    if noti == 'event_preview':
        if mitglied.event_preview:
            mitglied.event_preview = 0
        else:
            mitglied.event_preview = 1
    
    if noti == 'goali_alarm':
        if mitglied.goali_alarm:
            mitglied.goali_alarm = 0
        else:
            mitglied.goali_alarm = 1
    
    mitglied.save(ignore_permissions=True)
    frappe.db.commit()
    return
