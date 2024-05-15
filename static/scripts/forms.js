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


