from django.db import models
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import ReferenceSerializer
from app.models import Reference


def reference_list_call(request):
    return render(request, 'reference_list.html')


@api_view(['GET', "POST"])
def reference_list(request):
    if request.method == 'GET':
        references = Reference.objects.order_by("sort_order").all()
        serializer = ReferenceSerializer(references, many=True)
        return Response(serializer.data)

    # elif request.method == "POST":
    #     serializer = ReferenceSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #


@api_view(["DELETE"])
def reference_detail(request, pk):
    """
    Retrieve, update or delete a code reference.
    """
    try:
        instance = Reference.objects.get(pk=pk)
    except Reference.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # if request.method == "GET":
    #     serializer = ReferenceSerializer(reference)
    #     return Response(serializer.data)
    #
    # elif request.method == "PUT":
    #     serializer = ReferenceSerializer(reference, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        try:
            instance.delete()
            return JsonResponse({'success': True}, status=status.HTTP_200_OK)
        except models.ProtectedError as e:
            msg = f'「{instance}」は他で使われているため削除がきません'
            return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def bulk_sync_references(request):
    data_list = request.data
    response_data = []
    id_map = {}

    # enumerate を使って、データの並び順（0, 1, 2...）を index として取得します
    for index, item in enumerate(data_list):
        temp_id = item.get('id')
        parent_val = item.get('parent')
        item['sort_order'] = index

        is_temp_id = (
                temp_id is None or
                temp_id == "" or
                (isinstance(temp_id, str) and temp_id.startswith('u'))
        )
        instance = None
        if not is_temp_id:
            # 既存データをDBから探す（エラーにならないように filter().first() を使用）
            instance = Reference.objects.filter(id=temp_id).first()

        if instance:
            # 【更新】DBに存在する場合
            serializer = ReferenceSerializer(instance, data=item, partial=True)
        else:
            # 【新規】DBに存在しない、または一時IDの場合
            item.pop('id', None)  # IDを削除して新規作成として扱う
            serializer = ReferenceSerializer(data=item)

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
