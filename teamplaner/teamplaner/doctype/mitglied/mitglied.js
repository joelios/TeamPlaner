// Copyright (c) 2020, msmr.ch and contributors
// For license information, please see license.txt

frappe.ui.form.on('Mitglied', {
	 refresh: function(frm) {
		frm.add_custom_button(__("Update User in Events"), function() {
            update_user_in_events(frm);
        });
        frm.add_custom_button(__("Add all User to all Events"), function() {
            add_all_user_to_all_events(frm);
        });
	 }
});

function update_user_in_events(frm) {
    frappe.call({
        "method": "teamplaner.utils.update_user_in_events",
        "args": {},
        "async": false,
        "callback": function(response) {
            frappe.msgprint("done");
        }
    });
}

function add_all_user_to_all_events(frm) {
    frappe.call({
        "method": "teamplaner.utils.add_all_user_to_all_events",
        "args": {},
        "async": false,
        "callback": function(response) {
            frappe.msgprint("done");
        }
    });
}
