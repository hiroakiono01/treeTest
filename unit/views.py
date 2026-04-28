from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods, require_POST
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from app.models import Unit, Task
from django.urls import reverse_lazy
from django.contrib import messages
from unit.forms import UnitForm
from django.db import models, transaction
from api.serializers import UnitSerializer, TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from api.serializers import UnitSerializer
import json
from django.http import JsonResponse


def unit_list(request):
    return render(request, 'unit_list.html')


@api_view(['POST'])
def save_unit_api(request):
    if request.method == 'POST':
        data = request.data

        raw_id = data.get('id')
        instance = None
        if isinstance(raw_id, (int, str)) and str(raw_id).isdigit():
            instance = Unit.objects.filter(id=raw_id).first()

        if instance:
            # 更新 (Partial=True で一部フィールドのみの更新にも対応)
            serializer = UnitSerializer(instance, data=data, partial=True)
        else:
            # 新規作成 (一時IDなどはシリアライザに渡さないように id を除外)
            item_data = data.copy()
            item_data.pop('id', None)
            serializer = UnitSerializer(data=item_data)

        if serializer.is_valid():
            saved_instance = serializer.save()
            return Response({
                'success': True,
                'id': saved_instance.id,
                'data': UnitSerializer(saved_instance).data
            }, status=status.HTTP_200_OK)
        else:
            # バリデーションエラー時は例外を投げてロールバックさせる
            return Response({
                "error": "validation Failed",
                "details": serializer.errors,
                "item": data
            }, status=status.HTTP_400_BAD_REQUEST)





        # 更新の場合は instance を渡す（IDなどで判断）
        # instance = Unit.objects.filter(id=data.get('id')).first()
        # form = UnitForm(data, instance=instance)
        #
        # if form.is_valid():
        #     obj = form.save()
        #     return JsonResponse({
        #         'success': True,
        #         'id': obj.id})  # 新しく振られたIDを返す
        # else:
        #     # unique=True などのエラーメッセージを取得
        #     msg = " / ".join([e[0] for e in form.errors.values()])
        #     return JsonResponse({'success': False, 'message': msg})


# @api_view(['POST'])
# def batch_save(request):
#     # request.data自体がリスト（配列）なので、直接ループを回す
#
#     data_list = request.data
#     if not isinstance(data_list, list):
#         return Response({"error": "データがリスト形式ではありません"}, status=status.HTTP_400_BAD_REQUEST)
#     results = []
#     try:
#         with transaction.atomic():
#             # 送られてきたリストをループ処理
#             for item in request.data:
#                 raw_id = item.get('id')
#
#                 # 既存データの更新か新規作成かを判定
#                 # 数値型であり、かつ実際にDBに存在するIDか確認
#                 instance = None
#                 if isinstance(raw_id, (int, str)) and str(raw_id).isdigit():
#                     instance = Unit.objects.filter(id=raw_id).first()
#
#                 if instance:
#                     # 更新 (Partial=True で一部フィールドのみの更新にも対応)
#                     serializer = UnitSerializer(instance, data=item, partial=True)
#                 else:
#                     # 新規作成 (一時IDなどはシリアライザに渡さないように id を除外)
#                     item_data = item.copy()
#                     item_data.pop('id', None)
#                     serializer = UnitSerializer(data=item_data)
#
#                 if serializer.is_valid():
#                     saved_instance = serializer.save()
#                     results.append(UnitSerializer(saved_instance).data)
#                 else:
#                     # バリデーションエラー時は例外を投げてロールバックさせる
#                     return Response({
#                         "error": "validation Failed",
#                         "details": serializer.errors,
#                         "item": item
#                     }, status=status.HTTP_400_BAD_REQUEST)
#
#             # 全ての処理が成功した場合のみここに来る
#             return Response(results, status=status.HTTP_200_OK)
#     except Exception as e:
#         # 処理後の全データをリストで返却
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class UnitViewSet(viewsets.ModelViewSet):
#     queryset = Unit.objects.all()
#     serializer_class = UnitSerializer


@api_view(['GET'])
def data_list(request, offset):
    if request.method == 'GET':
        units = Unit.objects.order_by('unit_no').all()
        # tasks = Task.objects.all()
        unitData = UnitSerializer(units, many=True)
        # taskData = TaskSerializer(tasks, many=True)
        return Response({
            "units": unitData.data,
            # "tasks": taskData.data
        })


@api_view(['POST'])
def unit_add(request):
    if request.method == 'POST':
        serializer = UnitSerializer(
            data=request.data,
            many=isinstance(request.data, list),
            context={'request': request})
        print(serializer)

        if serializer.is_valid():
            units = serializer.save()
            # DHTMLXのグリッド更新用に、保存された全データをリストで返す
            return Response(
                UnitSerializer(units, many=True, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@require_http_methods(["DELETE", "POST"])
def delete_unit(request, pk):
    try:
        obj = Unit.objects.get(pk=pk)
        obj.delete()
        return JsonResponse({'success': True})
    except Unit.DoesNotExist:
        return JsonResponse({'success': False, 'message': '対象が見つかりません'}, status=404)
    except models.ProtectedError as e:
        return JsonResponse({'success': False, 'message': f'「{obj}」他で使われているため削除がきません'}, status=400)


# @api_view(['POST'])
# def task_add(request):
#     if request.method == 'POST':
#         serializer = TaskSerializer(data=request.data)
#         print(serializer)
#
#         if serializer.is_valid():
#             task = serializer.save()
#             return JsonResponse({'action': 'inserted', 'tid': task.id})
#         return JsonResponse({'action': 'error'})


# @api_view(['PUT', 'DELETE'])
# def task_update(request, pk):
#     try:
#         task = Task.objects.get(pk=pk)
#     except Task.DoesNotExist:
#         return JsonResponse({'action': 'error2'})
#
#     if request.method == 'PUT':
#         serializer = TaskSerializer(task, data=request.data)
#         print(serializer)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse({'action': 'updated'})
#         return JsonResponse({'action': 'error'})
#
#     if request.method == 'DELETE':
#         task.delete()
#         return JsonResponse({'action': 'deleted'})


class UnitList(generic.ListView):
    paginate_by = 10
    context_object_name = 'unit_list'
    template_name = 'unit_list.html'
    model = Unit
    form_class = UnitForm

    def get_queryset(self):
        return Unit.objects.order_by('unit_no').all()


class UnitAdd(generic.FormView):
    model = Unit
    template_name = 'unit_add.html'
    form_class = UnitForm
    success_url = reverse_lazy('unit:unit_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, '単位を追加しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "単位の追加に失敗しました。")
        return super().form_invalid(form)


class UnitEdit(generic.UpdateView):
    model = Unit
    template_name = 'unit_edit.html'
    form_class = UnitForm

    def get_success_url(self):
        return reverse_lazy('unit:unit_list')

    def form_valid(self, form):
        messages.success(self.request, '単位を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "単位の更新に失敗しました。")
        return super().form_invalid(form)


class UnitDel(generic.DeleteView):
    model = Unit
    template_name = 'unit_del.html'

    def post(self, request, *args, **kwargs):

        try:
            obj = self.get_object()
            obj.delete()
            messages.success(self.request, "単位を削除しました。")
            return redirect('unit:unit_list')
        except models.ProtectedError as e:
            messages.error(request, f'「{obj}」は他で使われているため削除がきません。')
            return redirect('unit:unit_list')
