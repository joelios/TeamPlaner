# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from teamplaner.utils import get_team_img, get_user_list, get_staff_img

no_cache = 1

def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	
	context['team_img'] = get_team_img()
	context['staff_img'] = get_staff_img()
	context['users'] = get_user_list()
	return context