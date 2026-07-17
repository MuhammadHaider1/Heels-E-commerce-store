from django.contrib import admin
from django import forms
from .models import Category, Product, ProductImage, Review, Color

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'sizes': forms.Textarea(attrs={'rows': 2, 'placeholder': 'e.g. ["36","37","38"]'}),
            'colors': forms.Textarea(attrs={'rows': 2, 'placeholder': 'e.g. [{"name":"Black","hex":"#000000"}]'}),
            'attributes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g. {"heel_type":"Block Heel","closure":"Zip"}'}),
        }

    def clean_sizes(self):
        val = self.cleaned_data.get('sizes')
        if not val or val == '[]':
            return []
        if isinstance(val, list):
            return val
        import json
        try:
            return json.loads(val)
        except (json.JSONDecodeError, TypeError):
            return []

    def clean_colors(self):
        val = self.cleaned_data.get('colors')
        if not val or val == '[]':
            return []
        if isinstance(val, list):
            return val
        import json
        try:
            return json.loads(val)
        except (json.JSONDecodeError, TypeError):
            return []

    def clean_attributes(self):
        val = self.cleaned_data.get('attributes')
        if not val or val == '{}':
            return {}
        if isinstance(val, dict):
            return val
        import json
        try:
            return json.loads(val)
        except (json.JSONDecodeError, TypeError):
            return {}

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['name', 'category', 'price', 'is_in_stock', 'is_featured', 'is_active']
    list_filter = ['category', 'is_in_stock', 'is_featured', 'gender']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ['category']

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Review)
admin.site.register(Color)
