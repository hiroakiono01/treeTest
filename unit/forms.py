from django import forms
from django.forms import ModelForm

from app.models import Unit

from django import forms
from app.models import Unit  # 実際のモデル名に合わせて変更してください


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        # フォームで扱うフィールドを指定
        fields = ['unit_no', 'unit_name']

        # ユーザーに表示するエラーメッセージのカスタマイズ
        error_messages = {
            'unit_no': {
                'unique': "この Unit No は既に登録されています。別の番号を入力してください。",
                'invalid': "有効な数値を入力してください。",
            },
            'unit_name': {
                'invalid': "必須の入力項目です。5555"
            }
        }

    def clean_unit_no(self):
        """
        特定の数値を除外したい、あるいは追加の論理チェックが必要な場合は
        ここにバリデーションロジックを書けます（任意）。
        """
        unit_no = self.cleaned_data.get('unit_no')

        # 例: 負の数は許可しない場合
        if unit_no is None or unit_no < 0:
            raise forms.ValidationError("Unit No に整数を設定してください。")

        return unit_no

    def clean_unit_name(self):
        unit_name = self.cleaned_data.get('unit_name')
        if unit_name is None:
            raise forms.ValidationError("Unit Name は必須項目です。ttt")

        return unit_name


# class UnitForm(ModelForm):
#     """ユニットのフォーム"""
#     # 必須項目の表示
#     required_css_class = 'required'
#
#     unit_no = forms.CharField(required=True, label='ユニット番号:')
#     unit_name = forms.CharField(required=True, label='ユニット名称:')
#
#     class Meta:
#         model = Unit
#
#         fields = ('unit_no', 'unit_name',)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
