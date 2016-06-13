import re, lxml.html

f = open('cedict_ts.u8', 'r', encoding='utf-8')
inp = open('stal.xml', 'r', encoding='utf-8')
out = open('output.xml', 'w', encoding='utf-8')

lines = f.readlines()

"""Создаю словарь, в котором ключом является иероглиф в новом написании,
а в значении содержатся массивы, состоящие из всех возможных вариантов чтения и перевода"""

lines = lines[30:]#только слова
dictionary = {}
for line in lines:
    parts = line.split(' ')
    lex = parts[1] #само слово
    transcr = re.search('\[.*?\]', line).group(0)[1:-1] #выделяю целиком транскрипцию
    sem = re.search('/(.*)/', line).group(1) #выделяю все значения
    sem = sem.replace('/',', ')
    dict_line = [transcr, sem]
    if lex not in dictionary: #если слова нет в словаре, то добавляю
        dictionary[lex] = [dict_line]
    else: #иначе добавляю по ключу новое значение
        dictionary[lex].append(dict_line)
"""Достаю предложения из входного файла"""
text = inp.read()
sentences = re.findall('<se>(.*?)</se>', text)

"""Для каждого предложения ищу максимальную цепочку в словаре и принимаю это за токен,
    записываю значения токенов в xml"""
out.write('<?xml version="1.0" encoding="utf-8"?>\n<html>\n<body>')
punct = ['！', '。', '？', '，', '“', '”']
for sent in sentences:
    out.write('\n<se>')
    length = len(sent)#длина цепочки
    while length>0:
        if sent[0:length] in dictionary.keys():#если цепочка есть в словаре
            word = sent[0:length]#Значит, мы нашли слово
            text_out='\n<w>'
            for i in range(0, len(dictionary[word])):
                text_out = text_out+'<ana lex=\"'+word+'\" transcr=\"'+dictionary[word][i][0]+'\" sem=\"'+dictionary[word][i][1]+'\"/>'
            text_out = text_out + word + '</w>'
            out.write(text_out)#записываем его в файл
            sent = sent[length:]#и убираем из цепочки
            length = len(sent)
        elif sent[0] in punct:#знаки пунктуации переносим без изменений и удаляем из цепочки
            out.write(sent[0])
            sent = sent[1:]
            length = len(sent)
        else:#если соотвествия нет, уменьшаем длину цепочки и проходим цикл заново
            length-=1
    out.write('</se>')

out.write('</body>\n</html>')

f.close()
inp.close()
out.close()
