from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Verein / Team / Mitglieder"),
			"items": [
				{
					"type": "doctype",
					"name": "Verein",
				},
				{
					"type": "doctype",
					"name": "Team",
					"dependencies": ["Verein"]
				},
				{
					"type": "doctype",
					"name": "Mitglied",
					"dependencies": ["Team"]
				}
			]
		}
	]
