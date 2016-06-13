"""транслитератор для амхарского"""
alph = open('amhar-alph.tsv', 'r', encoding = 'utf-8')
input = open('input_example.txt', 'r', encoding='utf-8')
output = open('output.txt', 'w', encoding='utf-8')

matrix = [] #массив для строк
dictionary = {} #будущий словарь транслитератора


for line in alph:
    line = line.strip('\n')
    matrix.append(line.split('\t')) #создаю массив строк, где каждая строка отдельный массиив; получается подобие матрицы.
for c in range(len(matrix)): #по матрице для каждой согласной
    for v in range(len(matrix[c])): #создаем пару с каждой гласной
        vowel = matrix[0][v]
        consonant = matrix[c][0]
        dictionary[matrix[c][v]] = consonant+vowel #ключ – символ амхарского, значение – пара согл+гл
#print(matrix)
print(dictionary)
for line in input: #в каждой строке входного файла
    for key, value in dictionary.items():
        line = line.replace(key, value)#заменяем символ амхарского на пару из словаря
    output.write(line)#записываем результат
alph.close()
input.close()
output.close()