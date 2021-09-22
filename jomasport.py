""" Работа через BeautifulSoup"""
# Необходимо попробовать ускорить процесс через asycio или thread. Подумать!!
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd

def parsermy(url, dataset, notthing):
    """ Получение всех страниц товаров. """
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
    if bsObj.find("div", class_="product-descr-wrap") is not None:
        if url not in dataset:
            dataset.add(url)
    for i in bsObj.find_all("a", {"href": re.compile("\/catalog\/[a-z0-9-\/]+")}):
        if ("http://jomasports.kz" + i["href"]) not in notthing:
            notthing.add("http://jomasports.kz" + i["href"])

def parsmain(ad, base):
    """ Получение информации со страниц товаров. """
    html = urlopen(ad)
    bsObj = BeautifulSoup(html, "html.parser")
    otchet = []
    otchet.append(ad)
    categ = bsObj.find("ul", class_="uk-breadcrumb").find_all("a", {"href": re.compile("[a-z0-9\/]*\/")})
    category = str()
    for k in categ:
        category += k.get_text() + "/"
    category += bsObj.find("ul", class_="uk-breadcrumb").find("li", class_="uk-active").get_text()
    otchet.append(category)
    name = bsObj.find("h1").get_text().replace("\n", "").lstrip(" ").rstrip(" ")
    otchet.append(str(name))
    price = float(bsObj.find("div", class_="prod_price").find("span").get_text()[:-2].replace(" ", ""))
    otchet.append(price)
    image = str()
    imag = bsObj.find("div", class_="jshop_img_description").find("span", id="list_product_image_thumb").find_all("img",
                                                            {"src": re.compile("\/upload\/images\/small\/[0-9_]+\.jpg")})
    for i in imag:
        image += ("http://jomasports.kz" + i["src"]) + " "
    otchet.append(str(image))
    articul = bsObj.find("span", class_="art-main").get_text()
    otchet.append(articul)
    if bsObj.find("div", class_="jshop_img_description").findPrevious("b").get_text() == "Состав:":
        inform = bsObj.find("div", class_="product-descr-wrap").find_all("p")
        sostav = inform[2].get_text().split(" ")
        izch = str()
        for i in sostav:
            if i != "Состав:" and i != "":
                izch += i + " "
        otchet.append(str(izch.strip(" ")))
    else:
        otchet.append("-")
    descr = bsObj.find("div", class_="jshop_prod_description").get_text().replace("\n", '')
    otchet.append(descr)
    base.append(otchet)

def makeData(chto):
    """ Создание итогового файла. """
    df = pd.DataFrame(chto, columns=['Ссылка', 'Категория', 'Наименование', 'Цена', 'Фото', 'Артикул', 'Состав', 'Описание'])
    df.to_excel("C:/Users/Артур/PycharmProjects/untitled1/jomasport.xls", index=False)

start = "http://jomasports.kz/"
pages = set()
net = set()
parsermy(start, pages, net)
urlpages = set()
for i in net:
    parsermy(i, pages, urlpages)
newpages = set()
for i in urlpages:
    parsermy(i, pages, newpages)
pppg = set()
for i in newpages:
    parsermy(i, pages, pppg)
sum = []
for i in pages:
    parsmain(i, sum)
makeData(sum)

