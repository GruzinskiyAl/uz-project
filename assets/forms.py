from django import forms
from assets.models import Asset


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ('asset_type', 'name', 'years_to_use', 'info')
