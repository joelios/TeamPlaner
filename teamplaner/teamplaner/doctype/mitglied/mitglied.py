# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Mitglied(Document):
    def validate(self):
        # remove notification roles
        entries = frappe.db.sql("""SELECT `name` FROM `tabHas Role` WHERE `parent` = '{user}'""".format(user=self.user_id), as_dict=True)
        for entry in entries:
            role_entry = frappe.get_doc("Has Role", entry.name)
            role_entry.delete()
            frappe.db.commit()
        
        
        # add default role
        user = frappe.get_doc("User", self.user_id)
        user.roles = []
        user.append('roles',{
                    "doctype": "Has Role",
                    "role": "teamplaner spieler"
                    })
        
        # add notification roles
        # neues aufgebot
        if self.new_aufgebot:
            user.append('roles',{
                        "doctype": "Has Role",
                        "role": "Notification Aufgebot"
                        })
        
        # neuer event
        if self.new_event:
            user.append('roles',{
                        "doctype": "Has Role",
                        "role": "Notification Neuer Event"
                        })
        
        # änderung event
        if self.changed_event:
            user.append('roles',{
                        "doctype": "Has Role",
                        "role": "Notification changed Event"
                        })
        
        # an / abmeldung
        if self.teilnehmer_mutation:
            user.append('roles',{
                        "doctype": "Has Role",
                        "role": "Notification An Abmeldung"
                        })
        
        # event preview
        if self.event_preview:
            user.append('roles',{
                        "doctype": "Has Role",
                        "role": "Notification Event Preview"
                        })
        
        # goali alarm
        if self.goali_alarm:
            user.append('roles',{
                        "doctype": "Has Role",
                        "role": "Notification Goali Alarm"
                        })
        
        user.save(ignore_permissions=True)
        frappe.db.commit()
    
    def on_trash(self):
        delete_anmeldungen = frappe.db.sql("""DELETE FROM `tabTP Event Teilnehmer` WHERE `mitglied` = '{user}'""".format(user=self.name), as_dict=True)
        frappe.db.commit()
