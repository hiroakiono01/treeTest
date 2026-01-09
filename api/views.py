from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import EstimateDSerializer
from app.models import Estimate, EstimateD


def estimate_tree(request):
    return render(request, 'estimate:estimate_tree.html')


def test_page(request):
    return render(request, 'testPage.html')


class EstimateDViewSet(viewsets.ModelViewSet):
    queryset = EstimateD.objects.all()
    serializer_class = EstimateDSerializer

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

    @action(detail=False, methods=['DELETE'])
    def delete(self, request, *args, **kwargs):
        try:
            ids_to_delete = request.data.get('ids', [])  # Get list of identifiers from request data
            instances_to_delete = self.queryset.filter(pk__in=ids_to_delete)
            instances_to_delete.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
