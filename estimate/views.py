import json
import urllib.parse

from django.db import models
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import EstimateSerializer
from app.models import Estimate


def estimate_list_call(request):
    return render(request, 'estimate_list.html')


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def estimate_list(request, client_id, sql):
    # if request.method == 'GET':
    try:
        if sql == "null":
            query = Q(client_id=client_id)
        else:

            # 1. URLパスからオブジェクトを復元
            decoded_sql = urllib.parse.unquote(sql)
            search_condition = json.loads(decoded_sql)

            # 2. 検索条件を保持するQオブジェクトを初期化
            # クライアントIDでの絞り込みは最初から固定で入れておきます
            query = Q(client_id=client_id)

            # 3. 各項目に値が入っているかチェックして条件を追加していく

            # 顧客ID (q_customer)
            if search_condition.get('q_customer'):
                query &= Q(customer_id=search_condition['q_customer'])

            # セグメント (q_segment)
            if search_condition.get('q_segment'):
                query &= Q(segment_id=search_condition['q_segment'])

            # 担当ユーザー (q_user)
            if search_condition.get('q_user'):
                query &= Q(estimate_person=search_condition['q_user'])

            # 工事名・内容 (q_construction)
            # ※ 部分一致（LIKE検索）にする場合は __contains や __icontains を使います
            if search_condition.get('q_construction'):
                query &= Q(construction_name__icontains=search_condition['q_construction'])

            # 4. ステータスの処理
            # {"1": true, "2": false, ...} のうち、値が「true」のものだけを抽出
            status_obj = search_condition.get('q_estimate_status', {})
            active_statuses = [
                status_id for status_id, is_active in status_obj.items() if is_active
            ]

            # もし true になっているステータスが1つ以上あれば、IN句（__in）で絞り込む
            if active_statuses:
                query &= Q(estimate_status__in=active_statuses)

        # 5. 組み立てた条件でデータベースを検索db = {str} 'default'（内部で安全なSQLが自動生成されます）
        if request.method == 'GET':
            estimates = Estimate.objects.filter(query)
            serializer = EstimateSerializer(estimates, many=True)
            return Response(serializer.data)
        # デバッグ用：実際に発行される生のSQLをコンソールで確認できます
        # print("発行されるSQL:", str(estimates.query))

        # 6. 結果をフロントに返す（シリアライズ処理など）
        # data = list(estimates.values())  # 必要に応じて調整してください
        # return JsonResponse({'status': 'success', 'data': data})

    except (json.JSONDecodeError, TypeError, Exception) as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# if request.method == 'GET':
#     estimates = Estimate.objects.order_by('estimate_year', 'estimate_no').filter(client_id=client_id).reverse()
#     serializer = EstimateSerializer(estimates, many=True)
#     return Response(serializer.data)
# elif request.method == 'POST':
#     # 1. リクエストデータに client_id を強制的に含める
#     data = request.data.copy()
#     # 2. estimate_no の重複チェック（null や空文字は除外）
#     estimate_no = data.get('estimate_no')
#     if estimate_no:
#         exists = Estimate.objects.filter(client_id=client_id, estimate_no=estimate_no).exists()
#         if exists:
#             return Response(
#                 {"estimate_no": ["この見積書番号は既に登録されています。"]},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#     serializer = EstimateSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status.HTTP_201_CREATED)
#     return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
# else:
#     return Response(status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def estimate_add(request, client_id):
    if request.method == 'POST':
        # 1. リクエストデータに client_id を強制的に含める
        data = request.data.copy()
        # 2. estimate_no の重複チェック（null や空文字は除外）
        estimate_no = data.get('estimate_no')
        if estimate_no:
            exists = Estimate.objects.filter(client_id=client_id, estimate_no=estimate_no).exists()
            if exists:
                return Response(
                    {"estimate_no": ["この見積書番号は既に登録されています。"]},
                    status=status.HTTP_400_BAD_REQUEST
                )
        serializer = EstimateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def estimate_detail(request, pk):
    try:
        instance = Estimate.objects.get(pk=pk)
    except Estimate.DoesNotExist:
        return Response({"detail": "対象が見つかりません"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        try:
            instance.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except models.ProtectedError:
            msg = f'「{instance.estimate_name}」は他で使われているため削除がきません'
            return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)

        # if request.method == "GET":
        # serializer = EstimateSerializer(instance)
        # return Response(serializer.data)

    serializer = EstimateSerializer(instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        # DHTMLX側が期待する「更新後のデータ単体」を返す
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        # バリデーションエラー時はシリアライザのエラーをそのまま返す
        # これによりJSの .catch(err => { ... }) で項目ごとにエラー表示が可能
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
