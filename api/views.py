# from rest_framework import renderers
from django.http import JsonResponse
# from rest_framework import renderers
from django.shortcuts import render
# from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from api.serializers import UnitSerializer
from app.models import Unit, Estimate


def index(request):
    return render(request, 'index.html')


@api_view(['GET'])
def get_unit_options(request):
    # combobox の場合はid,valueでselectは使えない
    unit_options = [
        {
            "id": unit.id,  # 文字型として代入
            "value": unit.unit_name  # 文字列型（表示名）
        }
        for unit in Unit.objects.order_by("unit_no").all()
    ]
    return Response({"units": unit_options})


@api_view(['GET'])
def get_estimate_options(request):
    estimate_options = [
        {
            "value": estimate.id,  # 数値型として代入
            "content": estimate.estimate_name  # 文字列型（表示名）
        }
        for estimate in Estimate.objects.all()
    ]
    return Response({"estimates": estimate_options})


# estimate_noを取得してえestimate_nameを返す
from django.http import JsonResponse
from app.models import Estimate


def get_estimate_name(request):
    # GETパラメータから 'estimate_no' を取得
    est_no = request.GET.get('estimate_no', None)

    if est_no:
        estimate = Estimate.objects.filter(estimate_no=est_no).first()
        if estimate:
            return JsonResponse({'estimate_name': estimate.estimate_name})

    return JsonResponse({'estimate_name': ''}, status=404)


# views.py


def reference_page(request):
    # DHTMLX Gridのoptions形式に合わせてリネームして取得

    units = Unit.objects.all().values("id", "unit_name", )
    unit_options = [{"id": c['id'], "value": c['unit_name']} for c in units]

    return render(request, 'reference/reference_list.html', {
        'unit_options': unit_options
    })


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    # renderer_classes = [JSONOpenAPIRenderer, TemplateHTMLRenderer]
    # renderer_classes = [JSONOpenAPIRenderer]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'unit_list.html'
