from django.contrib import admin
from app.models import Client
from app.models import User
from app.models import Process
from app.models import Customer
from app.models import Estimate
from app.models import Task
from app.models import Unit
from app.models import Construction
from app.models import Reference
from app.models import CurrentClient

admin.site.register(Client)
admin.site.register(User)
admin.site.register(Process)
admin.site.register(Customer)
admin.site.register(Estimate)
admin.site.register(Unit)
admin.site.register(Construction)
admin.site.register(Task)
admin.site.register(Reference)
admin.site.register(CurrentClient)
