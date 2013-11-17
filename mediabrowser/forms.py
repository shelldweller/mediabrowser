from django import forms

from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ("file",)
