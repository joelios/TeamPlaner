# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def get_user_profile(user):
	user_profile_name = frappe.db.sql("""SELECT `name` FROM `tabMitglied` WHERE `user_id` = '{user}'""".format(user=user), as_list=True)
	try:
		user_pofile = frappe.get_doc("Mitglied", user_profile_name[0][0])
	except:
		user_pofile = False
	return user_pofile