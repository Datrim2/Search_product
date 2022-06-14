#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------
#/ParseSite/load/urls.py
#-------------------------------------------

from django.urls import path
from load import views

app_name = 'load'

urlpatterns = [
    path('',views.UploadFile.as_view(),name="file"),
    path('history/',views.History.as_view(),name="history"),
    path('history/<int:pk>/',views.DocumentDetail.as_view(),name="document"),
    path('history/<int:pk>/delete',views.documentdelete,name="delete"),
]