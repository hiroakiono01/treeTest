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

from api.serializers import ReferenceSerializer
from app.models import Reference
from reference.forms import ReferenceForm


class ReferenceListView(TemplateView):
    template_name = "reference_list.html"


class ReferenceListCreateView(generics.ListCreateAPIView):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer

    def post(self, request, *args, **kwargs):
        # Unitの時と同様の一括保存ロジック（前述のUnitViewと同様のため省略）
        pass


class ReferenceDetailView(generics.DestroyAPIView):
    queryset = Reference.objects.all()


def reference_list_call(request):
    return render(request, 'reference_list.html')


@api_view(['GET', "POST"])
def reference_list(request):
    if request.method == 'GET':
        references = Reference.objects.all()
        serializer = ReferenceSerializer(references, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ReferenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def reference_detail(request, pk):
    """
    Retrieve, update or delete a code reference.
    """
    try:
        reference = Reference.objects.get(pk=pk)
    except Reference.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ReferenceSerializer(reference)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ReferenceSerializer(reference, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        reference.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['POST'])
# def reference_update(request):
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
#                     serializer = ReferenceSerializer(instance, data=item, partial=True)
#                 else:
#                     # 新規作成 (一時IDなどはシリアライザに渡さないように id を除外)
#                     item_data = item.copy()
#                     item_data.pop('id', None)
#                     serializer = ReferenceSerializer(data=item_data)
#
#                 if serializer.is_valid():
#                     saved_instance = serializer.save()
#                     results.append(ReferenceSerializer(saved_instance).data)
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
#

def get_reference_data(request):
    # unit_name_id とすることで、ForeignKeyのID値を直接取得できます
    data = list(Reference.objects.all().values(
        "id",
        "detail_name",
        "calcu_cls",
        "unit_name_id",  # ここが重要！
        "budget_price"
    ))
    return JsonResponse(data, safe=False)


class ReferenceList(generic.ListView):
    paginate_by = 10
    context_object_name = 'reference_list'
    template_name = 'reference_list.html'
    model = Reference
    form_class = ReferenceForm

    def get_queryset(self):
        return Reference.objects.all()


class ReferenceAdd(generic.FormView):
    model = Reference
    template_name = 'reference_add.html'
    form_class = ReferenceForm
    success_url = reverse_lazy('reference:reference_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, '単位を追加しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "単位の追加に失敗しました。")
        return super().form_invalid(form)


class ReferenceEdit(generic.UpdateView):
    model = Reference
    template_name = 'reference_edit.html'
    form_class = ReferenceForm

    def get_success_url(self):
        return reverse_lazy('reference:reference_list')

    def form_valid(self, form):
        messages.success(self.request, '単位を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "単位の更新に失敗しました。")
        return super().form_invalid(form)


class ReferenceDel(generic.DeleteView):
    model = Reference
    template_name = 'reference_del.html'

    def post(self, request, *args, **kwargs):

        try:
            obj = self.get_object()
            obj.delete()
            messages.success(self.request, "単位を削除しました。")
            return redirect('reference:reference_list')
        except models.ProtectedError as e:
            messages.error(request, f'「{obj}」は他で使われているため削除がきません。')
            return redirect('reference:reference_list')
