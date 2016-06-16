"""To use converter from command line do: python3 prs-xml.py [input_file] [output_file]"""

import csv
from lxml import etree
from sys import argv

def prs_xml(inp, outp):
    try:
        with open(inp, encoding='utf-8') as myfile:
            lines = csv.DictReader(myfile, delimiter='\t')
            root = etree.Element('body')
            for line in lines:
                if line['#sentno'].startswith('#meta'):#пропускаем строки с метаинформацией
                    continue
                if line['#wordno'] == '1' and line['#nvar'] == '1':#если это первое слово предложения
                    se = etree.SubElement(root, 'se')#добавляем предложение
                if line['#nvar'] == '1':#если это первый разбор слова
                    w = etree.SubElement(se, 'w')#добавляем слово
                if line['#word'] != ' ':#отфильтровываем псевдо-строки
                    ana = etree.SubElement(w, 'ana')
                    ana.set('lex', line['#lem'])
                    ana.set('morph', line['#flex'])
                    gr = line['#lex']+','+line['#gram']#склеиваем грамматическую информацию
                    ana.set('gr', gr)
                    if line['#nvar'] == line['#nvars']:#если это был последний разбор слова
                        ana.tail = line['#word']#добавляем само слово за тегом <ana>
                        if line['#punctr'] != 'bos' and line['#punctr'] != 'eos':
                            w.tail = line['#punctr']#возвращаем пунктуацию после слова, если есть
                        else:
                            w.tail = ''
        out_file = open(outp, 'w', encoding='utf-8')
        text_xml = etree.tostring(root, pretty_print=True, encoding="utf-8").decode()
        out_file.write(text_xml)
        out_file.close()
        print('prs-xml convertation successful')
    except Exception as error:
        print('can not convert this .prs to .xml; error:{}'.format(str(error)))

def xml_prs(inp, outp):
    try:
        inp_file = open(inp, 'r', encoding='utf-8')
        out_file = open(outp, 'w', encoding='utf-8')
        header = '#sentno\t#wordno\t#lang\t#graph\t#word\t#indexword\t#nvars\t#nlems\t#nvar\t#lem\t#trans\t#trans_ru\t#lex\t#gram\t#flex\t#punctl\t#punctr\t#sent_pos\n'
        out_file.write(header)
        tree = etree.fromstring(inp_file.read())
        s_counter = 1 #счётчик предложений; он же #sentno
        for sent in tree.iter('se'):
            w_counter = 1 #счётчик слов; он же #wordno
            s_len = len(list(tree.iter('se')))#длина предложения для (подстановки eos)
            for w in sent.iter('w'):
                if w.tail != None:
                    punctr = w.tail.strip() #пунктуация после слова
                else:
                    punctr = ''
                lang = ''#в примере везде пустая строка, не понятно, как информация выглядит в других примерах
                word = w.xpath("string()").strip()#само слово
                if word.istitle():#начинается ли слово с заглавной
                    graph = 'cap'
                else:
                    graph = ''
                indexword = '' #тоже пустые в примере
                nvar = 0 #номер разбора
                nvars = 0 #общее число разборов
                lemmas = []#список лемм
                for ana in w.iter('ana'):#cначала считаем число разборов
                    nvars+=1
                    if ana.get('lex') not in lemmas:
                        lemmas.append(ana.get('lex'))
                nlem = len(lemmas)#и число лемм
                if w_counter == 1:
                    sent_pos = 'bos'
                else:
                    if w_counter == s_len:
                        sent_pos = 'eos'
                    else:
                        sent_pos = ''
                for ana in w.iter('ana'):
                    nvar+=1#текущий номер разбора
                    xml_gram = ana.get('gr')
                    if ',' in xml_gram:
                        lex, gram = xml_gram.split(',', 1)
                    else:
                        lex = gram
                        gram = ''
                    """Ниже получаем все недостающие значения"""
                    lem = ana.get('lex')
                    if ana.get('trans') != None:
                        trans = ana.get('trans')
                    else:
                        trans = ''
                    trans_ru = ''
                    if ana.get('morph') != None:
                        flex = ana.get('morph')
                    else:
                        flex = ''
                    punctl = ''
                    line = str(s_counter), str(w_counter), lang, graph, word, indexword, str(nvars), str(nlem), str(nvar), lem, trans, trans_ru, lex, gram, flex, punctl, punctr, sent_pos
                    line = '\t'.join(line)+'\n'
                    out_file.write(line)
                w_counter+=1
            s_counter+=1
        out_file.close()
        inp_file.close()
        print('xml-prs convertation successful')
    except Exception as error:
        print('can not convert this .xml to .prs; error:{}'.format(str(error)))

if len(argv) == 3:
    if argv[1].endswith('.prs'):
        if argv[2].endswith('.xml'):
            print('prs-xml convertation is started')
            prs_xml(argv[1], argv[2])
        else:
            print('wrong output_file extention; .xml expected')
    elif argv[1].endswith('.xml'):
        if argv[2].endswith('.prs'):
            print('xml-prs convertation is started')
            xml_prs(argv[1], argv[2])
        else:
            print('wrong output_file extention; .prs expected')
    else:
        print('wrong input_file extention; .xml or .prs expected')
else:
    print('wrong arguments. usage: python3 prs-xml.py [input_file] [output_file]')

