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
        
    context['events'] = []

    all_events = frappe.db.sql("""SELECT `name` FROM `tabTP Event` WHERE `event_date` > CURDATE() - INTERVAL 1 DAY ORDER BY `event_date` ASC, `event_from` ASC""", as_list=True)

    for event in all_events:
        context['events'].append(frappe.get_doc("TP Event", event[0]))
    return context
	
@frappe.whitelist()
def anmelden(event_name, begruendung):
    send_notification(event_name, 'hat sich angemeldet', 'Anmeldung')
    frappe.db.sql("""UPDATE `tabTP Event Teilnehmer` SET `status` = 'Anwesend', `bemerkung` = '{begruendung}' WHERE `parent` = '{event_name}' AND `user` = '{user}'""".format(event_name=event_name, user=frappe.session.user, begruendung=begruendung), as_list=True)
    frappe.db.commit()
    return 'ok'

@frappe.whitelist()
def abmelden(event_name, begruendung):
    send_notification(event_name, 'hat sich abgemeldet', 'Abmeldung')
    frappe.db.sql("""UPDATE `tabTP Event Teilnehmer` SET `status` = 'Abwesend', `bemerkung` = '{begruendung}' WHERE `parent` = '{event_name}' AND `user` = '{user}'""".format(event_name=event_name, user=frappe.session.user, begruendung=begruendung), as_list=True)
    frappe.db.commit()
    goali_alert = check_goalis(event_name)
    if goali_alert:
        event = frappe.get_doc("TP Event", event_name)
        frappe.sendmail(
            recipients=get_recipients(True),
            sender="teamplaner@msmr.ch",
            subject="Goali Alarm",
            message="Hi Team-Mate<br><br>Achtung; am Event vom {datum} sind <b>weniger als 2 Torhüter</b> angemeldet!<br><br>Dein TeamPlaner<br><br><br><br>(Du möchtest dieses Mail nicht mehr erhalten? Deaktiviere die Notification im TeamPlaner!)".format(datum=frappe.utils.get_datetime(event.event_date).strftime('%d.%m.%Y'))
        )
    return 'ok'

@frappe.whitelist()
def komme_zu_spaet(event_name, begruendung):
    send_notification(event_name, 'wird sich verspäten', 'Verspätung')
    frappe.db.sql("""UPDATE `tabTP Event Teilnehmer` SET `status` = 'Verspätet', `bemerkung` = '{begruendung}' WHERE `parent` = '{event_name}' AND `user` = '{user}'""".format(event_name=event_name, user=frappe.session.user, begruendung=begruendung), as_list=True)
    frappe.db.commit()
    return 'ok'

@frappe.whitelist()
def get_more(shift):

    if not shift > 0:
        shift = 20
        
    all_events = frappe.db.sql("""SELECT `name` FROM `tabTP Event` WHERE `event_date` > CURDATE() - INTERVAL 1 DAY ORDER BY `event_date` ASC LIMIT {shift},20""".format(shift=shift), as_list=True)
    events = []
    for event in all_events:
        events.append(frappe.get_doc("TP Event", event[0]))
    return {
        'events': events,
        'shift': 20
    }

def send_notification(event_name, nachricht, status):
    mitglied = get_user_profile()
    event = frappe.get_doc("TP Event", event_name)
    frappe.sendmail(
        recipients=get_recipients(),
        sender="teamplaner@msmr.ch",
        subject="Teilnehmer Mutation ({status})".format(status=status),
        message="Hi Team-Mate<br><br>{vorname} {nachname} {nachricht}.<br>Dies betrifft den Event vom {datum}<br><br>Dein TeamPlaner<br><br><br><br>(Du möchtest dieses Mail nicht mehr erhalten? Deaktiviere die Notification im TeamPlaner!)".format(vorname=mitglied.vorname, nachname=mitglied.nachname, nachricht=nachricht, datum=frappe.utils.get_datetime(event.event_date).strftime('%d.%m.%Y'))
    )

def get_recipients(goali_alert=False):
    if goali_alert:
        _recipients = frappe.db.sql("""SELECT `parent` FROM `tabHas Role` WHERE `role` = 'Notification Goali Alarm'""", as_dict=True)
    else:
        _recipients = frappe.db.sql("""SELECT `parent` FROM `tabHas Role` WHERE `role` = 'Notification An Abmeldung'""", as_dict=True)
    recipients = []
    for _recipient in _recipients:
        recipients.append(_recipient.parent)
    return recipients

def check_goalis(event_name):
    mitglied = get_user_profile()
    if mitglied.position == 'Torwart':
        goali_qty = frappe.db.sql("""SELECT COUNT(`name`) AS `qty` FROM `tabTP Event Teilnehmer` WHERE `parent` = '{event_name}' AND `status` = 'Anwesend' AND `mitglied` IN (SELECT `name` FROM `tabMitglied` WHERE `position` = 'Torwart')""".format(event_name=event_name), as_dict=True)[0].qty
        if goali_qty < 5:
            return True
        else:
            return False
    else:
        return False
