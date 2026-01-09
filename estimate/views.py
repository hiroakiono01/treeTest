from django.contrib import messages
from django.db import models
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

# from estimate.forms import SearchEstimateForm
from app.models import Estimate
from estimate.forms import EstimateAddForm


class EstimateList(generic.ListView):
    """ 見積一覧表　照会画面 """
    context_object_name = 'estimate_list'
    template_name = 'estimate_list.html'
    model = Estimate

    def get_queryset(self):
        estimate = Estimate.objects.all()
        return estimate


class EstimateAdd(generic.CreateView):
    template_name = 'estimate_add.html'
    success_url = reverse_lazy('estimate:estimate_list')
    form_class = EstimateAddForm

    def form_valid(self, form):
        messages.success(self.request, 'create estimate')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "invalid estimate")
        return super().form_invalid(form)


class EstimateEdit(generic.UpdateView):
    model = Estimate
    template_name = 'estimate_edit.html'
    success_url = reverse_lazy('estimate:estimate_list')
    form_class = EstimateAddForm

    def form_valid(self, form):
        messages.success(self.request, 'edit estimate')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "invalid estimate")
        return super().form_invalid(form)


class EstimateDel(generic.DeleteView):
    model = Estimate
    template_name = 'estimate_del.html'

    def post(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            obj.delete()
            messages.success(self.request, "delete estimate")
            return redirect('estimate:estimate_list')
        except models.ProtectedError as e:
            messages.error(request, f'「{obj}」estimate use other')
            return redirect('estimate:estimate_list')


def test_page(request):
    return render(request, 'testPage.html')


def estimate_tree(request):
    return render(request, 'estimate_tree.html')
