
from django import forms
from django.forms import inlineformset_factory

from .models import Product, ProductImage


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            "category",
            "name",
            "slug",
            "sku",
            "brand",
            "description",
            "price",
            "discount_price",
            "image",
            "is_active",
            "is_featured",
        ]

        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 5,
            }),
            "price": forms.NumberInput(attrs={
                "step": "0.01",
            }),
            "discount_price": forms.NumberInput(attrs={
                "step": "0.01",
            }),
        }


class ProductImageForm(forms.ModelForm):

    class Meta:
        model = ProductImage

        fields = [
            "image",
            "alt_text",
            "is_primary",
        ]


ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=1,
    can_delete=True,
)
