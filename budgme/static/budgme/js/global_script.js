$(document).ready(function() {
    //===> tooltip init
    $('[data-toggle="tooltip"]').tooltip();

    //===> profile page success message fadeOut (should be moved to profile page?)
    // $("div.fadeout-slowly-3").fadeOut(3000);
    $("span.fadeout-slowly-3").css({opacity: 1.0, visibility: "visible"}).animate({opacity: 0.0},3000);

    $(this).delay(1000).queue(function() {
        ajaxGet('/ajax' + window.location.pathname, {}, function (content) {
            $("#loader-animation").hide();
        });
        $(this).dequeue();
    });
});