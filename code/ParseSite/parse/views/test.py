# import requests

# url = "https://www.holodilnik.ru/search/?search=BOSH"

# headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}

# response = requests.get(url,headers=headers)

# import requests
# req = requests.Session()
# req.headers.update({"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"})
# res = req.get("https://www.holodilnik.ru/search/?search=BOSH",allow_redirects=True)

import requests
import re
import json
from bs4 import BeautifulSoup


req = requests.Session()
req.headers.update({"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"})
res = req.get("https://www.ozon.ru/search/?from_global=true&seller=0&text=kitfort+kt-1004-2")
soup = BeautifulSoup(res.content)
res = soup.find("div",attrs={'id':re.compile("state-searchResultsV2")})
res = res.attrs['data-state']
res = json.loads(res)
res["items"][0]["mainState"][0]["atom"]["price"]["price"]#цена
res["items"][0]["mainState"][2]["atom"]["textAtom"]["text"]#имя
res["items"][0]["mainState"][3]["atom"]["rating"]["action"]["link"]#ссылка
res["items"][0]["tileImage"]["images"]#изображение