from django.db import models
from tree_queries.models import OrderableTreeNode


class Unit(models.Model):
    class Meta:
        db_table = 'unit'

    unit_no = models.IntegerField(null=True, blank=True, verbose_name='unit No')
    unit_name = models.CharField(max_length=15, null=True, blank=True, verbose_name='unit nmae')

    def __str__(self):
        return str(self.unit_name)


class Estimate(models.Model):
    class Meta:
        db_table = 'estimate'

    estimate_no = models.CharField(max_length=15, null=True, blank=True, verbose_name='estimate no')
    estimate_name = models.CharField(max_length=60, null=True, blank=True, verbose_name='estimate name')

    def __str__(self):
        return str(self.estimate_name)


class EstimateD(OrderableTreeNode):
    class Meta:
        db_table = 'estimateD'

    id = models.AutoField(primary_key=True)
    estimate_no = models.ForeignKey(Estimate, null=True, blank=True, on_delete=models.PROTECT)
    detail_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='明細名称')
    budget_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='予算数量')
    budget_unit = models.ForeignKey(Unit, blank=True, null=True, verbose_name='予算単位', related_name='unit1', on_delete=models.PROTECT)
    budget_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='予算単価')
    budget_amount = models.IntegerField(null=True, blank=True, verbose_name='予算金額')

    def __str__(self):
        return str(self.detail_name) + str(self.tree_path)
