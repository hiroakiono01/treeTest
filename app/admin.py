from django.contrib import admin

from app.models import Estimate
from app.models import Task
from app.models import Unit
from app.models import Reference

admin.site.register(Estimate)
admin.site.register(Unit)
admin.site.register(Task)
admin.site.register(Reference)
