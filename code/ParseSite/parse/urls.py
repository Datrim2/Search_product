#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------
#/ParseSite/parse/views/urls.py
#-------------------------------------------

from django.urls import path
from parse import views

app_name = 'parse'

urlpatterns = [
    # path('parse/',views.holodilnik,name="holodilnik"),
    path('wb/<int:pk>/',views.wb_new,name="wb"),
    path('wb_save/<int:pk>/<int:pk_wb>/<int:flag>',views.UpSaveWB.as_view(),name="wb_save"),
    path('wb_save_l/<int:pk_load>',views.wb_load,name="wb_load")
]