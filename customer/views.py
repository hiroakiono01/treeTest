import csv
import io

from django.db import models
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import CustomerSerializer
from app.models import Customer


def customer_list_call(request):
    return render(request, 'customer_list.html')


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def customer_list(request, client_id):
    if request.method == 'GET':
        customers = Customer.objects.order_by("customer_no").filter(client_id=client_id).all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        # 1. リクエストデータに client_id を強制的に含める（必要な場合）
        data = request.data.copy()
        # 2. customer_no の重複チェック（null や空文字は除外）
        customer_no = data.get('customer_no')

        if customer_no:
            exists = Customer.objects.filter(client_id=client_id, customer_no=customer_no).exists()
            if exists:
                return Response(
                    {"customer_no": ["この得意先管理番号は既に登録されています。"]},
                    status=status.HTTP_400_BAD_REQUEST
                )
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def customer_detail(request, pk):
    # 💡 見つからない場合は自動的に 404 エラー（APIException）を返してくれる
    instance = get_object_or_404(Customer, pk=pk)

    if request.method == "DELETE":
        # 1. 削除（DELETE）処理の共通化
        try:
            instance.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except models.ProtectedError:
            msg = f'「{instance.customer_name}」は他で使用されているため削除できません。'
            return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)

    # 2. 更新（PUT/PATCH）時の重複チェック
    customer_no = request.data.get('customer_no')
    # PATCHの場合、リクエストに含まれていない場合は現在のインスタンスの値を使用
    if request.method == "PATCH" and 'customer_no' not in request.data:
        customer_no = instance.customer_no

    if customer_no:  # 空文字やNoneでなければチェック
        # 自分自身(pk=pk)を除外し、同じ client_id 内で重複がないか確認
        exists = Customer.objects.filter(
            client_id=instance.client,
            customer_no=customer_no
        ).exclude(pk=pk).exists()

        if exists:
            return Response(
                {"customer_no": ["この得意先管理番号は既に他の得意先に登録されています。"]},
                status=status.HTTP_400_BAD_REQUEST
            )

    serializer = CustomerSerializer(instance, data=request.data, partial=(request.method == "PATCH"))

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        # バリデーションエラー時はシリアライザのエラーをそのまま返す
        # これによりJSの .catch(err => { ... }) で項目ごとにエラー表示が可能
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def customer_import(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        # ファイルオブジェクトをテキストモードに変換（UTF-8）
        # Excelで作成したCSVの場合は 'shift_jis' や 'cp932' を指定
        data_set = csv_file.read().decode("cp932")
        io_string = io.StringIO(data_set)

        # CSVを1行ずつループ処理
        reader = csv.reader(io_string, delimiter=",")

        # 1行目がヘッダー（列名）の場合は next() でスキップ可能
        # header = next(reader)

        for row in reader:
            # rowは配列です。例：['田中', '30', '東京都']
            print(row)
            add_customer_db(row)

            # ここでデータベースに保存する処理（モデルの作成など）を行う
            # MyModel.objects.create(name=row[0], age=row[1], city=row[2])

        return render(request, "complete.html")

    return render(request, "importCustomer.html")


def add_customer_db(row):
    if row[13] == "当月":
        payment_sight = "0"
    elif row[13] == "翌月":
        payment_sight = "1"
    elif row[13] == "翌々月":
        payment_sight = "2"
    else:
        payment_sight = ""
    Customer(
        client_id=1,
        customer_no=row[1],
        customer_name=row[4],
        customer_zip_code=row[5],
        customer_address1=row[6],
        customer_address2=row[7],
        customer_phone_no=row[8],
        customer_fax_no=row[9],
        customer_person=row[10],
        payment_close_date=row[11],
        payment_limit_date=row[12],
        payment_sight=payment_sight,
        payment_payday=row[14]
    ).save()
