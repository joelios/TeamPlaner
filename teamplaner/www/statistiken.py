# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

no_cache = 1

def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
		
	context['table'] = get_praesenz_table()
	context['bussen'] = get_bussen()
		
def get_praesenz_table(limit=False):
	filter = ''
	if limit:
		filter = ' LIMIT ' + str(limit)
	data = frappe.db.sql("""SELECT
								`tpet`.`mitglied` AS `mitglied`,
								`tpet`.`vorname` AS `vorname`,
								`tpet`.`nachname` AS `nachname`,
								IFNULL(`tble_anw`.`anwesend`, 0) AS `anwesend`,
								IFNULL(`tble_abw`.`abwesend`, 0) AS `abwesend`,
								IFNULL(`tble_sp`.`spaet`, 0) AS `spaet`,
								(IFNULL(`tble_anw`.`anwesend`, 0) + IFNULL(`tble_sp`.`spaet`, 0) - IFNULL(`tble_abw`.`abwesend`, 0)) AS `points`,
								((100 / (IFNULL(`tble_anw`.`anwesend`, 0) + IFNULL(`tble_abw`.`abwesend`, 0) + IFNULL(`tble_sp`.`spaet`, 0))) * (IFNULL(`tble_anw`.`anwesend`, 0) + IFNULL(`tble_sp`.`spaet`, 0))) AS `percent`
							FROM `tabTP Event Teilnehmer` AS `tpet`
							LEFT JOIN
							(
								SELECT
									`tpetanwesend`.`mitglied` AS `mitglied`,
									COUNT(`tpetanwesend`.`mitglied`) AS `anwesend`
								FROM `tabTP Event Teilnehmer` AS `tpetanwesend`
								WHERE `tpetanwesend`.`status` = 'Anwesend'
								AND `tpetanwesend`.`parent` IN (SELECT `name` FROM `tabTP Event` WHERE `event_date` <= CURDATE())
								GROUP BY `tpetanwesend`.`mitglied`) AS `tble_anw` ON `tble_anw`.`mitglied` = `tpet`.`mitglied`
							LEFT JOIN
							(
								SELECT
									`tpetabwesend`.`mitglied` AS `mitglied`,
									COUNT(`tpetabwesend`.`mitglied`) AS `abwesend`
								FROM `tabTP Event Teilnehmer` AS `tpetabwesend`
								WHERE `tpetabwesend`.`status` = 'Abwesend'
								AND `tpetabwesend`.`parent` IN (SELECT `name` FROM `tabTP Event` WHERE `event_date` <= CURDATE())
								GROUP BY `tpetabwesend`.`mitglied`) AS `tble_abw` ON `tble_abw`.`mitglied` = `tpet`.`mitglied`
							LEFT JOIN
							(
								SELECT
									`tpetspaet`.`mitglied` AS `mitglied`,
									COUNT(`tpetspaet`.`mitglied`) AS `spaet`
								FROM `tabTP Event Teilnehmer` AS `tpetspaet`
								WHERE `tpetspaet`.`status` = 'Verspätet'
								AND `tpetspaet`.`parent` IN (SELECT `name` FROM `tabTP Event` WHERE `event_date` <= CURDATE())
								GROUP BY `tpetspaet`.`mitglied`) AS `tble_sp` ON `tble_sp`.`mitglied` = `tpet`.`mitglied`
							WHERE `tpet`.`parent` IN (SELECT `name` FROM `tabTP Event` WHERE `event_date` <= CURDATE())
							GROUP BY `tpet`.`mitglied`
							ORDER BY `points` DESC, `spaet` ASC, `vorname` ASC{filter}""".format(filter=filter), as_dict=True)
	return data

def get_top_three():
	return get_praesenz_table(limit=3)

def get_bussen():
	return frappe.db.sql("""SELECT
							`tabBussen`.`parent`,
							SUM(`tabBussen`.`betrag`) AS `betrag`,
							`tabMitglied`.`vorname`,
							`tabMitglied`.`nachname`
							FROM `tabBussen`
							LEFT JOIN `tabMitglied` ON `tabMitglied`.`name` = `tabBussen`.`parent`
							GROUP BY `parent`
							ORDER BY `betrag` DESC""", as_dict=True)
