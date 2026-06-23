from django.db import models
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import SegmentSerializer
from app.models import Segment


def segment_list_call(request):
    return render(request, 'segment_list.html')


@api_view(['GET'])
def segment_list(request, client_id):
    if request.method == 'GET':
        segments = Segment.objects.order_by("segment_no").exclude(segment_name="").exclude(segment_name__isnull=True).filter(client_id=client_id).all()
        serializer = SegmentSerializer(segments, many=True)
        return Response(serializer.data)


@api_view(["DELETE"])
def segment_detail(request, pk):
    try:
        instance = Segment.objects.get(pk=pk)
    except Segment.DoesNotExist:
        return Response({"detail": "対象が見つかりません"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        try:
            instance.delete()
            return JsonResponse({'success': True}, status=status.HTTP_200_OK)
        except models.ProtectedError as e:
            msg = f'「{instance}」は他で使われているため削除がきません'
            return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def bulk_sync_segments(request):
    data_list = request.data
    response_data = []
    username = request.user.username

    try:
        with transaction.atomic():
            for index, item in enumerate(data_list):
                raw_id = item.get('id')

                # 元のデータを汚さないようにコピー
                save_data = item.copy()

                # 💡 判定：送られてきたIDが 'u' から始まる場合は「新規登録」
                if isinstance(raw_id, str) and raw_id.startswith('u'):
                    # 1. シリアライザのバリデーションを通すため、save_data から 'id' キーごと完全に削除する
                    save_data.pop('id', None)

                    # 2. シリアライザに余計なフィールドを渡さない（エラー防止）
                    serializer = SegmentSerializer(data=save_data)
                    instance_exists = False
                else:
                    # 💡 既存データの更新
                    instance = Segment.objects.filter(id=raw_id).first()
                    if not instance:
                        raise ValueError({'error': f'{index + 1}件目のデータ（ID: {raw_id}）がデータベースに存在しません。'})

                    serializer = SegmentSerializer(instance, data=save_data, partial=True)
                    instance_exists = True

                if serializer.is_valid():
                    # データベースに保存を実行（新規登録の場合は、ここで自動的に数値IDが採番されます）
                    if instance_exists:
                        saved_instance = serializer.save(update_user=username)
                    else:
                        saved_instance = serializer.save(create_user=username)

                    # 保存後のオブジェクトから、正式に出力用データを生成
                    result_item = SegmentSerializer(saved_instance).data

                    # 💡 新規登録だった場合のみ、レスポンスに元の一時ID（u...）を付与して返す
                    if not instance_exists:
                        result_item['client_id'] = raw_id

                    response_data.append(result_item)
                else:
                    # 💡 バリデーションエラーが起きた場合、何が原因か詳細をレスポンスに含める
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
