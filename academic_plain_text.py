from lxml import html
import os, re, requests, csv

def get_urls(website):
    """получает ссылки с веб-страницы"""
    urls_clear = [] #массив для будущих ссылок
    tree = html.parse(website)
    urls = tree.xpath(".//a")
    for url in urls:
        href = url.attrib
        if href.has_key('href')== True: #если в словаре есть ключ href
            urls_clear.append(href.get('href')) #достаю ссылку
    return urls_clear

def get_article(url, num):
    """1. вытаскивает с веб-страницы кусок html, содржащий словарную статью; записывает его в файл в отдельную папку
       2. формирует строку с информацией о статье для csv файла
       3. создаёт файл имя_статьи_plain_text.txt, в котором хранится текст статьи без html
       url - веб-страница словарной статьи
       num - порядковый номер статьи в каунтере"""
    page = requests.get(url)
    article_tree = html.fromstring(page.content)
    article_name = article_tree.xpath(".//dt[@itemprop='title']")[0].text #получаю название словарной статьи

    """path = './'+str(num) #создаю путь для новой папки
    os.mkdir(path) #создаю папку с этим путём
    os.chdir(path)#захожу в эту папку"""

    """file_name = article_name+'.txt'
    f = open(article_name, 'w', encoding = 'utf-8')#создаю файл для словарной статьи
    for elem in article_tree.xpath(".//*[@id='article']"):
        f.write(html.tostring(elem,encoding='unicode',))#записываю статью в файл
    f.close()"""

    plain_file_name = str(num)+'_plain_text.txt'
    f_plain = open(plain_file_name, 'w', encoding = 'utf-8')#создаю файл для словарной статьи
    texts = (article_tree.xpath(".//*[@id='article']//text()"))
    for text in texts:
        f_plain.write(text)
    f_plain.close()

    #os.chdir("..") #возвращаюсь в папку категории


    path = str(os.getcwd()+'/'+plain_file_name)
    source = article_tree.xpath(".//span[@itemprop='source']")[0].text
    year = article_tree.xpath(".//span[@itemprop='source-date']")[0].text
    language = 'ru'
    row_line = str(num),path,article_name,source, year, language
    print('file '+plain_file_name+' is processed')
    return row_line

def write_csv(df):
    """записывает информацию о статьях в csv файл"""
    with open('Dmitriev_info.csv', "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for raw in df:
            writer.writerow(raw)

os.mkdir('/Users/tatianagolovko/Documents/учёба/ВШЭ/Python/2/Dmitriev')
os.mkdir('/Users/tatianagolovko/Documents/учёба/ВШЭ/Python/2/Dmitriev/Dmitriev_plain_text')
os.chdir('/Users/tatianagolovko/Documents/учёба/ВШЭ/Python/2/Dmitriev/Dmitriev_plain_text')#папка, куда складывать словарь

#каунтеры:
count_articles_1 = 0 #подсчет статей в категории на 1 странице
count_aricles_2 = 0 #на второй странице
sum_1 = 0 #общее число статьей c первых страниц
sum_2 = 0 #со следующих страниц
cat_num =0 #число категорий
art_num = 1 #порядковый номер словарной статьи для записи в csv

#хранение данных:
articles2 = set()#ссылка на следующую страницу в коде попадается дважды; чтобы он два раза не обкачивал одни и те же
                #статьи, складываю уже просмотренные в это множество
df=[]#для хранения информации, которая будет записана в csv
header = 'number,path,title,source,year,language'.split(',')
df.append(header) #названия столбцов для csv файла


hrefs2 = get_urls("http://dic.academic.ru/contents.nsf/dmitriev/")#получаю массив ссылок со страницы
for href in hrefs2: #для каждой ссылки
    if re.match('http://dic.academic.ru/contents.nsf/dmitriev/\?f=',href)!= None: #если это ссылка на категорию
        cat_num+=1
        tree = html.parse(href)
        #cat_name = tree.xpath(".//*[@class='content']//h2")#извлекаю название категории
        path = './'+str(cat_num) #создаю путь для новой папки
        os.mkdir(path) #создаю папку с этим путём
        os.chdir(path)#захожу в эту папку
        hrefs3 = get_urls(href)# ищу все ссылки на странице категории
        for href in hrefs3: #для каждой ссылки со страницы категории
            if re.match('\?f=',href)!= None: #если это ссылка на следующую страницу
                next_urls = get_urls('http://dic.academic.ru/contents.nsf/dmitriev/'+href)#получаю все ссылки с неё
                for url in next_urls:
                    if re.match('http://dic.academic.ru/dic.nsf/dmitriev/\d', url)!= None and url not in articles2:#для каждой словарной статьи со второй страницы
                        info = get_article(url, art_num)#сохраняю словарные статьи и получаю информацию для csv
                        df.append(info)
                        articles2.add(url) #добавляю адрес в множество
                        art_num += 1 #увеличиваю порядковый номер статьи
                        count_aricles_2+=1
                sum_2 = sum_2 + count_aricles_2
                count_aricles_2 = 0
            if re.match('http://dic.academic.ru/dic.nsf/dmitriev/\d',href)!= None:#для каждой словарной статьи с первой страницы
                info = get_article(href, art_num)#сохраняю словарные статьи и получаю информацию для csv
                df.append(info)
                art_num += 1 #увеличиваю порядковый номер статьи
                count_articles_1+=1
        os.chdir("..") #возвращаюсь в корневую папку
        sum_1 = sum_1 + count_articles_1
        count_articles_1 = 0

write_csv(df)
print('ссылок на статьи с первых страниц: ', sum_1)
print('ссылок со вторых страниц: ', sum_2)
print ('обработано категорий: ', cat_num)

