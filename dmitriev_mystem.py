import os, subprocess

input_path = ('/Users/tatianagolovko/Documents/учёба/ВШЭ/Python/2/Dmitriev/Dmitriev_plain_text')
os.chdir("/Users/tatianagolovko/Documents/учёба/ВШЭ/Python/2/Dmitriev/")
output_path_1_main = './Mystem_txt'
output_path_2_main = './Mystem_xml'
os.mkdir(output_path_1_main)
os.mkdir(output_path_2_main)

for i in range(1,80): #80 категорий, папки названы по номерам
    cat_path = input_path+'/'+str(i) #путь к категории со статьями
    output_path_1 = output_path_1_main+'/'+str(i)
    output_path_2 = output_path_2_main+'/'+str(i)
    os.mkdir(output_path_1)#создаю папку с аналогичной категорией для mystem_txt
    os.mkdir(output_path_2)#создаю папку с аналогичной категорией для mystem_xml

    files = os.listdir(cat_path)#список файлов в категории
    for file in files:
        input_file = cat_path+'/'+file #адрес этого файла
        output_1 = output_path_1+'/'+file[:-15]+'_mystem'+'.txt' #формирую адрес файла для записи txt
        output_2 = output_path_2+'/'+file[:-15]+'_mystem'+'.xml' #формирую адрес файла для записи xml

        """вызываю mystem для записи в txt"""
        subprocess.call(['/Users/tatianagolovko/Desktop/mystem',
        '-e UTF-8',
        '-dicg',
        input_file,
        output_1])

        """вызываю mystem для записи в xml"""
        subprocess.call(['/Users/tatianagolovko/Desktop/mystem',
        '-e UTF-8',
        '-dicg',
        '--format',
        'xml',
        input_file,
        output_2])
