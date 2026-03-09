from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
# from rest_framework import renderers
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.renderers import JSONOpenAPIRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import EstimateDSerializer, UnitSerializer
from app.models import EstimateD, Unit

global estimate_no_counter, estimate_no_first

estimateD_counter = 1
global_param = ''


def index(request):
    return render(request, 'index.html')


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class FilterEstimateD(filters.FilterSet):
    estimate_no = filters.CharFilter(lookup_expr='iexact')
    id = filters.UUIDFilter()

    class Meta:
        model = EstimateD
        fields = ['estimate_no', 'id']


class EstimateDViewSet(viewsets.ModelViewSet):
    queryset = EstimateD.objects.all()
    serializer_class = EstimateDSerializer
    filter_backends = [DjangoFilterBackend]
    EstimateD.objects.rebuild()
    # lookup_field = 'id'
    # renderer_classes = [JSONOpenAPIRenderer, TemplateHTMLRenderer]
    # template_name = 'estimate_tree.html'

    def get_queryset(self):

        global estimateD_counter, global_param

        if estimateD_counter < 2:
            global_param = self.request.query_params
            if 'estimate_no' in global_param:
                estimate_no = global_param.get('estimate_no')
                estimateD_counter += 1
                queryset = EstimateD.objects.filter(estimate_no=estimate_no)
            if 'id' in global_param:
                key = global_param.get('id')
                estimateD_counter += 1
                queryset = EstimateD.objects.filter(id=int(key))
        else:
            if 'estimate_no' in global_param:
                estimate_no = global_param.get('estimate_no')
                queryset = EstimateD.objects.filter(estimate_no=estimate_no)
            if 'id' in global_param:
                key = global_param.get('id')
                queryset = EstimateD.objects.filter(id=int(key))
            estimateD_counter = 1
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({'success': True, 'data': [serializer.data]}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({'success': True, 'data': [serializer.data]}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # PATCH (データの一部更新)
    def patch(self, request, id):
        instance = get_object_or_404(EstimateD, id=id)
        # partial=True を指定するのがポイント
        serializer = EstimateDSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['DELETE'])
    def delete(self, request, *args, **kwargs):
        try:
            ids_to_delete = request.data.get('ids', [])  # Get list of identifiers from request data
            instances_to_delete = self.queryset.filter(id__in=ids_to_delete)
            instances_to_delete.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EstimateDDetail(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    """
    Retrieve, update or delete a snippet instance.
    """
    queryset = EstimateD.objects.all()
    serializer_class = EstimateDSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = EstimateD.objects.all()
        obj_id = self.request.query_params.get('id')
        if obj_id is not None:
            # ?id=xx があれば絞り込む
            queryset = queryset.filter(id=obj_id)
        return queryset

    # def get(self, request, id, format=None):
    #     estimateD = self.get_object(id)
    #     serializer = EstimateDSerializer(estimateD)
    #     return Response(serializer.data)

    # def put(self, request, id, format=None):
    #     estimateD = self.get_object(id)
    #     serializer = EstimateDSerializer(estimateD, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id=None, *args, **kwargs):
        estimateD = self.get_object(id)
        estimateD.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
