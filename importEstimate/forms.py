import os

from django import forms

from app.models import Estimate, Fiscalyear, Customer

VALID_EXTENSIONS_excel = ['.xlsx']


class ImportEstimateForm(forms.Form):
    client_name = forms.CharField(label='事業者名')
    client_pk = forms.IntegerField(label="事業者PK")
    fiscalyear = forms.ModelChoiceField(label="年度", queryset=Fiscalyear.objects.order_by("-fiscalyear_no").all())
    estimate_no = forms.CharField(label='見積書番号', max_length=8, required=True)
    customer = forms.ModelChoiceField(label="得意先", queryset=None, required=True)

    #
    def clean_estimate_no(self):
        estimate_no = self.cleaned_data.get('estimate_no')

        # 対策2：値が存在し、かつ型が文字列であることを確認してチェックする
        if estimate_no:
            # 念のため文字列型にキャスト（変換）してから isdigit() を呼ぶと絶対にエラーになりません
            estimate_no_str = str(estimate_no)

            if not estimate_no_str.isdigit():
                raise forms.ValidationError("見積書番号は半角数字のみで入力してください。")

            # if len(estimate_no_str) != 8:
            #     raise forms.ValidationError("見積もり番号は8桁で入力してください。")

        # 重複チェック
        estimate = Estimate.objects.filter(estimate_no=estimate_no).all()
        if len(estimate) > 0:
            raise forms.ValidationError("この見積書番号はすでに登録されています。")

        return estimate_no

    file = forms.FileField(label='見積書のExcel')

    def clean_file(self):
        file = self.cleaned_data['file']
        extension = os.path.splitext(file.name)[1]  # 拡張子を取得
        if not extension.lower() in VALID_EXTENSIONS_excel:
            raise forms.ValidationError('xlsxファイルを選択してください！')

    def __init__(self, queryset=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client_name'].widget.attrs['readonly'] = True

        client_pk = self.initial.get('client_pk')

        if client_pk:
            self.fields['customer'].queryset = Customer.objects.filter(
                client_id=client_pk)

        # # フォームのパーツにBootstrapの見た目と、検索用クラスを追加します
        # for field_name in ['client_name', 'fiscalyear', 'customer']:
        #     self.fields[field_name].widget.attrs.update({
        #         'class': 'form-control searchable-select'  # searchable-select クラスを付与
        #     })
