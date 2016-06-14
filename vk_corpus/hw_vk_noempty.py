import vk, os
from time import sleep

"""!DO NOT COMMIT!"""
APPID = ''
EMAIL = ''
PASSWORD = ''

meta = open('meta.tsv', 'w', encoding='utf-8')
meta_headers = 'uid' + '\t' + 'sex' + '\t' + 'bdate' + '\t' + 'city' + '\t' + 'langs' + '\n'
meta.write(meta_headers)

os.mkdir('./vk_corpus')

def save_meta_inf(users, user_posts):
    """Собирает мета-информацию о пользователях, у которых на стене есть текстовые записи,
    и записывает в .tsv  файл"""
    counter = 0
    for user in users:
        uid = user['uid']
        if uid in user_posts.keys():
            if user['sex'] == 1:
                sex = 'female'
            elif user['sex'] == 2:
                sex = 'male'
            else:
                sex = ''
            if 'bdate' in user:
                bdate = user['bdate']
            else:
                bdate = ''
            if user['city'] !=0: #фильтруем случаи, когда город не указан
                city = api.database.getCitiesById(city_ids=user['city'])[0]['name']
            else:
                city = ''
            if 'personal' in user and 'langs' in user['personal']:#достаём языки, которые указал пользователь
                langs = ",".join(user['personal']['langs'])#превращаем их в читаемую строку
            else:
                langs = ''
            meta_line = str(uid) + '\t' + sex + '\t' + bdate + '\t' + city + '\t' + langs + '\n'#задаём строку мета-информации
            meta.write(meta_line)
            counter+=1
            print("Meta for {} user(s) is saved.".format(counter))
            sleep(0.3)

def save_posts(users):
    """Проверяет наличие у пользователей техкстовых записей на стене;
    для тех, у кого они есть, создаёт текстовый файл и сохраняет в него посты;
    возращает список ID, у которых посты есть, и количество постов"""
    user_posts = {}
    counter = 0
    for user in users:
        texts = ''
        uid = user['uid']
        posts = api.wall.get(owner_id=uid, filter="owner", count=100)[1:]#собираем посты автора
        if len(posts) != 0:
            for post in posts:#достаём из них текст
                if post['post_type'] == 'post' and len(post['text']) > 1:#фильтруем случаи типа " " или "." и т.п.
                    texts = texts + post['text'] +'\n\n'
        if len(texts)>0:#если среди постов были текстовые
            #user_posts[uid] = len(posts) – для проверки использовалось кол-во постов пользователя
            out_file = open('./vk_corpus/{}_posts.txt'.format(uid), 'w', encoding='utf-8')
            out_file.write(texts)#записываем тексты в файл
            counter+=1
            print("Posts for {} user(s) are saved.".format(counter))
            out_file.close()
        sleep(0.3)
    return user_posts


session = vk.AuthSession(APPID, EMAIL, PASSWORD)
api = vk.API(session)
users = api.users.search(hometown='Забайкальск', count=1000, fields='sex, bdate, city,  personal')[1:]
user_posts = save_posts(users)
save_meta_inf(users, user_posts)

meta.close()