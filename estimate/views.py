from django.contrib import messages
from django.db import models
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import EstimateSerializer
from app.models import Estimate
from estimate.forms import EstimateAddForm


def estimate_list_call(request):
    return render(request, 'estimate_list.html')


@api_view(['GET', 'POST'])
def estimate_list(request):
    if request.method == 'GET':
        estimates = Estimate.objects.all()
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

    # 3. 取得処理 (GET)
    if request.method == "GET":
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


class EstimateList(generic.ListView):
    """ 見積一覧表　照会画面 """
    context_object_name = 'estimate_list'
    template_name = 'estimate_list.html'
    model = Estimate

    def get_queryset(self):
        estimate = Estimate.objects.all()
        return estimate


class EstimateAdd(generic.CreateView):
    template_name = 'estimate_add.html'
    success_url = reverse_lazy('estimate:estimate_list')
    form_class = EstimateAddForm

    def form_valid(self, form):
        messages.success(self.request, 'create estimate')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "invalid estimate")
        return super().form_invalid(form)


class EstimateEdit(generic.UpdateView):
    model = Estimate
    template_name = 'estimate_edit.html'
    success_url = reverse_lazy('estimate:estimate_list')
    form_class = EstimateAddForm

    def form_valid(self, form):
        messages.success(self.request, 'edit estimate')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "invalid estimate")
        return super().form_invalid(form)


class EstimateDel(generic.DeleteView):
    model = Estimate
    template_name = 'estimate_del.html'

    def post(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            obj.delete()
            messages.success(self.request, "delete estimate")
            return redirect('estimate:estimate_list')
        except models.ProtectedError as e:
            messages.error(request, f'「{obj}」estimate use other')
            return redirect('estimate:estimate_list')
