from django.db import models

from accounts.models import CustomUser

Calc_clas_select = [
    ('0', 'Items to include in The total　amount'),
    ('1', 'Aggregate within the hierarchy but do not include in The total amount'),
    ('2', 'The total amount excluding consumption tax'),
    ('3', 'Consumption tax'),
]
clientFlgData = [
    ('0', "既契約先"),
    ('1', "未契約先"),
]
clientFlgSelect = [
    ('', '-------'),
    ('0', "既契約先"),
    ('1', "未契約先"),
]
dirData = [
    ('殿', '殿'),
    ('御中', '御中'),
    ('様', '様'),
]
groupClsData = [
    ('1', '官庁'),
    ('2', '民間'),
]

salesFlgData = [
    ('0', "訪問済"),
    ('1', "未訪問"),
]
salesFlgSelect = [
    ('', '-------'),
    ('0', "訪問済"),
    ('1', "未訪問"),
]
sight = [
    ('', '-----'),
    ('0', '当月'),
    ('1', '翌月'),
    ('2', '翌々月'),
]
payday = [
    ('', '------'),
    ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'),
    ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'),
    ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('31', '月末'),

]
useFlgData = [
    ('0', '使用する'),
    ('9', '使用しない')
]
useFlgSelect = [
    ('', '--------'),
    ('0', '利用中'),
    ('9', '停止'),
]

userFlgData = [
    ('', '-------'),
    ('0', '対象者')
]

ecoDocuments_client_select = [
    ('', '-------'),
    ('1', '利用する'),
    ('2', '利用しない'),
    ('9', '中止する')
]

ecoEstimate_client_select = [
    ('', '-------'),
    ('1', '利用する'),
    ('2', '利用しない'),
    ('9', '中止する')
]

ecoContract_client_select = [
    ('', '-------'),
    ('1', '利用する'),
    ('2', '利用しない'),
    ('9', '中止する')
]

client_cls_select = [
    ('', '-------'),
    ('1', '法人'),
    ('2', '個人'),
]
fiscalYearFlg_Select = [
    ('0', '期首の年で表示する'),
    ('1', '期末の年で表示する'),
]

fiscalMonthFlg_Select = [
    ('0', '月初の月で表示する'),
    ('1', '月末の月で表示する'),
]

documents_manager_select = [
    ('', '一般ユーザー'),
    ('1', 'システム管理者'),
]

estimate_manager_select = [
    ('', '一般ユーザー'),
    ('1', 'システム管理者'),
]

contract_manager_select = [
    ('', '一般ユーザー'),
    ('1', 'システム管理者'),
]


