# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

no_cache = 1

def get_context(context):
	if frappe.session.user != "Guest":
		frappe.local.flags.redirect_location = "/dashboard" if frappe.session.data.user_type=="Website User" else "/desk"
		raise frappe.Redirect
