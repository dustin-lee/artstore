from django import forms
from django.forms import formset_factory
ProductFormSet = formset_factory(ProductForm)

class ProductForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    body = forms.CharField(max_length=245, label="Item Description")

class Meta:
    model = Product
    fields = ('title', 'body', )

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

class Meta:
    model = Image
    fields = ('image', )
