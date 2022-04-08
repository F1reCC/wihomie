from django import forms

from .models import FeatureValidator, CategoryFeature
from product.models import Category, Product


class NewCategoryFeatureKeyForm(forms.ModelForm):

    class Meta:
        model = CategoryFeature
        fields = '__all__'


class NewCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'

class NewProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'


class FeatureValidatorForm(forms.ModelForm):

    class Meta:
        model = FeatureValidator
        fields = ['category']


