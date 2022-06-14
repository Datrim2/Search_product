#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------
#/ParseSite/load/views.py
#-------------------------------------------
from django.urls import reverse,reverse_lazy
from load.forms import FormUploadFile
from django.http import HttpResponseRedirect,Http404
from django.shortcuts import get_object_or_404

from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from parse.models import Document, Product

class UploadFile(FormView):
    template_name = 'load/load_file.html'
    form_class = FormUploadFile
    success_url = 'load:file'

    def form_valid(self, form):
        form.load(self.request.user)
        return HttpResponseRedirect(reverse(self.get_success_url()))

class History(ListView):
    template_name = 'load/history.html'
    model = Document
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(user=self.request.user)
    
class DocumentDetail(ListView):
    template_name = 'load/history_detail.html'
    model = Product
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        pk = self.kwargs['pk']
        doc = get_object_or_404(Document, pk=pk, user=self.request.user)
        return qs.filter(document=doc)
    
# class DocumentDelete(DeleteView):
#     model = Document
#     success_url = 'load:history'
 
#     def delete(self, request, *args, **kwargs):
#        self.object = self.get_object()
#        print(self.object)
#        if self.object.user == request.user:
#           self.object.delete()
#           return HttpResponseRedirect(reverse(self.get_success_url()))
#        else:
#           raise Http404
def documentdelete(request,pk):
    doc = get_object_or_404(Document, pk=pk, user=request.user)
    doc.delete()
    return HttpResponseRedirect(reverse("load:history"))