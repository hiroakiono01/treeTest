import os

from django import forms

from app.models import Estimate, Client


VALID_EXTENSIONS_csv = ['.xls', ]


class ImportEstimateForm(forms.Form):
    q_client_id = forms.ModelChoiceField(Client.objects.all(),
                                         label='事業者',
                                         required=False)


    file = forms.FileField(label='索引ファイルを選択してください')



    def clean_file(self):
        file = self.cleaned_data['file']
        extension = os.path.splitext(file.name)[1]  # 拡張子を取得
        if not extension.lower() in VALID_EXTENSIONS_csv:
            raise forms.ValidationError('csvファイルを選択してください！')

    def __init__(self, queryset=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q_client_id'].widget = forms.HiddenInput()
