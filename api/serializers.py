# coding: utf-8

from rest_framework import serializers

from app.models import Task, Estimate, Unit, Reference


class UnitSerializer(serializers.ModelSerializer):
    # id = serializers.CharField(required=False, allow_blank=True)
    # unit_no = serializers.CharField(required=True)
    # unit_name = serializers.CharField(required=True)

    class Meta:
        model = Unit
        fields = ('id', 'unit_no', 'unit_name')

    # def create(self, validated_data):
    #     # IDがある場合は更新、ない場合は作成
    #     request = self.context.get('request')
    #     raw_id = request.data.get('id') if request else None
    #
    #     # 数値（または数値文字列）の場合のみ既存データを探す
    #     if raw_id is not None:
    #         # 文字列 '123' も数値 123 も判定できる方法
    #         str_id = str(raw_id)
    #         if str_id.isdigit():
    #             instance = Unit.objects.filter(id=int(str_id)).first()
    #             if instance:
    #                 # 既存データがあれば更新
    #                 return self.update(instance, validated_data)
    #
    #     # IDが「数値ではない文字列（u78787等）」または「存在しないID」の場合は新規作成
    #     # validated_dataからidを除去して、自動採番(AutoField)を確実に動かす
    #     validated_data.pop('id', None)
    #     return super().create(validated_data)


class ReferenceSerializer(serializers.ModelSerializer):
    unit_name_display = serializers.CharField(source='unit_name.unit_name', read_only=True)

    class Meta:
        model = Reference
        fields = ('id',
                  'detail_name',
                  'calcu_cls',
                  'unit_name',
                  'unit_name_display',
                  'budget_price',
                  )


class EstimateSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    estimate_no = serializers.CharField(required=True)
    estimate_name = serializers.CharField(required=True)

    class Meta:
        model = Estimate
        fields = ('id', 'estimate_no', 'estimate_name',)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """

        return Estimate.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        instance.estimate_no = validated_data.get("estimate_no", instance.estimate_no)
        instance.estimate_name = validated_data.get("estimate_name", instance.estimate_name)

        instance.save()
        return instance


class TaskSerializer(serializers.ModelSerializer):
    # parentId = serializers.IntegerField(source='parent')

    class Meta:
        model = Task

        fields = ('id', 'estimate_no', 'task_name',
                  'material_dimensions',
                  'budget_quantity', 'budget_unit',
                  'budget_price', 'budget_amount',
                  'quantity', 'unit',
                  'price', 'amount',
                  'markup_rate', 'calcu_cls',
                  'parent', 'sort_order',
                  )
