# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import requests

no_cache = 1

def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	context['spielplan'] = get_spielplan()
	context['tabelle'] = get_tabelle('full')
	return context

def get_spielplan():
	response = requests.get("https://api-v2.swissunihockey.ch/api/games?mode=team&team_id=428691&season=2022&games_per_page=20")
	r = response.json()['data']
	data = {}
	data['titel'] = r['title']
	data['games'] = []
	for game in r['regions'][0]['rows']:
		data['games'].append(game)
	return data
	
def get_tabelle(view='full'):
	response = requests.get("https://api-v2.swissunihockey.ch/api/calendars?season=2022&league=5&game_class=11&group=408429&view={view}".format(view=view))
	r = response.json()['data']
	data = {}
	data['titel'] = r['title']
	data['rankings'] = []
	if len(r['regions']) > 0:
		for ranking in r['regions'][0]['rows']:
			data['rankings'].append(ranking)
	return data

	# Anleitung für Group ID:
	# Das Jahr ändern der folgenden API: https://api-v2.swissunihockey.ch/api/games?mode=team&team_id=428691&season=2022&games_per_page=20 und im 
	# Browser eingeben. Im Browser nach "group" suchen und die Group ID auslesen. 