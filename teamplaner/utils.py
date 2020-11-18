# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def get_user_profile():
	user_profile_name = frappe.db.sql("""SELECT `name` FROM `tabMitglied` WHERE `user_id` = '{user}'""".format(user=frappe.session.user), as_list=True)
	try:
		user_profile = frappe.get_doc("Mitglied", user_profile_name[0][0])
	except:
		user_profile = False
	return user_profile
	
def get_team_img():
	user_profile = get_user_profile()
	if user_profile:
		try:
			team_img = frappe.get_doc("Team", user_profile.team).bild
		except:
			team_img = False
		return team_img
	else:
		return False
		
def get_user_list():
	user = get_user_profile()
	users = frappe.db.sql("""SELECT `vorname`, `nachname`, `position`, `bild`, `nummer` FROM `tabMitglied` WHERE `team` = '{team}' ORDER BY `vorname` ASC""".format(team=user.team), as_dict=True)
	return users