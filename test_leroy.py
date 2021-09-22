""" Работа через requests и selenium. """
# Необходимо попробовать ускорить процесс через asycio или thread. Подумать!!
import re
import pandas as pd
import datetime
from selenium import webdriver
import requests

def catalog(start):
    """ Получение страниц категорий. """
    start_time = datetime.datetime.now()
    driver.get(start)
    data = []
    file1 = open("D:/Kokoc/Projects/untitled1/каталог.txt", "w")
    for i in driver.find_elements_by_class_name("footer-slider-item-link"):
        if i.get_attribute("href") not in data:
            data.append(i.get_attribute("href"))
            file1.write(i.get_attribute("href") + "\n")
    end_time = datetime.datetime.now()
    print('catalog: {}'.format(end_time - start_time))
    print(len(data))
    return data

def thingsinpages(cat):
    """ Получение всех страниц товаров. """
    start_time = datetime.datetime.now()
    incite = []
    file2 = open("D:/Kokoc/Projects/untitled1/позиции.txt", "w")
    z = 1
    for i in cat:
        print(i, " ", z)
        z += 1
        driver.get(i)
        l = []
        try:
            driver.find_element_by_tag_name("uc-pagination")
            maximum = int(driver.find_element_by_tag_name("uc-pagination").get_attribute("total")) + 1
        except:
            maximum = 2
        for k in range(1, maximum):
            st = i + "?page=" + str(k)
            attempt = 1
            while attempt <= 5:
                try:
                    driver.get(st)
                    for y in driver.find_elements_by_class_name("plp-item__info__title"):
                        if y.get_attribute("href") not in incite:
                            incite.append(y.get_attribute("href"))
                            file2.write(y.get_attribute("href") + "\n")
                    attempt = 6
                except Exception as er:
                    attempt += 1
                    print("ОшибкаTh", " ", er)

    end_time = datetime.datetime.now()
    print('thingsinpages: {}'.format(end_time - start_time))
    print(len(incite))
    return incite

def expand_shadow_element(element):
  shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
  return shadow_root

def trypars(page, base):
    """ Получение информации со всех страниц, используя доступ к shadowroot. """
    if requests.get(page).status_code <= 400:
        rig = 1
        while rig <= 5:
            try:
                otchet = []
                nal = str()
                cat = str()
                otchet.append(page)
                driver.get(page)
                otchet.append(driver.find_element_by_tag_name("h1").text)
                print(driver.find_element_by_tag_name("h1").text)
                all_elems = driver.find_element_by_tag_name("uc-breadcrumbs-row")
                elems = all_elems.find_elements_by_tag_name("a")
                for i in elems:
                    cat += (re.sub("^\s+|\n|\r|\s+$", '', i.text)) + "/"
                otchet.append(cat)
                print(cat)
                for i in driver.find_elements_by_tag_name("span"):
                    if i.get_attribute("slot") == "article":
                        otchet.append(i.get_attribute("content"))
                    if i.get_attribute("slot") == "price":
                        otchet.append(i.text)
                root1 = driver.find_element_by_css_selector("uc-pdp-card-ga-enriched")
                shadow_root1 = expand_shadow_element(root1)
                elements = shadow_root1.find_elements_by_tag_name("uc-store-stock")
                for i in elements:
                    nal += i.text
                otchet.append(nal)
                base.append(otchet)
                rig = 6
            except Exception as ex:
                rig += 1
                print("ОшибкаTry", " ", ex)

def makeData(chto):
    """ Создание итогового файла. """
    df = pd.DataFrame(chto, columns=['Ссылка', 'Наименование', 'Категория', 'Цена', 'Артикул', 'Доступность'])
    df.to_excel("D:/Kokoc/Projects/untitled1/leroy.xls", index=False)

start_time = datetime.datetime.now()
driver = webdriver.Chrome("D:/Users/Kokoc/AppData/Local/Programs/Python/Python38/chromedriver.exe")
allthngs = []
time1 = datetime.datetime.now()
for k in thingsinpages(catalog("https://spb.leroymerlin.ru/")):
    trypars(k, allthngs)
time2 = datetime.datetime.now()
print('trypars: {}'.format(time2 - time1))
makeData(allthngs)
end_time = datetime.datetime.now()
driver.quit()
print('All: {}'.format(end_time - start_time))


