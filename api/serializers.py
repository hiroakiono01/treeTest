# coding: utf-8

from rest_framework import serializers

from app.models import EstimateD, Estimate


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


class EstimateDSerializer(serializers.ModelSerializer):
    class Meta:

        model = EstimateD

        fields = ('id', 'estimate_no', 'detail_name',
                  # 'parent',
                  # 'children',
                  # 'position',
                  'budget_quantity', 'budget_unit',
                  'budget_price', 'budget_amount')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return EstimateD.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if 'name' not in validated_data:
            validated_data['detail_name'] = instance.detail_name

        instance.save()
        return instance
