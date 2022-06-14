#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------
#/ParseSite/parse/views/views.py
#-------------------------------------------

from django.shortcuts import render
from parse.models import Document, DataResourse, Store
from django.shortcuts import get_object_or_404
from parse.Custom_class import ParseCitilink

def wb_new(request,pk):
    # -- Обращение к базе --
        # проверяем наличие загружаемого листа
    doc = get_object_or_404(Document, pk=pk, user=request.user)
    # выбираем все найденные связи
    tovar = DataResourse.objects.select_related("product").filter(product__is_done=False,product__document=doc).filter(store=Store.objects.get(name="WILDBERRIES"))
        # если пусто то возвращаем страницу загрузки
    if not tovar:
        return render(request, "parse/wb_done.html", {"pk":pk})
    else:
        tovar = tovar[0]
        # подсчет количества проверяемых товаров
    all_data = len(doc.product_set.all())
        # подсчет количества проверенных товаров
    kol_prov = all_data-len(doc.product_set.all().filter(is_done=False))
    # -- Запрос к Citilink --
    citilink_data = ParseCitilink()
    citilink_data.data_link(tovar.product.citilink_id)
    # сохраняем заранее обработанные данные
    product_elems = tovar.data
    
    
    return render(request, "parse/wb.html", locals())