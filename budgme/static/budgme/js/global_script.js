$(document).ready(function() {
    //===> tooltip init
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-load="ajax"]').each(function () {
        $(this).click(function (event) {
            event.preventDefault();
            pathname = $(this).prop('href').replace('http://', '').replace('https://', '').replace(window.location.host, '');
            getAjaxPage(pathname);
        })
    })

    //===> profile page success message fadeOut (should be moved to profile page?)
    // $("div.fadeout-slowly-3").fadeOut(3000);
    $("span.fadeout-slowly-3").css({opacity: 1.0, visibility: "visible"}).animate({opacity: 0.0},3000);

    var exclude_ajax_urls  = [
        '/login', '/logout', '/password_change/', '/password_change/done/',
    ]
    // load with delay 1 sec
    // $(this).delay(1000).queue(function() {
    //     ajaxGet('/ajax' + window.location.pathname, {}, function (content) {
    //         $("#loader-animation").hide();
    //     });
    //     $(this).dequeue();
    // });

    // direct method load
    if ($.inArray(window.location.pathname, exclude_ajax_urls) == -1){
        getAjaxPage(window.location.pathname);
    }
    $("#loader-animation").fadeOut(1000);
});

function getAjaxPage(url) {
    $("#loader-animation").show();
    $("#main-container").hide();
    try{
        ajaxGet('/ajax' + url, {'width': $(document).width()}, function (content) {
            $("#main-container").fadeIn(1000);
            $("#loader-animation").fadeOut(1000);
        });
    }
    finally {
        $("#loader-animation").fadeOut(1000);
    }
}