class Client(models.Model):
    class Meta:
        db_table = 'client'

    id = models.AutoField(primary_key=True)
    client_no = models.CharField(max_length=10, null=True, blank=True, verbose_name='事業者番号')
    client_name = models.CharField(max_length=40, null=True, blank=True, verbose_name='事業者名称')
    client_name_kana = models.CharField(max_length=40, null=True, blank=True, verbose_name='事業者名称カナ')
    client_rep_name = models.CharField(max_length=40, null=True, blank=True, verbose_name='代表者名称')
    client_cls = models.CharField(max_length=1, null=True, blank=True, verbose_name='事業者区分')
    client_zip_code = models.CharField(max_length=8, null=True, blank=True, verbose_name='郵便番号')
    client_address1 = models.CharField(max_length=60, null=True, blank=True, verbose_name='住所１')
    client_address2 = models.CharField(max_length=60, null=True, blank=True, verbose_name='住所２')
    client_phone_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='電話番号')
    client_fax_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='FAX')
    storage_volume = models.FloatField(null=True, blank=True, verbose_name='M容量')

    ecoDocuments_client_flg = models.CharField(max_length=1, null=True, blank=True, verbose_name='なんでも書庫使用区分')
    ecoEstimate_client_flg = models.CharField(max_length=1, null=True, blank=True, verbose_name='eco見積使用区分')
    ecoContract_client_flg = models.CharField(max_length=1, null=True, blank=True, verbose_name='eco受注使用区分')

    fiscalYear = models.CharField(max_length=4, null=True, blank=True, verbose_name='会計年度')
    fiscalYearFlg = models.CharField(max_length=1, null=True, blank=True, verbose_name='会計年度表示区分')
    fiscalYearFrom = models.CharField(max_length=10, null=True, blank=True, verbose_name='事業年度開始日')
    fiscalMonthFlg = models.CharField(max_length=10, null=True, blank=True, verbose_name='月度表示区分')

    create_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='作成者')
    update_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='更新者')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return self.client_name or "名称未設定"

    def get_client_cls_cha(self) -> str:
        if self.client_cls == '0':
            return "法人"
        if self.client_cls == '9':
            return "個人"

    def get_fiscal_year_cha(self) -> str:
        if self.fiscalYearFlg == '0':
            return "期首の年を表示"
        if self.fiscalYearFlg == '1':
            return "期末の年を表示"

    def get_fiscal_month_cha(self) -> str:
        if self.fiscalMonthFlg == '0':
            return "月初の月で表示"
        if self.fiscalMonthFlg == '1':
            return "月末の月で表示"

    def get_documents_client_cha(self) -> str:
        if self.ecoDocuments_client_flg == '1':
            return "利用する"
        if self.ecoDocuments_client_flg == '2':
            return "利用しない"
        if self.ecoDocuments_client_flg == '9':
            return "中止する"

    def get_estimate_client_cha(self) -> str:
        if self.ecoEstimate_client_flg == '1':
            return "利用する"
        if self.ecoEstimate_client_flg == '2':
            return "利用しない"
        if self.ecoEstimate_client_flg == '9':
            return "中止する"

    def get_contract_client_cha(self) -> str:
        if self.ecoContract_client_flg == '1':
            return "利用する"
        if self.ecoContract_client_flg == '2':
            return "利用しない"
        if self.ecoContract_client_flg == '9':
            return "中止する"

    def get_client_cls_cha(self) -> str:
        if self.client_cls == '1':
            return "法人"
        if self.client_cls == '2':
            return "個人"


class CurrentClient(models.Model):
    class Meta:
        db_table = 'currentClient'

    customUser = models.ForeignKey(CustomUser, null=True, blank=True, verbose_name='利用者', on_delete=models.PROTECT)
    client = models.ForeignKey(Client, null=True, blank=True, verbose_name='顧問先', on_delete=models.PROTECT)

    def __str__(self):
        return self.customUser.username + '  :' + self.client.client_name


class Fiscalyear(models.Model):
    class Meta:
        db_table = 'fiscalyear'

    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, null=True, blank=True, verbose_name='事業者', on_delete=models.PROTECT)
    fiscalyear_no = models.CharField(max_length=8, null=True, blank=True, verbose_name='部門コード')
    fiscalyear_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='部門名称')
    current_flg = models.CharField(max_length=1, null=True, blank=True, verbose_name='当年度フラグ', default="0")

    create_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='作成者')
    update_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='更新者')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return str(self.fiscalyear_name)


class Segment(models.Model):
    class Meta:
        db_table = 'segment'

    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, null=True, blank=True, verbose_name='事業者', on_delete=models.PROTECT)
    segment_no = models.CharField(max_length=8, null=True, blank=True, verbose_name='部門コード')
    segment_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='部門名称')
    use_flg = models.CharField(max_length=1, null=True, blank=True, verbose_name='利用状況', choices=useFlgData, default="0")

    create_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='作成者')
    update_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='更新者')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)


class Construction(models.Model):
    class Meta:
        db_table = 'construction'

    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, null=True, blank=True, verbose_name='事業者', on_delete=models.PROTECT)
    construction_no = models.CharField(max_length=2, null=True, blank=True, verbose_name='工事区分番号')
    construction_name = models.CharField(max_length=10, null=True, blank=True, verbose_name='工事区分名称')

    create_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='作成者')
    update_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='更新者')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)


