//Select2
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


//Functions for the Brand/Category filter
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

function filterFunction() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdown");
  a = div.getElementsByTagName("p");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}