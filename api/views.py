from django.shortcuts import render
# from rest_framework import renderers
from django.shortcuts import render
# from rest_framework import renderers
from rest_framework import viewsets

from api.serializers import UnitSerializer
from app.models import Unit


def index(request):
    return render(request, 'index.html')


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
