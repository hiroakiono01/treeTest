import json

from django.db import models
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import urllib.parse
from django.db.models import Q
from api.serializers import EstimateSerializer
from app.models import Estimate


def estimate_list_call(request):
    return render(request, 'estimate_list.html')


@api_view(['GET', 'POST'])
def estimate_list(request, client_id, sql):
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
    query &= Q(segment=search_condition['q_segment'])

# 担当ユーザー (q_user)
if search_condition.get('q_user'):
    query &= Q(user_id=search_condition['q_user'])

# 工事名・内容 (q_construction)
# ※ 部分一致（LIKE検索）にする場合は __contains や __icontains を使います
if search_condition.get('q_construction'):
    query &= Q(construction_name__icontains=search_condition['q_construction'])

if request.method == 'GET':
    estimates = Estimate.objects.order_by('estimate_year', 'estimate_no').filter(client_id=client_id).reverse()
    serializer = EstimateSerializer(estimates, many=True)
    return Response(serializer.data)
elif request.method == 'POST':
    serializer = EstimateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def estimate_detail(request, pk):
    try:
        instance = Estimate.objects.get(pk=pk)
    except Estimate.DoesNotExist:
        return Response({"detail": "対象が見つかりません"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        try:
            instance.delete()
            return JsonResponse({'success': True}, status=status.HTTP_200_OK)
        except models.ProtectedError as e:
            msg = f'「{instance}」は他で使われているため削除がきません'
            return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)

        # if request.method == "GET":
        serializer = EstimateSerializer(instance)
        return Response(serializer.data)

    serializer = EstimateSerializer(instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        # DHTMLX側が期待する「更新後のデータ単体」を返す
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        # バリデーションエラー時はシリアライザのエラーをそのまま返す
        # これによりJSの .catch(err => { ... }) で項目ごとにエラー表示が可能
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#


# class EstimateList(generic.ListView):
#     """ 見積一覧表　照会画面 """
#     context_object_name = 'estimate_list'
#     template_name = 'estimate_list.html'
#     model = Estimate
#
#     def get_queryset(self):
#         estimate = Estimate.objects.all()
#         return estimate
#
#
# class EstimateAdd(generic.CreateView):
#     template_name = 'estimate_add.html'
#     success_url = reverse_lazy('estimate:estimate_list')
#     form_class = EstimateAddForm
#
#     def form_valid(self, form):
#         messages.success(self.request, 'create estimate')
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         messages.error(self.request, "invalid estimate")
#         return super().form_invalid(form)
#
#
# class EstimateEdit(generic.UpdateView):
#     model = Estimate
#     template_name = 'estimate_edit.html'
#     success_url = reverse_lazy('estimate:estimate_list')
#     form_class = EstimateAddForm
#
#     def form_valid(self, form):
#         messages.success(self.request, 'edit estimate')
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         messages.error(self.request, "invalid estimate")
#         return super().form_invalid(form)
#
#
# class EstimateDel(generic.DeleteView):
#     model = Estimate
#     template_name = 'estimate_del.html'
#
#     def post(self, request, *args, **kwargs):
#         try:
#             obj = self.get_object()
#             obj.delete()
#             messages.success(self.request, "delete estimate")
#             return redirect('estimate:estimate_list')
#         except models.ProtectedError as e:
#             messages.error(request, f'「{obj}」estimate use other')
#             return redirect('estimate:estimate_list')
