from django import forms

from app.models import Estimate, EstimateD


class EstimateAddForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = '__all__'


# class EstimateDForm(forms.ModelForm, forms.Form):
#     # q_client = forms.ModelChoiceField(Client.objects.all(), required=False, label='')
#     # q_estimate = forms.ModelChoiceField(Estimate.objects.all(), required=False, label='')
#     # q_level = forms.CharField(label='level', required=False)
#     # q_parent_id = forms.CharField(label='parent_id', required=False)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.widget.attrs['class'] = 'form-control'
    #
    # class Meta:
    #     model = EstimateD
    #     fields = '__all__'

#
# class EstimateTreeForm(forms.ModelForm, forms.Form):
#     q_client = forms.ModelChoiceField(Client.objects.all())
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
#
#     class Meta:
#         model = EstimateD
#         fields = ('detail_name',)

# これがモデルフォームセット
# EstimateDFormSet = forms.modelformset_factory(
#     EstimateD, form=EstimateDForm, extra=10
# )
