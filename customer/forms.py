import os
from django import forms

VALID_EXTENSIONS_csv = ['.csv', ]


class ImportCustomerForm(forms.Form):
    file = forms.FileField(label='csvファイルを選択してください')

    def clean_file(self):
        file = self.cleaned_data['file']
        extension = os.path.splitext(file.name)[1]  # 拡張子を取得
        if not extension.lower() in VALID_EXTENSIONS_csv:
            raise forms.ValidationError('csvファイルを選択してください！')
