from django.contrib import messages
from django.db import models
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import TaskSerializer
from app.models import Reference, Task
from reference.forms import ReferenceForm


def task_list_call(request):
    return render(request, 'task_tree.html')


@api_view(['GET', 'POST'])
def task_list(request):
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
