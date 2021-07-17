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
	return context

def _get_tabelle():
	tabelle = get_tabelle('short')
	data = {}
	data['rankings'] = []
	data['go_for_it'] = False
	if len(tabelle['rankings']) > 0:
		data['go_for_it'] = True
		counter = 0
		for ranking in tabelle['rankings']:
			if ranking['cells'][1] == 'HC Rychenberg Winterthur II':
				if counter > 0:
					# hcr = 2. oder schlechter
					data['rankings'] = [
						[
							tabelle['regions'][0]['rows'][counter - 1]['cells'][0],
							tabelle['regions'][0]['rows'][counter - 1]['cells'][1],
							tabelle['regions'][0]['rows'][counter - 1]['cells'][3],
							tabelle['regions'][0]['rows'][counter - 1]['cells'][4]
						],
						[
							'<b>' + ranking['cells'][0] + '</b>',
							'<b>' + ranking['cells'][1] + '</b>',
							'<b>' + ranking['cells'][3] + '</b>',
							'<b>' + ranking['cells'][4] + '</b>'
						],
						[
							tabelle['regions'][0]['rows'][counter + 1]['cells'][0],
							tabelle['regions'][0]['rows'][counter + 1]['cells'][1],
							tabelle['regions'][0]['rows'][counter + 1]['cells'][3],
							tabelle['regions'][0]['rows'][counter + 1]['cells'][4]
						]
					]
				else:
					# hcr 1.
					data['rankings'] = [
						[
							'<b>' + ranking['cells'][0] + '</b>',
							'<b>' + ranking['cells'][1] + '</b>',
							'<b>' + ranking['cells'][3] + '</b>',
							'<b>' + ranking['cells'][4] + '</b>'
						],
						[
							tabelle['regions'][0]['rows'][counter + 1]['cells'][0],
							tabelle['regions'][0]['rows'][counter + 1]['cells'][1],
							tabelle['regions'][0]['rows'][counter + 1]['cells'][3],
							tabelle['regions'][0]['rows'][counter + 1]['cells'][4]
						],
						[
							tabelle['regions'][0]['rows'][counter + 2]['cells'][0],
							tabelle['regions'][0]['rows'][counter + 2]['cells'][1],
							tabelle['regions'][0]['rows'][counter + 2]['cells'][3],
							tabelle['regions'][0]['rows'][counter + 2]['cells'][4]
						]
					]
			else:
				counter += 1
	return data
