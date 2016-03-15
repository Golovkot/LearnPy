f1 = open ('alph.csv', 'r', encoding = "UTF-8")
f2 = open ('alph-res.txt', 'w', encoding = 'UTF-8')
f3 = open ('text.txt', 'r', encoding = "UTF-8")

adict = {} #создаём пустой словрь
for line in f1: #построчно перебираем csv
    arr = line.split(';') 
    adict[arr[0]] = arr[2] #записываем в словарь пары, где ключ - символ грузиницы, значение – символ IPA
#print (adict)   
for line in f3: #открываем текст на грузинице
    for i in line: #смотрим на него посимвольно
        if i in adict.keys(): #если символ – буква
            f2.write(adict[i]) #записываем в конечный файл эту букву в IPA
        else:
            f2.write(i) #если это другой символ, переносим без изменений

f1.close()
f2.close()
f3.close()

