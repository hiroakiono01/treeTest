import openpyxl

from api.views import get_unit_pk, get_user_pk
from app.models import Estimate, Task
from datetime import datetime
estimate_obj = {}
task_obj = {}


def upload_excel_estimate(excel_file, form):
    wb = openpyxl.load_workbook(excel_file)
    # sheet = wb["1-吹上ＤＭ外壁その他大規模修繕工事"]

    for i, worksheet in enumerate(wb.worksheets):
        if i == 0:
            # 1枚目のシート（インデックス 0）の処理
            first_sheet(worksheet, form)
        else:
            # 2枚目以降のシートの処理
            after_sheet(worksheet, form)


def first_sheet(worksheet, form):
    # --- Estimate情報 ---
    # Formから取得
    client = form.cleaned_data['client_pk']
    estimate_obj["client"] = client

    # Formから取得
    fiscalyear = form.cleaned_data['fiscalyear']
    estimate_obj["fiscalyear"] = fiscalyear.pk

    estimate_date = worksheet['AA7'].value
    formatted_date = estimate_date.strftime("%Y年%m月%d日")
    estimate_obj["estimate_date"] = formatted_date

    estimate_print_date = worksheet['AA7'].value
    formatted_date = estimate_print_date.strftime("%Y年%m月%d日")
    estimate_obj["estimate_print_date"] = formatted_date

    # Formから取得
    estimate_no = form.cleaned_data['estimate_no']
    estimate_obj["estimate_no"] = estimate_no

    # estimate_branch_no 取れない
    orderer_name1 = worksheet['AN9'].value
    estimate_obj["orderer_name1"] = orderer_name1

    orderer_name2 = worksheet['AO9'].value
    estimate_obj["orderer_name2"] = orderer_name2

    # estimate_branch_no 取れない
    # orderer_representative 取れない
    # orderer_person 取れない
    estimate_amount = worksheet['F9'].value
    estimate_obj["estimate_amount"] = estimate_amount

    # estimate_obj["estimate_tax_amount"] = estimate_tax_amount

    # estimate_tax_amount　明細を先に読んで消費税の金額をセットする
    consumption_cls = worksheet['AN5'].value
    estimate_obj["consumption_cls"] = consumption_cls

    estimate_name = worksheet['F12'].value
    estimate_obj["estimate_name"] = estimate_name

    # estimate_branch_name 取れない
    # contract_zip_code 取れない
    contract_address1 = worksheet['AN11'].value
    estimate_obj["contract_address1"] = contract_address1

    contract_address2 = worksheet['AO11'].value
    estimate_obj["contract_address2"] = contract_address2

    contract_address3 = worksheet['AP11'].value
    estimate_obj["contract_address3"] = contract_address3

    estimate_limit_date = worksheet['F16'].value
    estimate_obj["estimate_limit_date"] = estimate_limit_date

    payment_term = worksheet['F18'].value
    estimate_obj["payment_term"] = payment_term

    # estimate_start_date 取れない
    estimate_end_date = worksheet['F20'].value
    estimate_obj["estimate_end_date"] = estimate_end_date

    delivery_location = worksheet['F22'].value
    estimate_obj["delivery_location"] = delivery_location
    # summary 取れない
    # estimate_budget 取れない
    # estimate_profit 取れない
    # consumption_rate 取れない
    # markup_rate 取れない
    # estimate_cls 取れない
    # construction 取れない
    # estimate_status 取れない
    # segment 取れない
    estimate_person_name = worksheet['V16'].value
    clientPk = form.cleaned_data['client_pk']
    estimate_personPk = get_user_pk(clientPk, estimate_person_name)
    estimate_obj["estimate_person"] = estimate_personPk

    # customer Formから
    customer = form.cleaned_data['customer']
    estimate_obj["customer"] = customer.pk

    estimate_new_id = write_estimate(estimate_obj)

    row_counter = worksheet.max_row

    for i in range(row_counter - 26):
        task_obj["estimate_id"] = estimate_new_id

        material_dimensions = worksheet.cell(row=i + 27, column=10).value
        if material_dimensions is None:
            material_dimensions = ""
        task_obj["material_dimensions"] = material_dimensions

        quantity = worksheet.cell(row=i + 27, column=17).value
        if quantity is None:
            quantity = None
        task_obj["quantity"] = quantity

        unit_name = worksheet.cell(row=i + 27, column=20).value
        clientPk = form.cleaned_data['client_pk']
        unitPk = get_unit_pk(clientPk, unit_name)
        task_obj["unit"] = unitPk

        price = worksheet.cell(row=i + 27, column=22).value
        if price is None:
            price = None
        task_obj["price"] = price

        amount = worksheet.cell(row=i + 27, column=26).value
        if amount is None:
            amount = None
        task_obj["amount"] = amount

        note = worksheet.cell(row=i + 27, column=30).value
        if note is None:
            note = ""
        task_obj["note"] = note

        aggregation = worksheet.cell(row=i + 27, column=36).value
        if aggregation is None:
            aggregation = ""
        task_obj["aggregation"] = aggregation

        task_name = worksheet.cell(row=i + 27, column=2).value
        if task_name == '消費税':
            estimate_tax_amount = amount
        if task_name is None:
            task_name = ""
        task_obj["task_name"] = task_name

        write_task(task_obj)
        # print(task_name, material_dimensions, quantity, unit, price, amount, note, aggregation)


