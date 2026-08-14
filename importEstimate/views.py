from django.views import generic

from app.models import CurrentClient
from importEstimate.forms import ImportEstimateForm


class import_estimate(generic.FormView):
    template_name = 'importEstimate.html'
    form_class = ImportEstimateForm

    def get_initial(self):
        # Formにユーザーが処理しているクライアント名を送る
        initial = super().get_initial()
        client_link = CurrentClient.objects.filter(customUser=self.request.user).first()
        # データが存在する場合のみ初期値をセット（Noneエラー対策）
        if client_link and client_link.client:
            initial['client_name'] = client_link.client.client_name
        return initial
