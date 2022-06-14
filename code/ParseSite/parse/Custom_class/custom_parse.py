import requests
import re
import json
from bs4 import BeautifulSoup
from parse.models import Product, DataResourse, Store

# Обязательные поля в data:
# 

class Parse():
    
    data = []
    error = {}
    sess = requests.Session()
    
    def __init__(self):
        self.sess.headers.update({"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"})

    def keys_exists(self,element, *keys):

        if not isinstance(element, dict):
            raise AttributeError('keys_exists() expects dict as first argument.')
        if len(keys) == 0:
            raise AttributeError('keys_exists() expects at least two arguments, one given.')

        _element = element
        for key in keys:
            try:
                _element = _element[key]
            except KeyError:
                return False
        return True
    
class ParseWB(Parse):
    def data_link(self,search_name,pk):
        pass
    
class ParseCitilink(Parse):
    
    data = {}
    
    def data_link(self,search_name):
        # выполняем запрос к интернет магазину
        response = self.sess.get('http://localhost:8050/render.html',
                                 params={'url': f"https://www.citilink.ru/search/?text={search_name}", 'wait': 2})
        # добавление адреса, для перехода на странице
        self.data["citilink_url"] = response.url
    # -- Поиск данных --
        # Создаем экземпляр класса BeautifulSoup для поиска тегов
        soup = BeautifulSoup(response.text, 'lxml')
        # Собираем изображения со страницы
        try:
            self.data["images_citilink"] = enumerate([ link.get("src") for link in soup.find_all("img",{"class":"PreviewList__image Image"}) ])
            el = soup.find("script", {"type":"application/ld+json"})
            self.data["response_citilink"] = eval(el.text.strip())
        except AttributeError as ex:
            print(ex)
    
class ParseOzon(Parse):
    
    def data_link(self,pk):
        dataRowsTopic = Product.objects.get(pk=pk)
        response = self.sess.get(f"https://www.ozon.ru/search/?from_global=true&seller=0&text={dataRowsTopic.search_name.replace(' ', '+')}")
        print(response.url)
        soup_content = BeautifulSoup(response.content,"html.parser")
        soup_content = soup_content.find("div",attrs={'id':re.compile("state-searchResultsV2")})
        data_JSON = json.loads(soup_content.attrs['data-state'])
        f = open("1.json","w",encoding="utf-8")
        f.write(soup_content.attrs['data-state'])
        f.close()
        for elements in data_JSON["items"]:
            if self.keys_exists(elements,"mainState",0,"atom","price","price") and self.keys_exists(elements,"action","link") and self.keys_exists(elements,"tileImage","images"):
                for elem in elements["mainState"]:
                    if elem["id"] == "name":
                        name_product = elem["atom"]["textAtom"]["text"] 
                self.data.append({"pk_product" : pk,
                              "cost" : elements["mainState"][0]["atom"]["price"]["price"],
                              "name" : name_product,
                              "link" : elements["action"]["link"],
                              "images" : elements["tileImage"]["images"],})
            else:
                self.data={}
                self.error["Error"] = "Не верный JSON на сайте ozon"
            