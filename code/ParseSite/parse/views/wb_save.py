from parse.models import Document, Product, WBProduct
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from django.http import HttpResponseNotFound, HttpResponse
from ..utils import queryset_to_workbook

class UpSaveWB(RedirectView):

    permanent = False
    pattern_name = 'parse:wb'

    def get_redirect_url(self, *args, **kwargs):
        tovar = get_object_or_404(Product, pk=kwargs['pk'])
        print(1)
        if tovar.document.user != self.request.user:
            return HttpResponseNotFound()
        # doc = get_object_or_404(Document,pk=tovar.document,user=self.request.user)
        if kwargs['flag']:
            tovar.is_done = True
            tovar.wbproduct_set.create(url = f"https://www.wildberries.ru/catalog/{kwargs['pk_wb']}/detail.aspx")
        else:
            tovar.is_done = True
        tovar.save()
        return super().get_redirect_url(tovar.document_id)
    
def wb_load(request,pk_load):
    data = WBProduct.objects.select_related("product__document").filter(product__document__pk=pk_load)
    columns = (
        'url',
        'product.citilink_id',
        )
    workbook = queryset_to_workbook(data, columns)
    # print(dir(workbook))
    # print(workbook)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="export.xls"'
    workbook.save(response)
    return response
    # response = HttpResponse(data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # response['Content-Disposition'] = 'attachment; filename=%s_Report.xlsx' % pk
    # return response
