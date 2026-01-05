# coding: utf-8

from rest_framework import serializers

from app.models import Estimate


class EstimateSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    estimate_no = serializers.CharField(required=True)
    estimate_name = serializers.CharField(required=True)

    class Meta:
        model = Estimate
        fields = ('id', 'estimate_no', 'estimate_name',)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if 'estimate_name' not in validated_data:
            validated_data['estimate_name'] = instance.estimate_name

        instance.save()
        return instance

# class EstimateDSerializer(serializers.ModelSerializer):
#     class Meta:
#         id = serializers.IntegerField(required=False)
#         estimate_no = serializers.CharField(required=True)
#         detail_name = serializers.CharField(required=True)
#         model = EstimateD
#         fields = ('id', 'estimate_no', 'seq_no', 'detail_name',
#                   'budget_quantity', 'budget_unit',
#                   'budget_price', 'budget_amount')
#
#     def update(self, instance, validated_data):
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#
#         if 'name' not in validated_data:
#             validated_data['detail_name'] = instance.detail_name
#
#         instance.save()
#         return instance