class User(models.Model):
    class Meta:
        db_table = 'user'

    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, null=True, blank=True, verbose_name='事業者', on_delete=models.PROTECT)
    user_no = models.CharField(max_length=8, null=True, blank=True, verbose_name='担当者番号')
    user_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='担当者名称')
    user_short_name = models.CharField(max_length=5, null=True, blank=True, verbose_name='担当者略称')
    use_flg = models.CharField(max_length=1, null=True, blank=True, verbose_name='利用状況', choices=useFlgData, default="0")
    salesman_flg = models.CharField(max_length=1, null=True, blank=True, verbose_name='営業職')
    manager_flg = models.CharField(max_length=1, null=True, blank=True, verbose_name='現場管理職')

    create_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='作成者')
    update_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='更新者')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def get_use_flg_cha(self) -> str:
        if self.use_flg == '0':
            return "利用中"
        if self.use_flg == '9':
            return "停止"

    def __str__(self):
        return self.user_no + " " + self.user_name


# class Group(models.Model):
#     class Meta:
#         db_table = 'groups'
#
#     client = models.ForeignKey(Client, null=True, blank=True, verbose_name='事業者', on_delete=models.PROTECT)
#     group_code = models.CharField(max_length=4, null=True, blank=True, verbose_name='グループコード', unique=True)
#     group_cls = models.CharField(max_length=1, null=True, blank=True, choices=groupClsData, verbose_name='グループクラス')
#     group_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='グループ名称')
#
#     create_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='作成者')
#     update_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='更新者')
#     created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
#     updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)


class Customer(models.Model):
    class Meta:
        db_table = 'customer'

    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, null=True, blank=True, verbose_name='事業者', on_delete=models.PROTECT)
    customer_no = models.CharField(max_length=13, null=True, blank=True, verbose_name='得意先管理番号')
    customer_name = models.CharField(max_length=60, null=True, blank=True, verbose_name='得意先名称')
    customer_short_name = models.CharField(max_length=14, null=True, blank=True, verbose_name='得意先略称')
    customer_kana = models.CharField(max_length=14, null=True, blank=True, verbose_name='得意先カナ')
    customer_zip_code = models.CharField(max_length=8, null=True, blank=True, verbose_name='郵便番号')
    customer_address1 = models.CharField(max_length=60, null=True, blank=True, verbose_name='住所１')
    customer_address2 = models.CharField(max_length=60, null=True, blank=True, verbose_name='住所２')
    customer_phone_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='電話番号')
    customer_personal_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='携帯電話番号')
    customer_fax_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='FAX')
    customer_person = models.CharField(max_length=30, null=True, blank=True, verbose_name='担当者名')
    group_cls = models.CharField(max_length=1, null=True, blank=True, verbose_name='グループ')
    payment_close_date = models.CharField(max_length=2, null=True, blank=True, verbose_name='請求締め日')
    payment_sight = models.CharField(max_length=10, null=True, blank=True, verbose_name='請求サイト')
    payment_payday = models.CharField(max_length=2, null=True, blank=True, verbose_name='入金予定日')
    payment_limit_date = models.CharField(max_length=2, null=True, blank=True, verbose_name='請求書提出期限')
    customer_bank = models.CharField(max_length=20, null=True, blank=True, verbose_name='銀行コード')
    customer_branch = models.CharField(max_length=20, null=True, blank=True, verbose_name='支店コード')
    customer_deposit_cls = models.CharField(max_length=1, null=True, blank=True, verbose_name='預金種目')
    customer_bank_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='口座番号')
    customer_bank_holder = models.CharField(max_length=20, null=True, blank=True, verbose_name='名義人名')
    client_flg = models.CharField(max_length=1, null=True, blank=True, verbose_name=' 顧客区分')
    sales_flg = models.CharField(max_length=1, null=True, blank=True, verbose_name='営業対象')
    use_flg = models.CharField(max_length=1, null=True, blank=True, verbose_name='利用状況', choices=useFlgData, default="0")

    create_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='作成者')
    update_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='更新者')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return str(self.customer_no) + " " + self.customer_name

    def get_group_cls_cha(self) -> str:
        if self.group_cls == '1':
            return "官庁"
        if self.group_cls == '2':
            return "民間"

    def get_use_flg_cha(self) -> str:
        if self.use_flg == '0':
            return "利用中"
        if self.use_flg == '9':
            return "停止"

    def get_client_flg_cha(self) -> str:
        if self.client_flg == '0':
            return "既契約先"
        if self.client_flg == '1':
            return "未契約先"

    def get_sales_flg_cha(self) -> str:
        if self.sales_flg == '0':
            return "訪問済"
        if self.sales_flg == '1':
            return "見込"

    def get_payment_sight_cha(self) -> str:
        if self.payment_sight == '0':
            return '当月'
        if self.payment_sight == '1':
            return '翌月'
        if self.payment_sight == '2':
            return '翌々月'

    def get_payment_close_date_cha(self) -> str:
        if self.payment_close_date != "":
            if int(self.payment_close_date) > 27:
                return '月末'
            else:
                return self.payment_close_date
        else:
            return self.payment_close_date

    def get_payment_payday_cha(self) -> str:
        if self.payment_payday != "":
            if int(self.payment_payday) > 27:
                return '月末'
            else:
                return self.payment_payday
        else:
            return self.payment_payday


