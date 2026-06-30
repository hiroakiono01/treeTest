# coding: utf-8

from rest_framework import serializers

from app.models import Client, Task, Estimate, Unit, Process, Customer, User, Construction, Segment, Aggregation, Fiscalyear


class ClientSerializer(serializers.ModelSerializer):
    # client_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Client
        fields = '__all__'


class FiscalyearSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Fiscalyear
        fields = '__all__'


class SegmentSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Segment
        fields = '__all__'


class AggregationSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Aggregation
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ConstructionSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Construction
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Unit
        fields = '__all__'


class ProcessSerializer(serializers.ModelSerializer):
    unit_name_display = serializers.ReadOnlyField(source='unit_name.unit_name')
    process_name = serializers.CharField(required=True)
    calcu_cls = serializers.CharField(required=True)

    class Meta:
        model = Process
        fields = ('id',
                  'process_name',
                  'calcu_cls',
                  'unit_name',
                  'unit_name_display',
                  'budget_price',
                  'sort_order'
                  )


class EstimateSerializer(serializers.ModelSerializer):
    estimate_year = serializers.CharField(required=True)
    estimate_no = serializers.CharField(required=True)
    estimate_name = serializers.CharField(required=True)
    fiscalyear_display = serializers.ReadOnlyField(source='fiscalyear.fiscalyear_name')
    customer_name_display = serializers.ReadOnlyField(source='customer.customer_name')

    class Meta:
        model = Estimate
        fields = ('id', 'client', 'fiscalyear', 'fiscalyear_display',
                  'estimate_year', 'estimate_date', 'estimate_print_date',
                  'estimate_no', 'estimate_branch_no', 'orderer_name1',
                  'orderer_name2', 'orderer_representative', 'orderer_person',
                  'estimate_amount', 'estimate_tax_amount', 'consumption_cls',
                  'estimate_name', 'estimate_branch_name', 'contract_zip_code',
                  'contract_address1', 'contract_address2', 'estimate_limit_date',
                  'payment_term', 'estimate_start_date', 'estimate_end_date',
                  'delivery_location', 'summary', 'estimate_budget',
                  'estimate_profit', 'consumption_rate', 'markup_rate',
                  'estimate_cls', 'construction', 'estimate_status',
                  'segment', 'estimate_person', 'customer', 'customer_name_display'
                  )
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

    # budget_unit = serializers.SerializerMethodField()
    # unit = serializers.SerializerMethodField()

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

    # def get_budget_unit(self, obj):
    #     # null なら空文字、あれば文字列にして返す
    #     if obj.budget_unit_id is not None:
    #         return str(obj.budget_unit_id)
    #     return ""
    #
    # def get_unit(self, obj):
    #     # null なら空文字、あれば文字列にして返す
    #     if obj.unit_id is not None:
    #         return str(obj.unit_id)
    #     return ""
