from django.db import models
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import UnitSerializer
from app.models import Unit


def unit_list_call(request):
    return render(request, 'unit_list.html')


@api_view(['GET', 'POST'])
def unit_list(request):
    if request.method == 'GET':
        units = Unit.objects.order_by("unit_no").all()
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def unit_detail(request, pk):
    try:
        instance = Unit.objects.get(pk=pk)
    except Unit.DoesNotExist:
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
        serializer = UnitSerializer(instance)
        return Response(serializer.data)

    serializer = UnitSerializer(instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        # DHTMLX側が期待する「更新後のデータ単体」を返す
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        # バリデーションエラー時はシリアライザのエラーをそのまま返す
        # これによりJSの .catch(err => { ... }) で項目ごとにエラー表示が可能
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def bulk_sync_units(request):
    data_list = request.data
    response_data = []
    errors_dict = {}
    has_error = False
    # --------------------------------------------------
    # 1. 全データのバリデーション（チェック）フェーズ
    # --------------------------------------------------
    for index, item in enumerate(data_list):
        temp_id = item.get('id')
        item['sort_order'] = index  # 画面の並び順を反映
        # print(temp_id)
        is_temp_id = (
                temp_id is None or
                temp_id == "" or
                (isinstance(temp_id, str) and temp_id.startswith('u'))
        )
        instance = None
        if not is_temp_id:
            instance = Unit.objects.filter(id=temp_id).first()

        validate_data = item.copy()
        # print(validate_data, "validate")
        if not instance:
            validate_data.pop('id', None)

        if instance:
            # 💡 validate_data を渡すように統一します
            serializer = UnitSerializer(instance, data=validate_data, partial=True)
            print("instance yes", validate_data)
        else:
            serializer = UnitSerializer(data=validate_data)
            print("instance no", validate_data)
        # print(serializer, "serializer")

        if not serializer.is_valid():
            has_error = True
            error_info = serializer.errors.copy()
            print(error_info, "is_valid")

            cleaned_errors = {}
            for field, messages in error_info.items():
                if isinstance(messages, list) and len(messages) > 0:
                    cleaned_errors[field] = messages[0]  # 最初のエラーメッセージを取得
                else:
                    cleaned_errors[field] = messages

            # 各行のエラーを溜める
            errors_dict[temp_id] = cleaned_errors

    # 💡 修正ポイント: if has_error の判定は for ループの「外」に出します
    # これにより、全行のチェックが完全に終わった後でエラーを返却できます
    if has_error:
        return Response({'row_errors': errors_dict}, status=400)

    # --------------------------------------------------
    # 2. データベースへの保存フェーズ（エラーがない場合のみ到達）
    # --------------------------------------------------
    id_map = {}

    # 複数行の保存中にエラーが起きたら元に戻せるようトランザクションで囲みます
    with transaction.atomic():
        for index, item in enumerate(data_list):
            temp_id = item.get('id')
            item['sort_order'] = index

            is_temp_id = (
                    temp_id is None or
                    temp_id == "" or
                    (isinstance(temp_id, str) and temp_id.startswith('u'))
            )
            instance = None
            if not is_temp_id:
                instance = Unit.objects.filter(id=temp_id).first()

            save_data = item.copy()
            if not instance:
                save_data.pop('id', None)

            if instance:
                serializer = UnitSerializer(instance, data=save_data, partial=True)
            else:
                serializer = UnitSerializer(data=save_data)

            # 既に上のフェーズで検証済みなので必ず True になります
            if serializer.is_valid():
                # 💡 修正ポイント: データベースに保存を実行します
                saved_instance = serializer.save()

                # フロント側の一時IDと、新しく発行されたDBの本番IDをマッピング
                if is_temp_id or not instance:
                    id_map[temp_id] = saved_instance.id

                response_data.append(serializer.data)

    # 💡 修正ポイント: 関数の最後で、必ず成功レスポンスを返却します
    return Response({
        'status': 'success',
        'id_map': id_map,  # 新規作成した行のID変換表をフロントに伝える
        'data': response_data
    }, status=status.HTTP_200_OK)


