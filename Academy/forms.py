from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Row, Column, HTML
from django.template.defaultfilters import filesizeformat
from tinymce.widgets import TinyMCE

from .models import (
    Category,
    Bottle,
    Brand,
    AgeGate,
    Blog,
    BlogImage,
    Recipe,
    RecipeIngredient,
)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'subcategory','order','tagline','teaser','info','logo','image','video']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
            Row(
            Column('name', css_class='form-group col-md-5'),
            Column('subcategory', css_class='form-group col-md-5'),
            Column('order', css_class='form-group col-md-2'),
            ),
            Row('tagline', css_class='form-group col-md-12'),
            Row('teaser', css_class='form-group col-md-12'),
            Row('info',css_class='form-group col-md-12'),
            Row(
            Column('logo', css_class='col-md-6 form-control-file form-row my-1'),
            Column('image', css_class='col-md-6 form-control-file form-row my-1')
            ),
            Row('video', css_class='col-md-12 form-control-file form-row my-1'),
            Submit('submit', 'Save', css_class='my-3 btn btn-secondary')
        )
        )
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'sorting','category','owner','country_of_origin','story','image','video']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
            Row(
            Column('name', css_class='form-group col-md-6'),
            Column('category', css_class='form-group col-md-6'),
            ),
            Row(
            Column('sorting', css_class='form-group col-md-4'),
            Column('owner', css_class='form-group col-md-4'),
            Column('country_of_origin', css_class='form-group col-md-4'),
            ),
            Row('story', css_class='form-group col-md-12'),
            Row(
            Column('image', css_class='form-control-file col-md-6 my-1'),
            Column('video', css_class='form-control-file col-md-6 my-1'),
            ),
            Submit('submit', 'Save', css_class='my-3 btn btn-secondary')
            )
        )

