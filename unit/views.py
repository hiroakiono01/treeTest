from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import Unit
from django.urls import reverse_lazy
from django.contrib import messages
from unit.forms import UnitForm
from django.db import models


class UnitList(generic.ListView):
    paginate_by = 10
    context_object_name = 'unit_list'
    template_name = 'unit_list.html'
    model = Unit
    form_class = UnitForm

    def get_queryset(self):
        return Unit.objects.order_by('unit_no').all()


class UnitAdd(generic.FormView):
    model = Unit
    template_name = 'unit_add.html'
    form_class = UnitForm
    success_url = reverse_lazy('unit:unit_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, '単位を追加しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "単位の追加に失敗しました。")
        return super().form_invalid(form)


class UnitEdit(generic.UpdateView):
    model = Unit
    template_name = 'unit_edit.html'
    form_class = UnitForm

    def get_success_url(self):
        return reverse_lazy('unit:unit_list')

    def form_valid(self, form):
        messages.success(self.request, '単位を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "単位の更新に失敗しました。")
        return super().form_invalid(form)


class UnitDel(generic.DeleteView):
    model = Unit
    template_name = 'unit_del.html'

    def post(self, request, *args, **kwargs):

        try:
            obj = self.get_object()
            obj.delete()
            messages.success(self.request, "単位を削除しました。")
            return redirect('unit:unit_list')
        except models.ProtectedError as e:
            messages.error(request, f'「{obj}」は他で使われているため削除がきません。')
            return redirect('unit:unit_list')
