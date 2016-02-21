from lxml import html
import os
import urllib.request
import re

def get_urls(website):
    urls_clear = [] #массив для будущих ссылок
    tree = html.parse(website)
    urls = tree.xpath(".//a")
    #print('найдено ссылок на странице: ', len(urls))
    for url in urls:
        href = url.attrib
        if href.has_key('href')== True: #если в словаре есть ключ href
            urls_clear.append(href.get('href')) #достаю ссылку
    return urls_clear

os.chdir('/Users/tatianagolovko/Documents/учёба/ВШЭ/Python/2/Dmitriev')#папка, куда складывать словарь
cat_name = 1 #каунтер для папок с категориями, временно, надо заменить на имя категории


count_articles_1 = 0 #подсчет статей в категории на 1 странице
count_aricles_2 = 0 #на второй странице
sum_1 = 0 #общее число статьей c первых страниц
sum_2 = 0 #со следующих страниц
cat_num =0 #число категорий
articles2 = set()#ссылка на следующую страницу в коде попадается дважды; чтобы он два раза не обкачивал одни и те же
                #статьи, складываю уже просмотренные в это множество

hrefs2 = get_urls("http://dic.academic.ru/contents.nsf/dmitriev/")#получаю массив ссылок со страницы
for href in hrefs2: #для каждой ссылки
    if re.match('http://dic.academic.ru/contents.nsf/dmitriev/\?f=',href)!= None: #если это ссылка на категорию

        path = './'+str(cat_name) #создаю путь для новой папки
        os.mkdir(path) #создаю папку с этим путём
        cat_name+=1 #увеличиваю каунтер

        hrefs3 = get_urls(href)# ищу все ссылки на странице категории
        for href in hrefs3: #для каждой ссылки со страницы категории
            if re.match('\?f=',href)!= None: #если это ссылка на следующую страницу
                next_urls = get_urls('http://dic.academic.ru/contents.nsf/dmitriev/'+href)#получаю все ссылки с неё
                for url in next_urls:
                    if re.match('http://dic.academic.ru/dic.nsf/dmitriev/\d', url)!= None and url not in articles2:#для каждой словарной статьи со второй страницы
                        articles2.add(url) #добавляю адрес в множество
                        count_aricles_2+=1
                sum_2 = sum_2 + count_aricles_2
                count_aricles_2 = 0
            if re.match('http://dic.academic.ru/dic.nsf/dmitriev/\d',href)!= None:#для каждой словарной статьи с первой страницы
                count_articles_1+=1
        sum_1 = sum_1 + count_articles_1
        count_articles_1 = 0
        cat_num+=1
print('ссылок на статьи с первых страниц: ', sum_1)
print('ссылок со вторых страниц: ', sum_2)
print ('обработано категорий: ', cat_num)





#в urls лежат словари
