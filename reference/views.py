from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import Unit, Reference
from django.urls import reverse_lazy
from django.contrib import messages

from reference.forms import ReferenceForm
from unit.forms import UnitForm
from django.db import models


class ReferenceList(generic.ListView):
    paginate_by = 10
    context_object_name = 'reference_list'
    template_name = 'reference_list.html'
    model = Reference
    form_class = ReferenceForm

    def get_queryset(self):
        return Reference.objects.all()


class ReferenceAdd(generic.FormView):
    model = Reference
    template_name = 'reference_add.html'
    form_class = ReferenceForm
    success_url = reverse_lazy('reference:reference_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, '単位を追加しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "単位の追加に失敗しました。")
        return super().form_invalid(form)


class ReferenceEdit(generic.UpdateView):
    model = Reference
    template_name = 'reference_edit.html'
    form_class = ReferenceForm

    def get_success_url(self):
        return reverse_lazy('reference:reference_list')

    def form_valid(self, form):
        messages.success(self.request, '単位を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "単位の更新に失敗しました。")
        return super().form_invalid(form)


class ReferenceDel(generic.DeleteView):
    model = Reference
    template_name = 'reference_del.html'

    def post(self, request, *args, **kwargs):

        try:
            obj = self.get_object()
            obj.delete()
            messages.success(self.request, "単位を削除しました。")
            return redirect('reference:reference_list')
        except models.ProtectedError as e:
            messages.error(request, f'「{obj}」は他で使われているため削除がきません。')
            return redirect('reference:reference_list')