class Unit(models.Model):
    class Meta:
        db_table = 'unit'

    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, null=True, blank=True, verbose_name='事業者', on_delete=models.PROTECT)
    unit_no = models.IntegerField(null=True, blank=True, verbose_name='unit No', default=0)
    unit_name = models.CharField(max_length=15, null=True, blank=True, verbose_name='unit name')
    use_flg = models.CharField(max_length=1, null=True, blank=True, verbose_name='利用状況', choices=useFlgData, default="0")

    create_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='作成者')
    update_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='更新者')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return str(self.unit_name) + str(self.updated_at)


class Process(models.Model):
    class Meta:
        db_table = 'process'

    id = models.AutoField(primary_key=True)
    process_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='工種名称')
    calcu_cls = models.CharField(max_length=2, null=True, blank=True, verbose_name='計算区分', default='0')
    unit_name = models.ForeignKey(Unit, blank=True, null=True, verbose_name='予算単位', related_name='+', on_delete=models.PROTECT)
    budget_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='予算単価')
    sort_order = models.IntegerField(default=0)

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
        return str(self.calcu_cls) + " " + str(self.processl_name)


class Aggregation(models.Model):
    class Meta:
        db_table = 'aggregation'

    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, null=True, blank=True, verbose_name='事業者', on_delete=models.PROTECT)
    aggregation_no = models.CharField(max_length=2, null=True, blank=True, verbose_name='集計区分番号')
    aggregation_name = models.CharField(max_length=40, null=True, blank=True, verbose_name='集計区分名称')
    calcu_cls = models.CharField(max_length=2, null=True, blank=True, verbose_name='計算区分', default='0')

    create_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='作成者')
    update_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='更新者')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)


