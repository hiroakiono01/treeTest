from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from app.models import Estimate
from app.models import EstimateD
from app.models import Unit

admin.site.register(Estimate)
admin.site.register(Unit)

admin.site.register(
    EstimateD,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        'id',
        'estimate_no',
        'detail_name',
        'tree_seq',
        'parentId',
        'parentIndex',
        'tree_id',
        'level',
        'lft',
        'rght',
    ),
    list_disple_link=(
        'indented_title',
    ),

)
