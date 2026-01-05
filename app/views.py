import logging

from django.views import generic

logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView, generic.View):
    """ ホーム画面 """
    template_name = "index.html"
