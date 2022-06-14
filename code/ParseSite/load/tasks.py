from ParseSite.celery import app
from parse.models import Product, DataResourse, Store
from parse.Custom_class import ParseOzon
import requests

@app.task(ignore_result=True)
def load_data_to_db(id_document):
    dataRowsTopic = Product.objects.filter(document=id_document)
    for element in dataRowsTopic:
        url = f'https://wbxsearch.wildberries.ru/exactmatch/v2/common?query={element.search_name}'
        params_search = requests.get(url)
        params_search = params_search.json()
        if not params_search:
            element.is_done = True
            element.save()
            continue
        url = f'https://wbxcatalog-ru.wildberries.ru/{params_search["shardKey"]}/catalog?spp=0&regions=75,64,83,4,38,30,33,70,71,22,31,66,40,82,1,80,68,48,69&stores=117673,122258,122259,125238,125239,125240,507,3158,117501,120602,120762,6158,121709,124731,130744,159402,2737,117986,1733,686,132043&pricemarginCoeff=1.0&reg=0&appType=1&offlineBonus=0&onlineBonus=0&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=12,3,18,15,21&dest=-1029256,-102269,-2162196,-1257786&{params_search["query"]}'
        product_search = requests.get(url)
        product_search = product_search.json()
        
        product_elems = []
        
        for elem in product_search["data"]["products"]:
            url = f'https://wbx-content-v2.wbstatic.net/sellers/{elem["id"]}.json?locale=ru'
            response_url_wb_org = requests.get(url,timeout=3)
            response_url_wb_org = response_url_wb_org.json()
            if(response_url_wb_org['supplierId'] == 32477):
                product_elems.append({'pk_product': element.pk,
                                    'id':elem['id'], 
                                    'name': elem['name'],
                                    'priceU': str(elem['priceU'])[0:-2], 
                                    'salePriceU': str(elem['salePriceU'])[0:-2],
                                    'pics': [{url_img+1: f'https://images.wbstatic.net/c516x688/new/{str(elem["id"])[:-4]+"0000"}/{elem["id"]}-{url_img+1}.jpg'} for url_img in range(elem['pics'])],
                                    'colors': (el['name'] for el in elem['colors']),
                                    'supplierName': response_url_wb_org['supplierName'],})
        if product_elems:
            element.dataresourse_set.create(data=product_elems,store=Store.objects.get(name="WILDBERRIES"))
            element.save()
        else:
            element.is_done = True
            element.save()
    dataRowsTopic.status = 1
    dataRowsTopic.save()

@app.task(ignore_result=True)
def load_data_ozon(id_document):
    pass
#celery -A ParseSite worker -l INFO --purge -P eventlet