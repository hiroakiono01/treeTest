from django.db import models
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import TaskSerializer
from app.models import Task


def task_list_call(request):
    return render(request, 'task_list.html')


def task_tree_test(request):
    return render(request, 'task_tree_test.html')


@api_view(['GET', 'POST'])
def tree_list_test(request):
    # estimate_no = request.query_params.get('estimate_no')
    # estimate_no = 1
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def tree_detail_test(request, pk):
    try:
        instance = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"detail": "対象が見つかりません"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        try:
            instance.delete()
            return JsonResponse({'success': True}, status=status.HTTP_200_OK)
        except models.ProtectedError as e:
            msg = f'「{instance}」は他で使われているため削除がきません'
            return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)

    # 3. 取得処理 (GET)
    if request.method == "GET":
        serializer = TaskSerializer(instance)
        return Response(serializer.data)

    serializer = TaskSerializer(instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        # DHTMLX側が期待する「更新後のデータ単体」を返す
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        # バリデーションエラー時はシリアライザのエラーをそのまま返す
        # これによりJSの .catch(err => { ... }) で項目ごとにエラー表示が可能
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def task_list(request, estimate_no):
    # estimate_no = request.query_params.get('estimate_no')
    # estimate_no = 1
    if request.method == 'GET':
        if 'text/html' in request.headers.get('Accept', ''):
            return render(request, 'task_list.html', {'estimate_no': estimate_no})
        tasks = Task.objects.filter(estimate_no=estimate_no).order_by("sort_order").all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def task_detail(request, pk):
    try:
        instance = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"detail": "対象が見つかりません"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        try:
            instance.delete()
            return JsonResponse({'success': True}, status=status.HTTP_200_OK)
        except models.ProtectedError as e:
            msg = f'「{instance}」は他で使われているため削除がきません'
            return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)

    # 3. 取得処理 (GET)
    if request.method == "GET":
        serializer = TaskSerializer(instance)
        return Response(serializer.data)

    serializer = TaskSerializer(instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        # DHTMLX側が期待する「更新後のデータ単体」を返す
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        # バリデーションエラー時はシリアライザのエラーをそのまま返す
        # これによりJSの .catch(err => { ... }) で項目ごとにエラー表示が可能
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import Unit
from api.serializers import UnitSerializer

from django.shortcuts import get_object_or_404


@api_view(['POST'])
def bulk_sync_tasks(request):
    data_list = request.data
    response_data = []
    id_map = {}

    for item in data_list:
        temp_id = item.get('id')
        parent_val = item.get('parent')

        # 親IDの解決
        if parent_val in id_map:
            item['parent'] = id_map[parent_val]

        # 新規か更新かの判定ロジックを強化
        # 1. IDがNone or 空文字
        # 2. 文字列で 'u' から始まる
        # 3. IDがDBに存在しない (DoesNotExist 対策)
        is_temp_id = (
                temp_id is None or
                temp_id == "" or
                (isinstance(temp_id, str) and temp_id.startswith('u'))
        )

        instance = None
        if not is_temp_id:
            # 既存データをDBから探す（エラーにならないように filter().first() を使用）
            instance = Task.objects.filter(id=temp_id).first()

        if instance:
            # 【更新】DBに存在する場合
            serializer = TaskSerializer(instance, data=item, partial=True)
        else:
            # 【新規】DBに存在しない、または一時IDの場合
            item.pop('id', None)  # IDを削除して新規作成として扱う
            serializer = TaskSerializer(data=item)

        if serializer.is_valid():
            saved_instance = serializer.save()

            # マッピングの記録（後続の子要素のため）
            if is_temp_id or not instance:
                id_map[temp_id] = saved_instance.id

            response_data.append(serializer.data)
        else:
            print(f"Serializer Error: {serializer.errors}")  # デバッグ用
            return Response(serializer.errors, status=400)

    return Response(response_data, status=200)

