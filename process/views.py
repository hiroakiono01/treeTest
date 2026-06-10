from django.db import models, transaction
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import ProcessSerializer
from app.models import Process


def process_list_call(request):
    return render(request, 'process_list.html')


@api_view(['GET'])
def process_list(request):
    if request.method == 'GET':
        processes = Process.objects.order_by("sort_order").all()
        serializer = ProcessSerializer(processes, many=True)
        return Response(serializer.data)

    # elif request.method == "POST":
    #     serializer = ProcessSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #


@api_view(["DELETE"])
def process_detail(request, pk):
    """
    Retrieve, update or delete a code process.
    """
    try:
        instance = Process.objects.get(pk=pk)
    except Process.DoesNotExist:
        return Response({"detail": "対象が見つかりません"}, status=status.HTTP_404_NOT_FOUND)

    # if request.method == "GET":
    #     serializer = ProcessSerializer(process)
    #     return Response(serializer.data)
    #
    # elif request.method == "PUT":
    #     serializer = ProcessSerializer(process, data=request.data)
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
def bulk_sync_processes(request):
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
                    serializer = ProcessSerializer(data=save_data)
                    instance_exists = False
                else:
                    # 💡 既存データの更新
                    instance = Process.objects.filter(id=raw_id).first()
                    if not instance:
                        raise ValueError({'error': f'{index + 1}件目のデータ（ID: {raw_id}）がデータベースに存在しません。'})

                    serializer = ProcessSerializer(instance, data=save_data, partial=True)

                    instance_exists = True

                if serializer.is_valid():
                    saved_instance = serializer.save()
                    # 保存後のオブジェクトから、正式に出力用データを生成
                    result_item = ProcessSerializer(saved_instance).data
                    # マッピングの記録（後続の子要素のため）
                    if not instance_exists:
                        result_item['client_id'] = raw_id

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
# def bulk_sync_processs(request):
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
#             instance = Process.objects.filter(id=temp_id).first()
#
#         if instance:
#             # 【更新】DBに存在する場合
#             serializer = ProcessSerializer(instance, data=item, partial=True)
#         else:
#             # 【新規】DBに存在しない、または一時IDの場合
#             item.pop('id', None)  # IDを削除して新規作成として扱う
#             serializer = ProcessSerializer(data=item)
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
