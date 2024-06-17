$(document).ready(function() {
  
    $(".owl-carousel").owlCarousel({
      center: true,
      items:5,
      loop:true,
      autoplay:true,
      autoplayTimeout:1500,
      autoplayHoverPause:true,
      lazyload: true,
      margin:75,
      responsive : {
        // breakpoint from 0 up
        0 : {
            items:1,
            nav:false,
            margin:0
        },
        // breakpoint from 480 up
        480 : {
            items:3,
            nav:false,
        }
      }
    });
  });