// open nav
$("[data-trigger]").on("click", function(){
    $('#main_nav').toggleClass("show");
});

// close nav 
$(".offcanvas-header").click(function(){
    $("#main_nav").removeClass("show");
}); 

// Ereignisse
function anmelden(event_name) {
	show_waiting_screen();
	change_status('teamplaner.www.ereignisse.anmelden', event_name, '');
}

function abmelden(event_name) {
	var begruendung = $("#begruendung" + event_name).val();
	if (begruendung.length > 3) {
		$("#dismissbtn" + event_name).click();
		show_waiting_screen();
		change_status('teamplaner.www.ereignisse.abmelden', event_name, begruendung);
	} else {
		$("#begruendung" + event_name).css("border","2px solid red");
	}
}

function komme_zu_spaet(event_name) {
	show_waiting_screen();
	change_status('teamplaner.www.ereignisse.komme_zu_spaet', event_name, '');
}

function komme_puenktlich(event_name) {
	show_waiting_screen();
	change_status('teamplaner.www.ereignisse.anmelden', event_name, '');
}

function change_status(_method, _event_name, begruendung) {
	frappe.call({
		method: _method,
		args: {
			'event_name': _event_name,
			'begruendung': begruendung
		},
		callback: function(r) {
			if(r.message) {
				location.reload();
			} 
		}
	});
}
