from django.db import models
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views import generic
from api.serializers import CustomerSerializer
from app.models import Customer

import csv
import io
from django.shortcuts import render


def customer_list_call(request):
    return render(request, 'customer_list.html')


@api_view(['GET', 'POST'])
def customer_list(request, client_id):
    if request.method == 'GET':
        customers = Customer.objects.order_by("customer_no").filter(client_id=client_id).all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "PATCH", "DELETE"])
def customer_detail(request, pk):
    try:
        instance = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({"detail": "対象が見つかりません"}, status=status.HTTP_404_NOT_FOUND)

    # 1. 削除（DELETE）処理の共通化
    if request.method == "DELETE":
        try:
            instance.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except models.ProtectedError:
            msg = f'「{instance}」は他で使用されているため削除できません。'
            return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)

    # if request.method == "GET":
    #     serializer = CustomerSerializer(instance)
    #     return Response(serializer.data)

    serializer = CustomerSerializer(instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        # バリデーションエラー時はシリアライザのエラーをそのまま返す
        # これによりJSの .catch(err => { ... }) で項目ごとにエラー表示が可能
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def bulk_sync_customers(request):
    data_list = request.data
    response_data = []

    try:
        with transaction.atomic():
            # enumerate を使って、データの並び順（0, 1, 2...）を index として取得します
            for index, item in enumerate(data_list):
                raw_id = item.get('id')
                # 元のデータを汚さないようにコピー
                save_data = item.copy()

                if isinstance(raw_id, str) and raw_id.startswith('u'):
                    # 1. シリアライザのバリデーションを通すため、save_data から 'id' キーごと完全に削除する
                    save_data.pop('id', None)

                    # 2. シリアライザに余計なフィールドを渡さない（エラー防止）
                    serializer = CustomerSerializer(data=save_data)
                    instance_exists = False
                else:
                    # 💡 既存データの更新
                    instance = Customer.objects.filter(id=raw_id).first()
                    if not instance:
                        raise ValueError({'error': f'{index + 1}件目のデータ（ID: {raw_id}）がデータベースに存在しません。'})

                    serializer = CustomerSerializer(instance, data=save_data, partial=True)

                    instance_exists = True

                if serializer.is_valid():
                    saved_instance = serializer.save()
                    # 保存後のオブジェクトから、正式に出力用データを生成
                    result_item = CustomerSerializer(saved_instance).data
                    # マッピングの記録（後続の子要素のため）
                    if not instance_exists:
                        result_item['customer_id'] = raw_id

                    response_data.append(serializer.data)
                else:
                    error_message = {
                        'error': f'{index + 1}件目のデータ（送信ID: {raw_id}）のバリデーションに失敗しました。',
                        'details': serializer.errors
                    }
                    raise ValueError(error_message)

        return Response({
            'status': 'success',
            'data': response_data
        }, status=status.HTTP_200_OK)

    except ValueError as e:
        # 発生したエラーメッセージの辞書をそのまま400エラーとして返す
        return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)

    # @api_view(['POST'])
    # def bulk_sync_references(request):
    #     data_list = request.data
    #     response_data = []
    #     id_map = {}
    #
    #     # enumerate を使って、データの並び順（0, 1, 2...）を index として取得します
    #     for index, item in enumerate(data_list):
    #         temp_id = item.get('id')
    #         parent_val = item.get('parent')
    #         item['sort_order'] = index
    #
    #         is_temp_id = (
    #                 temp_id is None or
    #                 temp_id == "" or
    #                 (isinstance(temp_id, str) and temp_id.startswith('u'))
    #         )
    #         instance = None
    #         if not is_temp_id:
    #             # 既存データをDBから探す（エラーにならないように filter().first() を使用）
    #             instance = Reference.objects.filter(id=temp_id).first()
    #
    #         if instance:
    #             # 【更新】DBに存在する場合
    #             serializer = ReferenceSerializer(instance, data=item, partial=True)
    #         else:
    #             # 【新規】DBに存在しない、または一時IDの場合
    #             item.pop('id', None)  # IDを削除して新規作成として扱う
    #             serializer = ReferenceSerializer(data=item)
    #
    #         if serializer.is_valid():
    #             saved_instance = serializer.save()
    #
    #             # マッピングの記録（後続の子要素のため）
    #             if is_temp_id or not instance:
    #                 id_map[temp_id] = saved_instance.id
    #
    #             response_data.append(serializer.data)
    #         else:
    #             print(f"Serializer Error: {serializer.errors}")  # デバッグ用
    #             return Response(serializer.errors, status=400)
    #
    #     return Response(response_data, status=200)


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
