from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from app.models import CurrentClient
from importEstimate.addExcelEstimate import upload_excel_estimate
from importEstimate.forms import ImportEstimateForm


class import_estimate(generic.FormView):
    template_name = 'importEstimate.html'
    form_class = ImportEstimateForm
    success_url = reverse_lazy('importEstimate:complete')

    def get_initial(self):
        # Formにユーザーが処理しているクライアント名を送る
        initial = super().get_initial()
        currentClient = CurrentClient.objects.filter(customUser=self.request.user).first()
        # client_obj = currentClient.client if currentClient else None

        # データが存在する場合のみ初期値をセット（Noneエラー対策）
        if currentClient and currentClient.client:
            initial['client_name'] = currentClient.client.client_name
            initial['client_pk'] = currentClient.client.pk
        return initial

    def form_valid(self, form):
        excel_file = self.request.FILES.get("file")
        result = upload_excel_estimate(excel_file, form)

        return render(self.request, 'complete.html')


# 変換処理完了
class complete(generic.TemplateView):
    template_name = 'complete.html'