def write_estimate(estimate_obj):
    estimate = Estimate(
        client_id=estimate_obj["client"],
        fiscalyear_id=estimate_obj["fiscalyear"],
        estimate_date=estimate_obj["estimate_date"],
        estimate_print_date=estimate_obj["estimate_print_date"],
        estimate_no=estimate_obj["estimate_no"],
        orderer_name1=estimate_obj["orderer_name1"],
        orderer_name2=estimate_obj["orderer_name2"],
        estimate_amount=estimate_obj["estimate_amount"],
        # estimate_tax_amount=estimate_obj["estimate_tax_amount"],
        consumption_cls=estimate_obj["consumption_cls"],
        estimate_name=estimate_obj["estimate_name"],
        contract_address1=estimate_obj["contract_address1"],
        contract_address2=estimate_obj["contract_address2"],
        estimate_limit_date=estimate_obj["estimate_limit_date"],
        payment_term=estimate_obj["payment_term"],
        estimate_end_date=estimate_obj["estimate_end_date"],
        delivery_location=estimate_obj["delivery_location"],
        # estimate_person=estimate_obj["estimate_person"],
        customer_id=estimate_obj["customer"],

    )
    estimate.save()

    return estimate.id


def write_task(task_obj):
    Task(
        estimate_id=task_obj["estimate_id"],
        task_name=task_obj["task_name"],
        material_dimensions=task_obj["material_dimensions"],
        # budget_quantity=task_obj["budget_quantity"],
        # budget_unit=task_obj["budget_unit"],
        # budget_name=task_obj["budget_name"],
        # budget_amount=task_obj["budget_amount"],
        # quantity=task_obj["quantity"],
        # unit=task_obj["unit"],
        # price=task_obj["price"],
        amount=task_obj["amount"],
        # markup_rate=task_obj["markup_rate"],
        # aggregation=task_obj["aggregation"],
        note=task_obj["note"],
        # parent=task_obj["parent"],
        # sort_order=task_obj["sort_order"],
    ).save()


def after_sheet(worksheet, form):
    row_counter = worksheet.max_row
    for i in range(row_counter - 3):

        task_name = worksheet.cell(row=i + 4, column=2).value
        if task_name is None:
            task_name = ""

        material_dimensions = worksheet.cell(row=i + 4, column=3).value
        if material_dimensions is None:
            material_dimensions = ""

        quantity = worksheet.cell(row=i + 4, column=4).value
        if quantity is None:
            quantity = ""

        unit = worksheet.cell(row=i + 4, column=5).value
        if unit is None:
            unit = ""

        price = worksheet.cell(row=i + 4, column=6).value
        if price is None:
            price = ""

        amount = worksheet.cell(row=i + 4, column=7).value
        if amount is None:
            amount = ""

        note = worksheet.cell(row=i + 4, column=8).value
        if note is None:
            note = ""

        aggregation = worksheet.cell(row=i + 4, column=10).value
        if aggregation is None:
            aggregation = ""

        print(task_name, material_dimensions, quantity, unit, price, amount, note, aggregation)
