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


//Function to search through bottle/brand tiles

function searchFunction(inputId, targetClass) {
  const searchInput = document.getElementById(inputId);
  const tiles = document.querySelectorAll('.' + targetClass);

  const filter = searchInput.value.toUpperCase();

  tiles.forEach(function(tile) {
      const brandNameElement = tile.querySelector('h4'); // For bottles
      const bottleNameElement = tile.querySelector('h2'); // For both brands and bottles

      const brandName = brandNameElement ? brandNameElement.textContent.toUpperCase() : '';
      const bottleName = bottleNameElement ? bottleNameElement.textContent.toUpperCase() : '';

      if (brandName.includes(filter) || bottleName.includes(filter)) {
          tile.style.display = "";
      } else {
          tile.style.display = "none";
      }
  });
}


//Function to set the amount of servings in a cocktail
document.addEventListener('DOMContentLoaded', function() {
  const servingsInput = document.getElementById('servings-amount');
  const ingredientAmountCells = document.querySelectorAll('td[data-amount]');

  function updateIngredientAmounts() {
      const multiplier = parseFloat(servingsInput.value);
      ingredientAmountCells.forEach(cell => {
          const originalAmount = parseFloat(cell.getAttribute('data-amount'));
          let newAmount = (originalAmount * multiplier).toFixed(2);
          if (isNaN(newAmount)) {
              newAmount = originalAmount.toFixed(2);
          }
          cell.textContent = newAmount;
      });
  }

  // Initial update when the page loads
  updateIngredientAmounts();

  // Update amounts whenever the input value changes
  servingsInput.addEventListener('input', updateIngredientAmounts);
});

