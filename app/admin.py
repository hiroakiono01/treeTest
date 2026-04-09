from django.contrib import admin

from app.models import Estimate
from app.models import Task
from app.models import Unit

admin.site.register(Estimate)
admin.site.register(Unit)
admin.site.register(Task)
