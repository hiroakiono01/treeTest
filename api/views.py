# from rest_framework import renderers
from django.shortcuts import render
# from rest_framework import renderers
from django.shortcuts import render
# from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from api.serializers import UnitSerializer
from app.models import Unit


def index(request):
    return render(request, 'index.html')


@api_view(['GET'])
def get_unit_options(request):
    unit_options = [
        {
            "value": unit.id,  # 数値型として代入
            "content": unit.unit_name  # 文字列型（表示名）
        }
        for unit in Unit.objects.all()
    ]
    return Response({"units": unit_options})


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
