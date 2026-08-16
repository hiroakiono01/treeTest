from django.urls import reverse_lazy
from django.views import generic

from app.models import CurrentClient
from importEstimate.forms import ImportEstimateForm
from importEstimate.addExcelEstimate import upload_Eecel_Estimate


class import_estimate(generic.FormView):
    template_name = 'importEstimate.html'
    form_class = ImportEstimateForm
    success_url = reverse_lazy('importEstimate:complete')

    def get_initial(self):
        # Formにユーザーが処理しているクライアント名を送る
        initial = super().get_initial()
        client_link = CurrentClient.objects.filter(customUser=self.request.user).first()
        # データが存在する場合のみ初期値をセット（Noneエラー対策）
        if client_link and client_link.client:
            initial['client_name'] = client_link.client.client_name
        return initial

    def form_valid(self, form):
        excel_file = self.request.FILES.get("file")
        result = upload_Eecel_Estimate(excel_file)


# 変換処理完了
class complete(generic.TemplateView):
    template_name = 'complete.html'
