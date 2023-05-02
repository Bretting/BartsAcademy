from django import forms
from .models import (
    Category,
)


class CategoryForm(forms.Form):
    model = Category
    fields = ['name','subcategory','info','image','video']
    
