from django.contrib import messages
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from app.models import DetailMaster
from detailMaster.forms import DetailMasterForm


class DetailMasterList(generic.ListView):
    paginate_by = 10
    context_object_name = 'detailMaster_list'
    template_name = 'detailMaster_list.html'
    model = DetailMaster
    form_class = DetailMasterForm

    def get_queryset(self):
        return DetailMaster.objects.all()


class DetailMasterAdd(generic.FormView):
    model = DetailMaster
    template_name = 'detailMaster_add.html'
    form_class = DetailMasterForm
    success_url = reverse_lazy('detailMaster:detailMaster_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'add Detail Master')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "fail Detail Master")
        return super().form_invalid(form)


class DetailMasterEdit(generic.UpdateView):
    model = DetailMaster
    template_name = 'detailMaster_edit.html'
    form_class = DetailMasterForm

    def get_success_url(self):
        return reverse_lazy('detailMaster:detailMaster_list')

    def form_valid(self, form):
        messages.success(self.request, 'update Detail Master')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "fail Detail Master")
        return super().form_invalid(form)


class UDetailMasterDel(generic.DeleteView):
    model = DetailMaster
    template_name = 'detailMaster_del.html'

    def post(self, request, *args, **kwargs):

        try:
            obj = self.get_object()
            obj.delete()
            messages.success(self.request, "delete")
            return redirect('detailMaster:detailMaster_list')
        except models.ProtectedError as e:
            messages.error(request, f'「{obj}」other use')
            return redirect('detailMaster:detailMaster_list')
