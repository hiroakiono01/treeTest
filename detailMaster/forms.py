from django import forms
from django.forms import ModelForm

from app.models import DetailMaster, Calc_clas_select


class DetailMasterForm(ModelForm):
    """項目マスタのフォーム"""
    # 必須項目の表示
    required_css_class = 'required'

    detail_name = forms.CharField(required=True, label='項目名称:')
    # calcu_cls = forms.CharField(required=True, label='計算区分:')
    calcu_cls = forms.ChoiceField(choices=Calc_clas_select, required=True,label="")

    class Meta:
        model = DetailMaster

        fields = ('detail_name', 'calcu_cls', 'unit_name', 'budget_price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
