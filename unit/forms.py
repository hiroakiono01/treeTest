from django import forms
from django.forms import ModelForm

from app.models import Unit


class UnitForm(ModelForm):
    """ユニットのフォーム"""
    # 必須項目の表示
    required_css_class = 'required'

    unit_no = forms.CharField(required=True, label='ユニット番号:')
    unit_name = forms.CharField(required=True, label='ユニット名称:')

    class Meta:
        model = Unit

        fields = ('unit_no', 'unit_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
