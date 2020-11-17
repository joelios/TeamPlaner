// open nav
$("[data-trigger]").on("click", function(){
    $('#main_nav').toggleClass("show");
});

// close nav 
$(".offcanvas-header").click(function(){
    $("#main_nav").removeClass("show");
}); 