class BottleForm(forms.ModelForm):
    class Meta:
        model = Bottle
        fields = ['name','category','sorting','brand','bottle_size','abv','info','tasting_notes','image','shop_link',
                  'consumer_shop_link','website_link','tech_nom','tech_region','tech_source_material','tech_cooking','tech_extraction',
                  'tech_mash','tech_water_source','tech_fermentation','tech_distillation','tech_filtration','tech_still','tech_batch_size',
                  'tech_blend','tech_aging','tech_aging_barrels','tech_other', 'tech_botanicals', 'tech_fruits', 'tech_mezcal_type']

    bottle_size = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'in ML'}))    
    abv = forms.DecimalField(label='ABV',widget=forms.NumberInput(attrs={'placeholder':'00.0%'}))    
    tech_source_material = forms.CharField(label='Source material',required=False,widget=forms.TextInput(attrs={'placeholder':'Agave, Cereals etc'}))
    tech_distillation = forms.CharField(label='Distillation',required=False,widget=forms.TextInput(attrs={'placeholder':'How often & other specifics'}))
    tech_region = forms.CharField(label='Region', required=False, widget=forms.TextInput(attrs={'placeholder':'Specific region of production, I.E. Cognac instead of France'}))
    website_link = forms.URLField(required=False,widget=forms.TextInput(attrs={'placeholder':'please use http://'}))
    shop_link = forms.URLField(required=False,widget=forms.TextInput(attrs={'placeholder':'please use http://'}))
    consumer_shop_link = forms.URLField(required=False,widget=forms.TextInput(attrs={'placeholder':'please use http://'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
            Row(
            Column('name', css_class='form-group col-md-6'),
            Column('category', css_class='form-group col-md-3'),
            Column('sorting', css_class='form-group col-md-3'),
            css_class='form-row my-1'
            ),
            Row(
            Column('brand', css_class='form-group col-md-6'),
            Column('bottle_size', css_class='form-group col-md-3'),
            Column('abv', css_class='form-group col-md-3'),
            Column('tech_region', css_class='form-group col-md-3'),
            css_class='form-row my-1'
            ),css_class='corner px-3 py-2'),
            Row('info', css_class='form-row my-1'
            ),
            Row('tasting_notes', css_class='form-row my-1'
            ),
            Row('image', css_class='form-control-file form-row my-1'
            ),
            Row(
            Column('shop_link', css_class='form-group col-md-4'),
            Column('consumer_shop_link', css_class='form-group col-md-4'),
            Column('website_link', css_class='form-group col-md-4'),
            css_class='form-row mt-1 mb-5'
            ),
            HTML("""<h2>Add technical product info</h2>"""),
            Div(
            Row(
            Column('tech_source_material',css_class='form-group col-md-4'),
            Column('tech_cooking',css_class='form-group col-md-4'),
            Column('tech_extraction',css_class='form-group col-md-4'),
            css_class='form-row my-1'
            ),
            Row(
            Column('tech_nom',css_class='form-group col-md-3'),
            Column('tech_mezcal_type',css_class='form-group col-md-3'),
            css_class='form-row my-1'
            ),
            Row(
            Column('tech_mash',css_class='form-group col-md-3'),
            Column('tech_botanicals',css_class='form-group col-md-3'),
            Column('tech_fruits',css_class='form-group col-md-3'),
            Column('tech_water_source',css_class='form-group col-md-3'),
            ),
            Row('tech_fermentation',css_class='form-row my-1'),
            Row(
            Column('tech_distillation',css_class='form-group col-md-3'),
            Column('tech_filtration',css_class='form-group col-md-3'),
            Column('tech_still',css_class='form-group col-md-3'),
            Column('tech_batch_size',css_class='form-group col-md-3'),
            css_class='form-row my-1'
            ), 
            Row(
            Column('tech_blend',css_class='form-group col-md-3'),
            Column('tech_aging',css_class='form-group col-md-3'),
            Column('tech_aging_barrels',css_class='form-group col-md-3'),
            css_class='form-row my-1'
            ),
            Row('tech_other',css_class='form-row my-1'),
            css_class='corner px-3 py-2'),
            Submit('submit', 'Save', css_class='my-3 btn btn-secondary')
        )

class AgeGateForm(forms.ModelForm):
    class Meta:
        model = AgeGate
        fields = '__all__'
       

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['name','teaser','hero_image','text','video','category_tag','brand_tag','bottle_tag', 'type_tag']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            Div(
            Row('name', css_class='form-row my-1'),
            Row('teaser', css_class='form-control, my-1'),
            Row('text', css_class='form-control, my-1'),
            Row('hero_image', css_class='form-control-file form-row my-1'),
            Row('video', css_class='form-control-file form-row my-1'),
            ),
            Div(
            HTML("""<h3 class='text-center'>Max 4 category and type tags</h3>"""),
            Row(
            Column('category_tag', css_class='form-group col-md-3 my-1'),
            Column('brand_tag', css_class='form-group col-md-3 my-1'),
            Column('bottle_tag', css_class='form-group col-md-3 my-1'),
            Column('type_tag', css_class='form-group col-md-3 my-1'),
            css_class='form-row my-1'
            ),css_class='corner px-3 py-2'),)
            
class BlogImageForm(forms.ModelForm):
    class Meta:
        model = BlogImage
        fields = ['image', 'image_text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            Div(
            Row('image', css_class='form-control-file form-row my-1'),
            Row('image_text', css_class='form-control, my-1'),
            css_class='corner px-3 py-2'))
            

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'type', 'occasion','taste', 'image', 'description', 'recipe_steps'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            Div(
            Row('name', css_class='form-control, my-1'),
            Row(
                Column('taste', css_class='form-control, my-1'),
                Column('type', css_class='form-control, my-1'),
                Column('occasion', css_class='form-control, my-1'),),
            Row('image', css_class='form-control-file form-row my-1'),
            Row('description', css_class='form-control, my-1'),
            Row('recipe_steps', css_class='form-control, my-1'),),)
            # Submit('submit', 'Save', css_class='my-3 btn btn-secondary hide'))
        

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['related_product', 'unrelated_product', 'amount', 'type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            Div(
            Row(
                Column('related_product', css_class='form-control, my-1'),
                Column('unrelated_product', css_class='form-control, my-1'),),
            Row(
                Column('amount', css_class='form-control, my-1'),
                Column('type', css_class='form-control, my-1'),
                ),
            Row('DELETE', css_class='input-small'),
            css_class='corner px-3 py-2'))