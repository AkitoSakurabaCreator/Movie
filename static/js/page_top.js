jQuery(function() {
    var appear = false;
    var pagetop = $('#page_top');
    $(window).scroll(function() {
        if ($(this).scrollTop() > 200) {
            if (appear == false) {
                appear = true;
                pagetop.stop().animate({
                    'right': '5px'
                }, 300);
            }
        } else {
            if (appear) {
                appear = false;
                pagetop.stop().animate({
                    'right': '-50px'
                }, 300);
            }
        }
    });
});