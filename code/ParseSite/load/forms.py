#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------
#/ParseSite/load/forms.py
#-------------------------------------------
from django import forms
import pandas as pd
from parse.models import Document, Product, Store
from load.tasks import load_data_to_db

class FormUploadFile(forms.Form):
          
    title = forms.CharField(max_length=50, required=False, label='Имя файла:')
    file = forms.FileField(label='Файл:')
    story = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Store.objects.all(),
        label = "Магазин"
    )
    
    def load(self,user):
        # -- Считывание загружаемого файла --
            # файл считывается с временного хранилища, которое было настроенно в settings
        doc = pd.read_excel(io = self.cleaned_data.get('file').open(), engine='openpyxl')#.drop(labels=[0],axis=0)
        # -- Замена заголовков --
            # Забираем вторую строку в excel
        new_headers = doc.iloc[0]
            # Убираем ее в DataFrame
        doc = doc[1:]
            # Присваиваем как заголовки столбцов
        doc.columns = new_headers
        
        # -- Добавляем данные в базу --
            # Создаем загружаемый лист
        document = Document.objects.create(doc_name =(self.cleaned_data.get('title') if self.cleaned_data.get('title') else self.cleaned_data.get('file').name)
                                          ,user=user)
        document.store_set.add(*self.cleaned_data.get('story'))
        document.save()
            # Проходим по элементам DataFrame делаем срез столбоцов
            # left(ID,товар) right(ID,Вайлдберриз)
        for _,value in pd.merge(left = doc.iloc[:, 1:3],right=doc[['ID для проверки','ВАЙЛДБЕРРИЗ ООО']]).iterrows():
            if value[2].replace(" ","")=='-':
                # Добавляем товар к листу
                short_name = (value[1].split(',')[0])
                tovar = Product.objects.create(document=document,citilink_id=value[0],product_name=value[1],search_name= short_name[:short_name.rfind('-')] if short_name.count('-') > 1 else short_name)
                tovar.save()
                
        load_data_to_db.delay(document.pk)

