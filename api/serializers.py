# coding: utf-8

from rest_framework import serializers

from app.models import Task, Estimate, Unit, Reference


class UnitSerializer(serializers.ModelSerializer):
    # id = serializers.CharField(required=False, allow_blank=True)
    # unit_no = serializers.CharField(required=True)
    unit_name = serializers.CharField(required=True)

    class Meta:
        model = Unit
        fields = ('id', 'unit_no', 'unit_name')
        extra_kwargs = {
            'unit_no': {
                'error_messages': {
                    'unique': "この Unit No は既に登録されています。別の番号を入力してください。",
                    'invalid': "有効な数値を入力してください。",
                }
            },
            'unit_name': {
                'error_messages': {
                    'required': "必須の入力項目です。5555",
                    # 'blank': "空欄にはできません。",
                }
            }
        }


class ReferenceSerializer(serializers.ModelSerializer):
    unit_name_display = serializers.ReadOnlyField(source='unit_name.unit_name')
    detail_name = serializers.CharField(required=True)
    calcu_cls = serializers.CharField(required=True)

    class Meta:
        model = Reference
        fields = ('id',
                  'detail_name',
                  'calcu_cls',
                  'unit_name',
                  'unit_name_display',
                  'budget_price',
                  )


class EstimateSerializer(serializers.ModelSerializer):
    estimate_year = serializers.CharField(required=True)
    estimate_no = serializers.CharField(required=True)
    estimate_name = serializers.CharField(required=True)

    class Meta:
        model = Estimate
        fields = ('id', 'estimate_year', 'estimate_no', 'estimate_name',)
        extra_kwargs = {
            'estimate_no': {
                'error_messages': {
                    'unique': "この Unit No は既に登録されています。別の番号を入力してください。",
                    'invalid': "有効な数値を入力してください。",
                }
            },
            'estimate_name': {
                'error_messages': {
                    'required': "必須の入力項目です。5555",
                    # 'blank': "空欄にはできません。",
                }
            }
        }


class TaskSerializer(serializers.ModelSerializer):
    unit_display = serializers.ReadOnlyField(source='unit.unit_name')
    budget_unit_display = serializers.ReadOnlyField(source='budget_unit.unit_name')
    estimate_no_display = serializers.ReadOnlyField(source='estimate_no.estimate_name')

    # task_name = serializers.CharField(required=True)

    class Meta:
        model = Task

        fields = ('id', 'estimate_no',
                  'estimate_no_display',
                  'task_name',
                  'material_dimensions',
                  'budget_quantity', 'budget_unit',
                  'budget_unit_display',
                  'budget_price', 'budget_amount',
                  'quantity', 'unit',
                  'unit_display',
                  'price', 'amount',
                  'markup_rate', 'calcu_cls',
                  'parent', 'sort_order',
                  )
