#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------
#/ParseSite/parse/views/views.py
#-------------------------------------------

from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
import html_text
# import json

def holodilnik(request):
    url = "https://www.citilink.ru/search/?text=1359289"
    
    headers = {
    'Cookie': '_space=msk_cl%3A; _tuid=93c62282ef00fc3f3287468c28cf5d6a4dde8181; ab_test=90x10v4%3A1%7Creindexer%3A2%7Cnew_designv10%3A1%7Cnew_designv13%3A1%7Cproduct_card_design%3A2%7Cwelcome_mechanics%3A3%7Cdummy%3A10; ab_test_analytics=90x10v4%3A1%7Creindexer%3A2%7Cnew_designv10%3A1%7Cnew_designv13%3A1%7Cproduct_card_design%3A2%7Cwelcome_mechanics%3A3%7Cdummy%3A10; is_show_welcome_mechanics=1; old_design=0'
    }
    
    response = requests.get(url,headers=headers,  timeout=(3.05, 100))
    # soup = BeautifulSoup(response.text, 'lxml')
    # response=(soup.title)
    # el = soup.find("script", {"type":"application/ld+json"})
    # response = eval(el.text.strip())
    
    # url = response["offers"]["url"]
    # print(response)
    # print('-'*30)
    # del(response,el,soup)
    
    # response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    images_citilink = iter( link.get("src") for link in soup.find_all("img",{"class":"PreviewList__image Image"}))
    first_image_citilink = next(images_citilink)
    el = soup.find("script", {"type":"application/ld+json"})
    response = eval(el.text.strip())
    print(response)
    
    if('brand' in response and "mpn" in response):
        search_name = f'{response["brand"]} {response["mpn"]}'
    else:
        search_name = response["name"].split(',')[0]
    print(search_name)
    #url = f'https://autocomplete.diginetica.net/autocomplete?st={search_name}&apiKey=BZQ1NIP98I'
    url = f'https://www.holodilnik.ru/search/?search_provider=anyquery&strategy=vectors_advanced,zero_queries&search={search_name}'
    response_url = requests.get(url)
    # res_json = response_url.json()
    print(response_url.text)
    # products = res_json['products']
    # image_url = [ el['image_url'] for el in res_json['products']]
        
    return render(request, "parse/holodilnik.html", locals())
