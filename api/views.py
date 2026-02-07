from rest_framework import viewsets
from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework.renderers import TemplateHTMLRenderer

from api.serializers import EstimateDSerializer, UnitSerializer
from app.models import EstimateD, Unit



class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class EstimateDViewSet(viewsets.ModelViewSet):
    serializer_class = EstimateDSerializer
    renderer_classes = [JSONOpenAPIRenderer, TemplateHTMLRenderer]
    template_name = 'estimate_tree.html'
    EstimateD.objects.rebuild()

    def get_queryset(self):
        # estimate_no = self.kwargs.get('estimate_no')
        estimate_no = '002'
        if estimate_no is not None:
            queryset = EstimateD.objects.filter(estimate_no=estimate_no)
            return queryset

    # def create(self, request, *args, **kwargs):
    #     try:
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_create(serializer)
    #         return Response({'success': True, 'data': [serializer.data]}, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #
    # def update(self, request, *args, **kwargs):
    #     try:
    #         partial = kwargs.pop('partial', False)
    #         instance = self.get_object()
    #         serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_update(serializer)
    #         return Response({'success': True, 'data': [serializer.data]}, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #
    # @action(detail=False, methods=['DELETE'])
    # def delete(self, request, *args, **kwargs):
    #     try:
    #         ids_to_delete = request.data.get('ids', [])  # Get list of identifiers from request data
    #         instances_to_delete = self.queryset.filter(pk__in=ids_to_delete)
    #         instances_to_delete.delete()
    #         return Response({'success': True}, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
