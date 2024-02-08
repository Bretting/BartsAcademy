//Select2
$(document).ready(function() {
  $('#id_category').select2({ 
      theme:'bootstrap-5'   
      });
      
  $('#id_brand').select2({
      theme:'bootstrap-5'                 
  });

  $('#id_category_tag').select2({
    theme:'bootstrap-5'                 
  });
  $('#id_brand_tag').select2({
    theme:'bootstrap-5'                 
  });
  $('#id_bottle_tag').select2({
    theme:'bootstrap-5'                 
  });

  $(".owl-carousel").owlCarousel({
    center: true,
    items:4,
    loop:true,
    autoplay:true,
    autoplayTimeout:1500,
    autoplayHoverPause:true,
    lazyload: true,
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