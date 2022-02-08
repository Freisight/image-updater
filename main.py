import os
import time
import shutil
from shutil import rmtree
from tqdm import tqdm
from ftplib import FTP

# Задачи на будущее
# Прикрутить логирование
# Сделать классом для более удобного дальнеййшего расширения, есть ещё пара каталогов для обновления.
# Следовательно прикрутить ещё каталоги

alphabet = {'а':'a', 'б':'b', 'в':'v', 'г':'g','д':'d','е':'e','ё':'yo',
      'ж':'zh','з':'z','и':'i','й':'j','к':'k','л':'l','м':'m','н':'n',
      'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
      'ц':'c','ч':'ch','ш':'sh','щ':'sh','ъ':'','ы':'y','ь':'','э':'e',
      'ю':'u','я':'ya', ' ':'_', '-':'_', '  ':'_', '   ':'_', '1':'1', '2':'2',
      '3':'3', '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9',}


# Опознают директорию в которой лежит скрипт, потом меняем рабочую директорию на опознанную папку.
dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)
# print(os.getcwd())

# тут узнаем разницу между текущим временем и временем обновления файла.
now_time = time.time()

def get_difference_days(now, file):
    file_time = os.path.getmtime(file)
    dif_time = now - file_time
    dif_day = dif_time // 60 // 60 // 24
    return dif_day


# производим копирование и игнорирование ненужного
# if os.path.isdir('cottages'):
#     rmtree('cottages')

# if not os.path.isdir('cottages'):
#     copytree('K:\Информационный отдел для земельных экспертов\_ЦЕНЫ по коттеджным поселкам\Коттеджные поселки_для сайта', 'cottages', ignore=ignore_patterns('*.db', 'tmp*'))


# получаем все файлы, которые есть на диске К.
directory_image_eng = os.listdir('K:\Информационный отдел для земельных экспертов\_ЦЕНЫ по коттеджным поселкам\Коттеджные поселки_для сайта')

# удаляем лишние файлы из списка
for item in directory_image_eng:
    if '.db' in item:
      directory_image_eng.remove(item)


# удаляем папку cottages если она есть с старыми файлами
if os.path.isdir('cottages'):
    rmtree('cottages')

# создаем папку в которую будет копировать файлы
os.mkdir("cottages")

# меняем 
os.chdir('cottages')

# добавляет название файлов с сервера
print('Проверяем обновление у файлов.')
for file in tqdm(directory_image_eng):
    url = f'K:\Информационный отдел для земельных экспертов\_ЦЕНЫ по коттеджным поселкам\Коттеджные поселки_для сайта\{file}'
    if get_difference_days(now_time, url) < 2:
        shutil.copyfile(url, file)


directory_image_rus = os.listdir(os.getcwd())
directory_image_eng = []

# Переименование файлов побуквенно
for items in directory_image_rus:
    new_word = []
    for word in items:
        word = word.lower()
        if word in alphabet:
            new_word.append(alphabet[word])
        elif word == '.':
            break

    new_name = ''.join(new_word) # в new_word у нас каждая буква элемент списка, тут мы склеиваем всё в одно слово
    end_name = new_name + '.jpg' # new_name теперь целовое слово, добавим к нему формат картинки
    directory_image_eng.append(end_name) # каждое новое слово добавляем в новый список изображений

# делаем из двух списков один словарь, чтобы точно ничего не перепутать
all_cottages = dict(zip(directory_image_rus, directory_image_eng))

print(all_cottages)


# заменяем название файлов В случае побуквенной замены названий файлов
for rus, eng in all_cottages.items():
    if os.path.exists(rus):
        os.replace(rus, eng)

print(all_cottages)



# подготавливаем список файлов из cottages
directory_image = os.listdir(os.getcwd())

print(directory_image)


print('Подключаемся к FTP...')
ftp = FTP('')
ftp.login('zem-expert-map', '', 80) 
# меняем директорию на cottages
ftp.cwd('cottages')

print('Закачиваем файлы на FTP...')

for items in tqdm(directory_image):
    file_to_upload = open(items, 'rb')
    ftp.storbinary('STOR ' + items, file_to_upload)


ftp.quit()
print('Карты обновлены.')
