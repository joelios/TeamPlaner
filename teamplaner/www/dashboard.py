# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from teamplaner.www.statistiken import get_top_three
from teamplaner.www.swissunihockey import get_tabelle

no_cache = 1

def get_context(context):
    if frappe.session.user=='Guest':
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    context['next_event'] = {}
    next_event = frappe.db.sql("""SELECT `name` FROM `tabTP Event` WHERE `typ` != 'Match' AND `event_date` > CURDATE() - INTERVAL 1 DAY ORDER BY `event_date` ASC LIMIT 1""", as_list=True)
    if len(next_event) == 1:
        context['next_event'] = frappe.get_doc("TP Event", next_event[0][0])
    context['next_game'] = {}
    next_game = frappe.db.sql("""SELECT `name` FROM `tabTP Event` WHERE `typ` = 'Match' AND `event_date` > CURDATE() - INTERVAL 1 DAY ORDER BY `event_date` ASC LIMIT 1""", as_list=True)
    if len(next_game) == 1:
        context['next_game'] = frappe.get_doc("TP Event", next_game[0][0])
    context['top_three'] = get_top_three()
    context['tabelle'] = _get_tabelle()
    context['topscorer'] = get_topscorer(limit=3)
    return context

def _get_tabelle():
    tabelle = get_tabelle()
    data = {}
    data['rankings'] = []
    data['go_for_it'] = False
    if len(tabelle['rankings']) > 0:
        data['go_for_it'] = True
        counter = 0
        for ranking in tabelle['rankings']:
            if ranking['data']['team']['name'] == 'HC Rychenberg Winterthur II':
                if counter > 0:
                    if counter > 6:
                        # hcr letzter
                        platz1 = [
                                str(tabelle['rankings'][counter - 2]['cells'][0]["text"][0]),
                                str(tabelle['rankings'][counter - 2]['cells'][2]["text"][0]),
                                str(tabelle['rankings'][counter - 2]['cells'][9]["text"][0]),
                                str(tabelle['rankings'][counter - 2]['cells'][10]["text"][0])
                            ]
                        data['rankings'].append(platz1)
                        platz2 = [
                                str(tabelle['rankings'][counter - 1]['cells'][0]["text"][0]),
                                str(tabelle['rankings'][counter - 1]['cells'][2]["text"][0]),
                                str(tabelle['rankings'][counter - 1]['cells'][9]["text"][0]),
                                str(tabelle['rankings'][counter - 1]['cells'][10]["text"][0])
                            ]
                        data['rankings'].append(platz2)
                        hcr_data = [
                                '<b>' + str(ranking['cells'][0]["text"][0]) + '</b>',
                                '<b>' + str(ranking['cells'][2]["text"][0]) + '</b>',
                                '<b>' + str(ranking['cells'][9]["text"][0]) + '</b>',
                                '<b>' + str(ranking['cells'][10]["text"][0]) + '</b>'
                            ]
                        data['rankings'].append(hcr_data)
                        break
                    else:
                        # hcr = 2. oder schlechter
                        platz1 = [
                                str(tabelle['rankings'][counter - 1]['cells'][0]["text"][0]),
                                str(tabelle['rankings'][counter - 1]['cells'][2]["text"][0]),
                                str(tabelle['rankings'][counter - 1]['cells'][9]["text"][0]),
                                str(tabelle['rankings'][counter - 1]['cells'][10]["text"][0])
                            ]
                        data['rankings'].append(platz1)
                        hcr_data = [
                                '<b>' + str(ranking['cells'][0]["text"][0]) + '</b>',
                                '<b>' + str(ranking['cells'][2]["text"][0]) + '</b>',
                                '<b>' + str(ranking['cells'][9]["text"][0]) + '</b>',
                                '<b>' + str(ranking['cells'][10]["text"][0]) + '</b>'
                            ]
                        data['rankings'].append(hcr_data)
                        platz2 = [
                                str(tabelle['rankings'][counter + 1]['cells'][0]["text"][0]),
                                str(tabelle['rankings'][counter + 1]['cells'][2]["text"][0]),
                                str(tabelle['rankings'][counter + 1]['cells'][9]["text"][0]),
                                str(tabelle['rankings'][counter + 1]['cells'][10]["text"][0])
                            ]
                        data['rankings'].append(platz2)
                        break
                else:
                    # hcr 1.
                    hcr_data = [
                            '<b>' + str(ranking['cells'][0]["text"][0]) + '</b>',
                            '<b>' + str(ranking['cells'][2]["text"][0]) + '</b>',
                            '<b>' + str(ranking['cells'][9]["text"][0]) + '</b>',
                            '<b>' + str(ranking['cells'][10]["text"][0]) + '</b>'
                        ]
                    data['rankings'].append(hcr_data)
                    platz1 = [
                            str(tabelle['rankings'][counter + 1]['cells'][0]["text"][0]),
                            str(tabelle['rankings'][counter + 1]['cells'][2]["text"][0]),
                            str(tabelle['rankings'][counter + 1]['cells'][9]["text"][0]),
                            str(tabelle['rankings'][counter + 1]['cells'][10]["text"][0])
                        ]
                    data['rankings'].append(platz1)
                    platz2 = [
                            str(tabelle['rankings'][counter + 2]['cells'][0]["text"][0]),
                            str(tabelle['rankings'][counter + 2]['cells'][2]["text"][0]),
                            str(tabelle['rankings'][counter + 2]['cells'][9]["text"][0]),
                            str(tabelle['rankings'][counter + 2]['cells'][10]["text"][0])
                        ]
                    data['rankings'].append(platz2)
                    break
            else:
                counter += 1
    return data

def get_topscorer(limit=False):
    if limit:
        limit = ' Limit {limit}'.format(limit=limit)
    else:
        limit = ''
    scorer = frappe.db.sql("""SELECT `vorname`, `nachname`, `tore`, `assists`, (`tore` + `assists`) AS `punkte` FROM `tabMitglied` ORDER BY `punkte` DESC, `tore` DESC, `nachname` ASC{limit}""".format(limit=limit), as_dict=True)
    return scorer
