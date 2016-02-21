#задача: выкачать словарь Дмитриева 
import urllib.request
import re

article_urls = []

#получаем ссылки на разделы:
url = 'http://dic.academic.ru/contents.nsf/dmitriev/' 
con = urllib.request.urlopen(url)
page = con.read() #читаю главную страницу словаря;
page = page.decode('utf-8')
#ссылки на разделы выглядят однообразно, вытаскию их:
urls1 = re.findall ('<li><A HREF="(http://dic.academic.ru/contents.nsf/dmitriev/(?:.+?)nt=76)">',page)
print ('найдено ссылок на разделы: ', len(urls1))

#вытаскиваем ссылка на конкретные статьи:   
for url2 in urls1: 
    con2 = urllib.request.urlopen(url2)
    page2 = con2.read() #поочерёдно захожу в каждый раздел;
    page2 = page2.decode('utf-8')
#print (page2) - нет блока с ссылками
#в коде страницы отсутствуют ссылки на страницы о.О
    
 #   urls2 = re.findall('href="(http://dic.academic.ru/dic.nsf/dmitriev/(?:.+?))">', page2)
 #   for url in urls2:
 #       article_urls.append(url)
#print('найдено ссылок на статьи: ', len(article_urls))
