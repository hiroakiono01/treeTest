# from rest_framework import renderers
# from rest_framework import renderers
# from rest_framework import renderers
from django.http import JsonResponse
from django.shortcuts import render

from app.models import Estimate, CurrentClient, Client, Fiscalyear, Customer, Segment, Construction


def index(request):
    return render(request, 'index.html')


# @api_view(['GET'])
# def get_unit_options(request):
#     # combobox の場合はid,valueでselectは使えない
#     unit_options = [
#         {
#             "id": unit.id,  # 文字型として代入
#             "value": unit.unit_name  # 文字列型（表示名）
#         }
#         for unit in Unit.objects.order_by("unit_no").all()
#     ]
#     return Response({"units": unit_options})


# @api_view(['GET'])
# def get_estimate_options(request):
#     estimate_options = [
#         {
#             "value": estimate.id,  # 数値型として代入
#             "content": estimate.estimate_name  # 文字列型（表示名）
#         }
#         for estimate in Estimate.objects.all()
#     ]
#     return Response({"estimates": estimate_options})


# estimate_noを取得してえestimate_nameを返す
def get_current_client(self):
    try:
        # currentClient = CurrentClient.objects.all().first()
        currentClient = CurrentClient.objects.filter(customUser=self.user).all().first()
        client = Client.objects.get(pk=currentClient.client.pk)
        result = {'client_id': client.id,
                  'client_no': client.client_no,
                  'client_name': client.client_name,
                  }
        return JsonResponse({'current-client': result})
    except Exception as e:

        result = {'client_id': '',
                  'client_no': '',
                  'client_name': '選択されていません',
                  }

    return JsonResponse({'current-client': result}, status=404)


def get_estimate_name(request):
    # GETパラメータから 'estimate_no' を取得
    est_no = request.GET.get('estimate_no', None)

    if est_no:
        estimate = Estimate.objects.filter(estimate_no=est_no).first()
        if estimate:
            return JsonResponse({'estimate_name': estimate.estimate_name})

    return JsonResponse({'estimate_name': ''}, status=404)


def get_fiscalyears(request, client_id):
    # データベースから全年度を取得
    years = Fiscalyear.objects.all().filter(client_id=client_id).order_by('-id')  # 必要に応じてソート

    # DHTMLXのComboが要求する形式 [ {"value": "X", "content": "Y"}, ... ] に整形
    data = [
        {
            "id": str(year.id),
            "value": str(year.fiscalyear_name)  # 画面に表示したい名称のフィールド（例: 2026年度）
        }
        for year in years
    ]

    return JsonResponse(data, safe=False)


def get_customers(request, client_id):
    customers = Customer.objects.all().filter(client_id=client_id).order_by('customer_no')  # 必要に応じてソート
    data = [
        {
            "id": str(customer.id),
            "value": str(customer.customer_name)
        }
        for customer in customers
    ]
    return JsonResponse(data, safe=False)


def get_segments(request, client_id):
    segments = Segment.objects.all().filter(client_id=client_id).order_by('segment_no')  # 必要に応じてソート
    data = [
        {
            "id": str(segment.id),
            "value": str(segment.segment_name)
        }
        for segment in segments
    ]
    return JsonResponse(data, safe=False)


def get_constructions(request, client_id):
    constructions = Construction.objects.all().filter(client_id=client_id).order_by('construction_no')  # 必要に応じてソート
    data = [
        {
            "id": str(construction.id),
            "value": str(construction.construction_name)
        }
        for construction in constructions
    ]
    return JsonResponse(data, safe=False)

# def reference_page(request):
#     # DHTMLX Gridのoptions形式に合わせてリネームして取得
#
#     units = Unit.objects.all().values("id", "unit_name", )
#     unit_options = [{"id": c['id'], "value": c['unit_name']} for c in units]
#
#     return render(request, 'reference/reference_list.html', {
#         'unit_options': unit_options
#     })


# class UnitViewSet(viewsets.ModelViewSet):
#     queryset = Unit.objects.all()
#     serializer_class = UnitSerializer
#     # renderer_classes = [JSONOpenAPIRenderer, TemplateHTMLRenderer]
#     # renderer_classes = [JSONOpenAPIRenderer]
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'unit_list.html'
