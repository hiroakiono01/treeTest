from django.db import models
from django.db import transaction
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import UnitSerializer
from app.models import Unit


def unit_list_call(request):
    return render(request, 'unit_list.html')


@api_view(['GET'])
def unit_list(request, client_id):
    units = Unit.objects.order_by("unit_no").exclude(unit_name="").exclude(unit_name__isnull=True).filter(client_id=client_id).all()
    serializer = UnitSerializer(units, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
def unit_detail(request, pk):
    try:
        instance = Unit.objects.get(id=pk)
        try:
            instance.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except models.ProtectedError:
            msg = f'「{instance.unit_name}」は他で使用されているため削除できません。'
            return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)
    except Unit.DoesNotExist:
        return Response({"detail": "対象が見つかりません"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 💡 ログイン必須にする（未ログインなら 401 応答）
def bulk_sync_units(request):
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
                    serializer = UnitSerializer(data=save_data)
                    instance_exists = False
                else:
                    # 💡 既存データの更新
                    instance = Unit.objects.filter(id=raw_id).first()
                    if not instance:
                        raise ValueError({'error': f'{index + 1}件目のデータ（ID: {raw_id}）がデータベースに存在しません。'})

                    serializer = UnitSerializer(instance, data=save_data, partial=True)
                    instance_exists = True

                if serializer.is_valid():
                    # データベースに保存を実行（新規登録の場合は、ここで自動的に数値IDが採番されます）
                    if instance_exists:
                        saved_instance = serializer.save(update_user=username)
                    else:
                        saved_instance = serializer.save(create_user=username)

                    # 保存後のオブジェクトから、正式に出力用データを生成
                    result_item = UnitSerializer(saved_instance).data

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
