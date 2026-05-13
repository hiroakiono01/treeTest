from django.db import models
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
        units = Unit.objects.order_by("sort_order").all()
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
            instance = Unit.objects.filter(id=temp_id).first()

        if instance:
            # 【更新】DBに存在する場合
            serializer = UnitSerializer(instance, data=item, partial=True)
        else:
            # 【新規】DBに存在しない、または一時IDの場合
            item.pop('id', None)  # IDを削除して新規作成として扱う
            serializer = UnitSerializer(data=item)

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
#
# @api_view(['GET'])
# def data_list(request, offset):
#     if request.method == 'GET':
#         units = Unit.objects.order_by('unit_no').all()
#         # tasks = Task.objects.all()
#         unitData = UnitSerializer(units, many=True)
#         # taskData = TaskSerializer(tasks, many=True)
#         return Response({
#             "units": unitData.data,
#             # "tasks": taskData.data
#         })
#
#
# @api_view(['POST'])
# def unit_add(request):
#     if request.method == 'POST':
#         serializer = UnitSerializer(
#             data=request.data,
#             many=isinstance(request.data, list),
#             context={'request': request})
#         print(serializer)
#
#         if serializer.is_valid():
#             units = serializer.save()
#             # DHTMLXのグリッド更新用に、保存された全データをリストで返す
#             return Response(
#                 UnitSerializer(units, many=True, context={'request': request}).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @require_http_methods(["DELETE", "POST"])
# def delete_unit(request, pk):
#     try:
#         obj = Unit.objects.get(pk=pk)
#         obj.delete()
#         return JsonResponse({'success': True})
#     except Unit.DoesNotExist:
#         return JsonResponse({'success': False, 'message': '対象が見つかりません'}, status=404)
#     except models.ProtectedError as e:
#         return JsonResponse({'success': False, 'message': f'「{obj}」他で使われているため削除がきません'}, status=400)
#
#
# # @api_view(['POST'])
# # def task_add(request):
# #     if request.method == 'POST':
# #         serializer = TaskSerializer(data=request.data)
# #         print(serializer)
# #
# #         if serializer.is_valid():
# #             task = serializer.save()
# #             return JsonResponse({'action': 'inserted', 'tid': task.id})
# #         return JsonResponse({'action': 'error'})
#
#
# # @api_view(['PUT', 'DELETE'])
# # def task_update(request, pk):
# #     try:
# #         task = Task.objects.get(pk=pk)
# #     except Task.DoesNotExist:
# #         return JsonResponse({'action': 'error2'})
# #
# #     if request.method == 'PUT':
# #         serializer = TaskSerializer(task, data=request.data)
# #         print(serializer)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return JsonResponse({'action': 'updated'})
# #         return JsonResponse({'action': 'error'})
# #
# #     if request.method == 'DELETE':
# #         task.delete()
# #         return JsonResponse({'action': 'deleted'})
#
#
# class UnitList(generic.ListView):
#     paginate_by = 10
#     context_object_name = 'unit_list'
#     template_name = 'unit_list.html'
#     model = Unit
#     form_class = UnitForm
#
#     def get_queryset(self):
#         return Unit.objects.order_by('unit_no').all()
#
#
# class UnitAdd(generic.FormView):
#     model = Unit
#     template_name = 'unit_add.html'
#     form_class = UnitForm
#     success_url = reverse_lazy('unit:unit_list')
#
#     def form_valid(self, form):
#         form.save()
#         messages.success(self.request, '単位を追加しました。')
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         messages.error(self.request, "単位の追加に失敗しました。")
#         return super().form_invalid(form)
#
#
# class UnitEdit(generic.UpdateView):
#     model = Unit
#     template_name = 'unit_edit.html'
#     form_class = UnitForm
#
#     def get_success_url(self):
#         return reverse_lazy('unit:unit_list')
#
#     def form_valid(self, form):
#         messages.success(self.request, '単位を更新しました。')
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         messages.error(self.request, "単位の更新に失敗しました。")
#         return super().form_invalid(form)
#
#
# class UnitDel(generic.DeleteView):
#     model = Unit
#     template_name = 'unit_del.html'
#
#     def post(self, request, *args, **kwargs):
#
#         try:
#             obj = self.get_object()
#             obj.delete()
#             messages.success(self.request, "単位を削除しました。")
#             return redirect('unit:unit_list')
#         except models.ProtectedError as e:
#             messages.error(request, f'「{obj}」は他で使われているため削除がきません。')
#             return redirect('unit:unit_list')
