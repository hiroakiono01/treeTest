from django import forms

from app.models import Estimate


class EstimateAddForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = '__all__'
