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
	change_status('teamplaner.www.ereignisse.anmelden', event_name);
}

function abmelden(event_name) {
	show_waiting_screen();
	change_status('teamplaner.www.ereignisse.abmelden', event_name);
}

function komme_zu_spaet(event_name) {
	show_waiting_screen();
	change_status('teamplaner.www.ereignisse.komme_zu_spaet', event_name);
}

function komme_puenktlich(event_name) {
	show_waiting_screen();
	change_status('teamplaner.www.ereignisse.anmelden', event_name);
}

function change_status(_method, _event_name) {
	console.log(_method);
	console.log(_event_name);
	frappe.call({
		method: _method,
		args: {
			event_name: _event_name
		},
		callback: function(r) {
			if(r.message) {
				location.reload();
			} 
		}
	});
}