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



//Functions for adding image gallery formsets on CreateBlog page.
let imageForm = document.querySelectorAll(".image-form")
let container = document.querySelector("#formset")
let addButton = document.querySelector("#add-form")
let totalForms = document.querySelector("#id_blogimage_set-TOTAL_FORMS")

let formNum = imageForm.length-1
addButton.addEventListener('click', addForm)

function addForm(e){
    e.preventDefault()

    let newForm = imageForm[0].cloneNode(true)
    let formImageRegex = RegExp(`blogimage_set-(\\d){1}-image`,'g')
    let formTextRegex = RegExp(`blogimage_set-(\\d){1}-text`,'g')

    formNum++
    console.log(formNum)
    newForm.innerHTML = newForm.innerHTML.replace(formImageRegex, `blogimage_set-${formNum}-image`)
    newForm.innerHTML = newForm.innerHTML.replace(formTextRegex, `blogimage_set-${formNum}-text`)

    container.insertBefore(newForm, addButton)
    
    totalForms.setAttribute('value', `${formNum+1}`)
}