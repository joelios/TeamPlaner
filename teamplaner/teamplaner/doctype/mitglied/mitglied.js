// Copyright (c) 2020, msmr.ch and contributors
// For license information, please see license.txt

frappe.ui.form.on('Mitglied', {
	 refresh: function(frm) {
		frm.add_custom_button(__("Update all User in Events"), function() {
            update_user_in_events(frm);
        });
        frm.add_custom_button(__("Update THIS User in Events"), function() {
            update_this_user_in_events(frm);
        });
        frm.add_custom_button(__("Add all User to all Events"), function() {
            add_all_user_to_all_events(frm);
        });
        frm.add_custom_button(__("Add THIS User to all Events"), function() {
            add_this_user_to_all_events(frm);
        });
	 },
	 pos_bilanz: function(frm){
	    cur_frm.set_value('bilanz', cur_frm.doc.pos_bilanz - cur_frm.doc.neg_bilanz);
	},
	neg_bilanz: function(frm){
	    cur_frm.set_value('bilanz', cur_frm.doc.pos_bilanz - cur_frm.doc.neg_bilanz);
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

function update_this_user_in_events(frm) {
    frappe.call({
        "method": "teamplaner.utils.update_this_user_in_events",
        "args": {"user": cur_frm.doc.name},
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

function add_this_user_to_all_events(frm) {
    frappe.call({
        "method": "teamplaner.utils.add_this_user_to_all_events",
        "args": {"user": cur_frm.doc.name},
        "async": false,
        "callback": function(response) {
            frappe.msgprint("done");
        }
    });
}
