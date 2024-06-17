//Select2



//Functions for the Brand/Category filter
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

function filterFunction(inputId, dropdownId) {
  var input, filter, div, p, i, txtValue;
  input = document.getElementById(inputId);
  filter = input.value.toUpperCase();
  div = document.getElementById(dropdownId);
  p = div.getElementsByTagName("p");

  for (i = 0; i < p.length; i++) {
      txtValue = p[i].textContent || p[i].innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
          p[i].style.display = "";
      } else {
          p[i].style.display = "none";
      }
  }
}
