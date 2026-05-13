from django.db import models

Calc_clas_select = [
    ('0', 'Items to include in The total　amount'),
    ('1', 'Aggregate within the hierarchy but do not include in The total amount'),
    ('2', 'The total amount excluding consumption tax'),
    ('3', 'Consumption tax'),
]


class Unit(models.Model):
    class Meta:
        db_table = 'unit'

    id = models.AutoField(primary_key=True)
    unit_no = models.IntegerField(null=True, blank=True, verbose_name='unit No', unique=True)
    unit_name = models.CharField(max_length=15, null=True, blank=True, verbose_name='unit name')
    sort_order = models.IntegerField(default=0)

    def __str__(self):
        return str(self.unit_name)


class Reference(models.Model):
    class Meta:
        db_table = 'reference'

    id = models.AutoField(primary_key=True)
    detail_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='明細名称')
    calcu_cls = models.CharField(null=True, blank=True, verbose_name='計算区分', default='0')
    unit_name = models.ForeignKey(Unit, blank=True, null=True, verbose_name='予算単位', related_name='+', on_delete=models.PROTECT)
    budget_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='予算単価')

    def get_calcu_cls_cha(self) -> str:
        if self.calcu_cls == '0':
            return "Items to include in The total　amount"
        if self.calcu_cls == '1':
            return "Aggregate within the hierarchy but do not include in The total amount"
        if self.calcu_cls == '2':
            return "The total amount excluding consumption tax"
        if self.calcu_cls == '3':
            return "Consumption tax"

    def __str__(self):
        return str(self.calcu_cls) + " " + str(self.detail_name)


# class DetailMaster(models.Model):
#     class Meta:
#         db_table = 'detailMaster'
#
#     detail_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='明細名称')
#     calcu_cls = models.CharField(null=True, blank=True, verbose_name='計算区分')
#     unit_name = models.ForeignKey(Unit, blank=True, null=True, verbose_name='予算単位', related_name='unit1', on_delete=models.PROTECT)
#     budget_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='予算単価')
#
#     def get_calcu_cls_cha(self) -> str:
#         if self.calcu_cls == '':
#             return "Items to include in The total　amount"
#         if self.calcu_cls == '1':
#             return "Aggregate within the hierarchy but do not include in The total amount"
#         if self.calcu_cls == '2':
#             return "tThe total amount excluding consumption tax"
#         if self.calcu_cls == '3':
#             return "Consumption tax"


class Estimate(models.Model):
    class Meta:
        db_table = 'estimate'

    id = models.AutoField(primary_key=True)
    estimate_year = models.CharField(max_length=4, null=True, blank=True, verbose_name='estimate year')
    estimate_no = models.CharField(max_length=15, null=True, blank=True, verbose_name='estimate no')
    estimate_name = models.CharField(max_length=60, null=True, blank=True, verbose_name='estimate name')

    def __str__(self):
        return str(self.estimate_name)


class Task(models.Model):
    class Meta:
        db_table = 'task'

    id = models.AutoField(primary_key=True)
    estimate_no = models.ForeignKey(Estimate, null=True, blank=True, on_delete=models.PROTECT)
    task_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='明細名称')
    material_dimensions = models.CharField(max_length=50, null=True, blank=True, verbose_name='材質・寸法')
    budget_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='予算数量')
    budget_unit = models.ForeignKey(Unit, blank=True, null=True, verbose_name='予算単位', related_name='+', on_delete=models.PROTECT)
    budget_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='予算単価')
    budget_amount = models.IntegerField(null=True, blank=True, verbose_name='予算金額')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='見積数量')
    unit = models.ForeignKey(Unit, blank=True, null=True, verbose_name='見積単位', related_name='+', on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='見積単価')
    amount = models.IntegerField(null=True, blank=True, verbose_name='見積金額')
    markup_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='掛率')
    calcu_cls = models.CharField(null=True, blank=True, verbose_name='計算区分', default='0')

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    sort_order = models.IntegerField(default=0)

    def __str__(self):
        return str(self.task_name)