class Reference(models.Model):
    class Meta:
        db_table = 'reference'

    id = models.AutoField(primary_key=True)

    detail_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='明細名称')
    calcu_cls = models.CharField(null=True, blank=True, verbose_name='計算区分', default='0')
    unit_name = models.ForeignKey(Unit, blank=True, null=True, verbose_name='予算単位', related_name='+', on_delete=models.PROTECT)
    budget_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='予算単価')
    sort_order = models.IntegerField(default=0)

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
    client = models.ForeignKey(Client, null=True, blank=True, verbose_name='事業者', on_delete=models.PROTECT)
    fiscalyear = models.ForeignKey(Fiscalyear, null=True, blank=True, verbose_name='受注年度', on_delete=models.PROTECT)
    estimate_year = models.CharField(max_length=15, null=True, blank=True, verbose_name='受注年度')
    estimate_date = models.CharField(max_length=10, null=True, blank=True, verbose_name='見積年月日')
    estimate_print_date = models.CharField(max_length=10, null=True, blank=True, verbose_name='見積書作成日')
    estimate_no = models.CharField(max_length=8, null=True, blank=True, verbose_name='見積書番号')
    estimate_branch_no = models.CharField(max_length=3, null=True, blank=True, verbose_name='見積書枝番号')
    orderer_name1 = models.CharField(max_length=60, null=True, blank=True, verbose_name='発注者名上段')
    orderer_name2 = models.CharField(max_length=60, null=True, blank=True, verbose_name='発注者名下段')
    orderer_representative = models.CharField(max_length=30, null=True, blank=True, verbose_name='発注者代表者')
    orderer_person = models.CharField(max_length=30, null=True, blank=True, verbose_name='発注担当者')
    estimate_amount = models.IntegerField(null=True, blank=True, verbose_name='税抜見積金額')
    estimate_tax_amount = models.IntegerField(null=True, blank=True, verbose_name='消費税額')
    consumption_cls = models.CharField(max_length=1, null=True, blank=True, verbose_name='消費税区分')
    estimate_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='工事名称')
    estimate_branch_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='工事枝番名称')
    contract_zip_code = models.CharField(max_length=8, null=True, blank=True, verbose_name='現場郵便番号')
    contract_address1 = models.CharField(max_length=60, null=True, blank=True, verbose_name='現場住所１')
    contract_address2 = models.CharField(max_length=60, null=True, blank=True, verbose_name='現場住所２')
    estimate_limit_date = models.CharField(max_length=10, null=True, blank=True, verbose_name='見積有効期限')
    payment_term = models.CharField(max_length=30, null=True, blank=True, verbose_name='支払条件')
    estimate_start_date = models.CharField(max_length=10, null=True, blank=True, verbose_name='工事開始予定日')
    estimate_end_date = models.CharField(max_length=10, null=True, blank=True, verbose_name='工事完成予定日')
    delivery_location = models.CharField(max_length=60, null=True, blank=True, verbose_name='受渡場所')
    summary = models.CharField(max_length=256, null=True, blank=True, verbose_name='備考')
    estimate_budget = models.IntegerField(null=True, blank=True, verbose_name='実行予算')
    estimate_profit = models.IntegerField(null=True, blank=True, verbose_name='工事利益')
    consumption_rate = models.CharField(max_length=5, null=True, blank=True, verbose_name='消費税率')
    estimate_cls = models.CharField(max_length=1, null=True, blank=True, verbose_name='請負形態区分')
    estimate_status = models.CharField(max_length=1, null=True, blank=True, verbose_name='受注状態区分')
    segment = models.ForeignKey(Segment, null=True, blank=True, verbose_name='部門', on_delete=models.PROTECT)
    estimate_person = models.ForeignKey(User, null=True, blank=True, verbose_name='見積担当者', on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, null=True, blank=True, verbose_name='得意先', on_delete=models.PROTECT)

    create_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='作成者')
    update_user = models.CharField(max_length=150, null=True, blank=True, verbose_name='更新者')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

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
    budget_amount = models.DecimalField(max_digits=14, decimal_places=0, null=True, blank=True, verbose_name='予算金額')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='見積数量')
    unit = models.ForeignKey(Unit, blank=True, null=True, verbose_name='見積単位', related_name='+', on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='見積単価')
    amount = models.DecimalField(max_digits=14, decimal_places=0, null=True, blank=True, verbose_name='見積金額')
    markup_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='掛率')
    calcu_cls = models.CharField(null=True, blank=True, verbose_name='計算区分', default='0')

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    sort_order = models.IntegerField(default=0)

    def __str__(self):
        return str(self.task_name)
