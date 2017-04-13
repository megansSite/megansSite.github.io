(function ($) {
    
    // Init Wow
    wow = new WOW( {
        animateClass: 'animated',
        offset:       100
    });
    wow.init();
    
    // Navigation scrolls
    $('.navbar-nav li a').bind('click', function(event) {
        $('.navbar-nav li').removeClass('active');
        $(this).closest('li').addClass('active');
        var $anchor = $(this);
        var nav = $($anchor.attr('href'));
        if (nav.length) {
        $('html, body').stop().animate({				
            scrollTop: $($anchor.attr('href')).offset().top				
        }, 1500, 'easeInOutExpo');
        
        event.preventDefault();
        }
    });

    $('.navbar-collapse a').click(function (e) {
        $('.navbar-collapse').collapse('toggle');
    });
    
    // About section scroll
    $(".overlay-detail a").on('click', function(event) {
        event.preventDefault();
        var hash = this.hash;
        $('html, body').animate({
            scrollTop: $(hash).offset().top
        }, 900, function(){
            window.location.hash = hash;
        });
    });
       
    //jQuery to collapse the navbar on scroll
    $(window).scroll(function() {
        if ($(".navbar-default").offset().top > 50) {
            $(".navbar-fixed-top").addClass("top-nav-collapse");
        } else {
            $(".navbar-fixed-top").removeClass("top-nav-collapse");
        }
    });

    // $(window).scroll(function () {
        //         if ($(window).scrollTop() >= $(document).height() - $(window).height() - 1950) {
            
        // }
    // });
    
    
})(jQuery);


  function initMap() {
    var uluru = {lat: 41.988231, lng: -87.808771};
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 12,
      center: uluru,
      zoomControl: true,
    });
    var marker = new google.maps.Marker({
      position: uluru,
      map: map
    });
  }
