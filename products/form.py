
from django import forms
from django.forms import inlineformset_factory
from django.utils.text import slugify
from django.utils.text import slugify

from .models import Product, ProductImage, Category


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = [
            "name",
            "slug",
            "description",
            "image",
            "is_active",
        ]

        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
            }),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip()

        if not slug:
            slug = slugify(self.cleaned_data.get("name", ""))

        original_slug = slug
        counter = 1

        while Category.objects.filter(slug=slug).exclude(
            pk=self.instance.pk
        ).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        return slug

        

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
            "description": forms.Textarea(attrs={"rows": 5}),
            "price": forms.NumberInput(attrs={"step": "0.01"}),
            "discount_price": forms.NumberInput(attrs={"step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].queryset = Category.objects.filter(
            is_active=True
        ).order_by("name")

        self.fields["category"].empty_label = "Select a category"
        self.fields["category"].label = "Product Category"

        # Slug can be generated automatically.
        self.fields["slug"].required = False

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip()

        # Generate a slug from the product name if none was supplied.
        if not slug:
            name = self.cleaned_data.get("name", "")
            base_slug = slugify(name)

            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exclude(
                pk=self.instance.pk
            ).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

        # Ensure a manually entered slug is unique too.
        existing = Product.objects.filter(slug=slug).exclude(
            pk=self.instance.pk
        )

        if existing.exists():
            raise forms.ValidationError(
                "This URL slug is already in use. Please choose another."
            )

        return slug

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
    extra=3,
    can_delete=True,
)
