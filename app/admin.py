from django.contrib import admin
from tree_queries.admin import TreeAdmin

from app.models import Estimate
from app.models import EstimateD
from app.models import Unit

admin.site.register(Estimate)
admin.site.register(Unit)


@admin.register(EstimateD)
class EstimateDAdmin(TreeAdmin):
    list_display = [*TreeAdmin.list_display, "detail_name"]
    position_field = "position"
