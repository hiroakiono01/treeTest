# from rest_framework import renderers
# from rest_framework import renderers
# from rest_framework import renderers
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.models import Estimate, CurrentClient, Client, Fiscalyear, Customer, Segment, Construction, User, Unit, Aggregation


def index(request):
    return render(request, 'index.html')


@api_view(['GET'])
def get_unit_options(_request, client_id, use_flg):
    # combobox の場合はid,valueでselectは使えない
    if use_flg == "0":
        units = Unit.objects.all().filter(client_id=client_id, use_flg=use_flg).order_by('unit_no')
    else:
        units = Unit.objects.all().filter(client_id=client_id).order_by('unit_no')
    unit_options = [
        {
            "id": unit.id,  # 文字型として代入
            "value": unit.unit_name  # 文字列型（表示名）
        }
        for unit in units
    ]
    return Response({"units": unit_options})


def get_unit_pk(client_id, unit_name):
    unit = Unit.objects.filter(client_id=client_id, unit_name=unit_name).first()
    return unit.id if unit else None


def get_user_pk(client_id, user_name):
    user = User.objects.filter(client_id=client_id, user_name__icontains=user_name).first()
    return user.id if user else None


@api_view(['GET'])
def get_aggr_options(_request, client_id):
    # combobox の場合はid,valueでselectは使えない
    aggr_options = [
        {
            "id": aggregation.id,  # 文字型として代入
            "value": aggregation.aggregation_name  # 文字列型（表示名）
        }
        for aggregation in Aggregation.objects.order_by("aggregation_no").filter(client_id=client_id).all()
    ]
    return Response({"aggregations": aggr_options})


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
        currentClient = CurrentClient.objects.filter(customUser=self.user).first()
        client = Client.objects.get(pk=currentClient.client_id)
        result = {'client_id': client.id,
                  'client_no': client.client_no,
                  'client_name': client.client_name,
                  'markup_rate': client.markup_rate,
                  }
        return JsonResponse({'current-client': result})
    except Exception:

        result = {'client_id': '',
                  'client_no': '',
                  'client_name': '選択されていません',
                  'markup_rate': '',
                  }

    return JsonResponse({'current-client': result}, status=404)


def get_estimate_name(_request, client_id, estimate_no):
    # GETパラメータから 'estimate_no' を取得
    # est_no = request.GET.get(estimate_no, client_id, None)

    # if est_no:
    estimate = Estimate.objects.filter(estimate_no=estimate_no, client_id=client_id).first()
    if estimate:
        return JsonResponse({'estimate_name': estimate.estimate_name, 'estimateId': estimate.pk})

    else:
        return JsonResponse({'estimate_name': ''}, status=404)


def get_fiscalyears(_request, client_id):
    # データベースから全年度を取得
    years = Fiscalyear.objects.all().filter(client_id=client_id).order_by('-id')  # 必要に応じてソート

    # DHTMLXのComboが要求する形式 [ {"value": "X", "content": "Y"}, ... ] に整形
    data = [
        {
            "id": str(year.id),
            "value": str(year.fiscalyear_name),  # 画面に表示したい名称のフィールド（例: 2026年度）
            "fiscalyear": str(year.fiscalyear_name)
        }
        for year in years
    ]

    return JsonResponse(data, safe=False)


@api_view(['GET'])
def get_fiscalyear_options(_request, client_id):
    fiscalyear_options = [
        {
            "id": item.id,
            "value": item.fiscalyear_name
        }
        for item in Fiscalyear.objects.all().filter(client_id=client_id).order_by('-id')
    ]
    return Response({"fiscalyears": fiscalyear_options})


@api_view(['GET'])
def get_user_options(_request, client_id, use_flg):
    if use_flg == "0":
        users = User.objects.all().filter(client_id=client_id, use_flg=use_flg).order_by('user_no')  # 必要に応じてソート
    else:
        users = User.objects.all().filter(client_id=client_id).order_by('user_no')  # 必要に応じてソート
    user_options = [
        {
            "id": item.id,
            "value": item.user_name
        }
        for item in users
    ]
    return Response({"users": user_options})


# def get_users(_request, client_id, use_flg):
#     if use_flg == "0":
#         users = User.objects.all().filter(client_id=client_id, use_flg=use_flg).order_by('user_no')  # 必要に応じてソート
#     else:
#         users = User.objects.all().filter(client_id=client_id).order_by('user_no')  # 必要に応じてソート
#     data = [
#         {
#             "id": str(user.id),
#             "value": str(user.user_name)
#         }
#         for user in users
#     ]
#     return JsonResponse(data, safe=False)

@api_view(['GET'])
def get_customer_options(_request, client_id, use_flg):
    if use_flg == "0":
        customers = Customer.objects.all().filter(client_id=client_id, use_flg=use_flg).order_by('customer_no')  # 必要に応じてソート
    else:
        customers = Customer.objects.all().filter(client_id=client_id).order_by('customer_no')  # 必要に応じてソート
    customer_options = [
        {
            "id": str(customer.id),
            "value": str(customer.customer_name)
        }
        for customer in customers
    ]
    return Response({"customers": customer_options})


@api_view(['GET'])
def get_segment_options(_request, client_id, use_flg):
    if use_flg == "0":
        segments = Segment.objects.all().filter(client_id=client_id, use_flg=use_flg).order_by('segment_no')  # 必要に応じてソート
    else:
        segments = Segment.objects.all().filter(client_id=client_id).order_by('segment_no')  # 必要に応じてソート

    segment_options = [
        {
            "id": str(segment.id),
            "value": str(segment.segment_name)
        }
        for segment in segments
    ]
    return Response({"segments": segment_options})


@api_view(['GET'])
def get_construction_options(_request, client_id):
    constructions = Construction.objects.all().filter(client_id=client_id).order_by('construction_no')  # 必要に応じてソート
    construction_options = [
        {
            "id": str(construction.id),
            "value": str(construction.construction_name)
        }
        for construction in constructions
    ]
    return Response({"constructions": construction_options})

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
