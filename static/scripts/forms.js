// Functions for adding image gallery formsets on CreateBlog page.
let addButton = document.querySelector("#add-form");

if (addButton) {
    let imageForm = document.querySelectorAll(".image-form");
    let container = document.querySelector("#formset");
    let totalForms = document.querySelector("#id_blogimage_set-TOTAL_FORMS");

    let formNum = imageForm.length - 1;
    addButton.addEventListener('click', addImageForm);

    function addImageForm(e) {
        e.preventDefault();

        let newForm = imageForm[0].cloneNode(true);
        let formImageRegex = RegExp(`blogimage_set-(\\d){1}-image`, 'g');
        let formTextRegex = RegExp(`blogimage_set-(\\d){1}-text`, 'g');

        formNum++;
        console.log(formNum);
        newForm.innerHTML = newForm.innerHTML.replace(formImageRegex, `blogimage_set-${formNum}-image`);
        newForm.innerHTML = newForm.innerHTML.replace(formTextRegex, `blogimage_set-${formNum}-text`);

        container.insertBefore(newForm, addButton);

        totalForms.setAttribute('value', `${formNum + 1}`);
    }
}

// Functions for adding ingredient formsets on CreateRecipe page.
let addIngredientButton = document.querySelector("#add-ingredient-form");

if (addIngredientButton) {
    let ingredientForm = document.querySelectorAll(".ingredient-form");
    let ingredientContainer = document.querySelector("#formset");
    let ingredientTotalForms = document.querySelector("#id_recipeingredient_set-TOTAL_FORMS");

    let formNumber = ingredientForm.length - 1;
    addIngredientButton.addEventListener('click', addIngredientForm);

    function addIngredientForm(e) {
        e.preventDefault();

        let newForm = ingredientForm[0].cloneNode(true);
        let formRelatedRegex = RegExp(`recipeingredient_set-(\\d){1}-related_product`, 'g');
        let formUnrelatedRegex = RegExp(`recipeingredient_set-(\\d){1}-unrelated_product`, 'g');
        let formAmountRegex = RegExp(`recipeingredient_set-(\\d){1}-amount`, 'g');
        let formTypeRegex = RegExp(`recipeingredient_set-(\\d){1}-type`, 'g');

        formNumber++;
        console.log(formNumber);
        newForm.innerHTML = newForm.innerHTML.replace(formRelatedRegex, `recipeingredient_set-${formNumber}-related_product`);
        newForm.innerHTML = newForm.innerHTML.replace(formUnrelatedRegex, `recipeingredient_set-${formNumber}-unrelated_product`);
        newForm.innerHTML = newForm.innerHTML.replace(formAmountRegex, `recipeingredient_set-${formNumber}-amount`);
        newForm.innerHTML = newForm.innerHTML.replace(formTypeRegex, `recipeingredient_set-${formNumber}-type`);

        ingredientContainer.insertBefore(newForm, addIngredientButton);

        ingredientTotalForms.setAttribute('value', `${formNumber + 1}`);
    }
}


