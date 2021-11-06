import csv

f = open('anime.csv', encoding='utf-8', newline = '')
animes = csv.DictReader(f)

#########task1#########
print('Жанры?')
janres = input().replace(' ', '').split(',')
print('Тип? (Че это?)')
type = input()
print('Многосерийное аниме? (Y, N)')
is_serial = input()
print('Законченное аниме? (Y, N)')
is_finished = input()
print('Предпочтительные студии?')
studios = input().replace(' ', '').split(',')
#остальное думаю не имеет смысла опрашивать, не знаю

anime_list = list()
anime_list_temp = list()
for anime in animes:
    anime_list.append(anime)
anime_list_temp = anime_list.copy()

if janres != ['']:
    rmv = True
    for anime in anime_list_temp:
        for janre in janres:
            tags = anime['Tags'].replace(' ', '').split(',')
            if janre in tags:
                rmv = False
                break
        if rmv:
            anime_list.remove(anime)
        rmv = True
anime_list_temp = anime_list.copy()

if type != '':
    for anime in anime_list_temp:
        if not (anime['Type'] == type):
            anime_list.remove(anime)
anime_list_temp = anime_list.copy()

if is_serial != '':
    if is_serial == 'Y':
        for anime in anime_list_temp:
            if anime['Episodes'] == '1':
                anime_list.remove(anime)
    if is_serial == 'N':
        for anime in anime_list_temp:
            if anime['Episodes'] != '1':
                anime_list.remove(anime)
anime_list_temp = anime_list.copy()

if is_finished != '':
    if is_finished == 'Y':
        for anime in anime_list_temp:
            if anime['Episodes'] == 'False':
                anime_list.remove(anime)
    if is_finished == 'N':
        for anime in anime_list_temp:
            if anime['Episodes'] == 'True':
                anime_list.remove(anime)
anime_list_temp = anime_list.copy()

if studios != ['']:
    rmv = True
    for anime in anime_list_temp:
        for studio in studios:
            studios_in_anime = anime['Studios'].replace(' ', '').split(',')
            if studio in studios_in_anime:
                rmv = False
                break
        if rmv:
            anime_list.remove(anime)
        rmv = True
anime_list_temp = anime_list.copy()

f.close()

def custom_key(anime):
    try:
        result = float(anime['Rating Score'])
        return result
    except:
        return 0
anime_list.sort(reverse=True, key=custom_key)

f = open('result.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
wr.writerow(animes.fieldnames)
for anime in anime_list:
    wr.writerow(anime.values())

f.close()

#########task_additive#########
import requests

i = 1
for anime in anime_list:
    url = 'https://www.anime-planet.com/images/anime/covers/thumbs/' + str(anime['Anime-PlanetID']) + '.jpg'
    img_data = requests.get(url).content
    handler = open(str(i) + '.jpg', 'wb')
    handler.write(img_data)
    handler.close()
    i += 1
    if i > 5:
        break

#########workspace#########

# import pip
# pip.main(['install','requests'])

# for row in wtf:
#     for word in row:
#         print(word)
#     if wtf.line_num == 2:
#         break

# janres_temp = list()
# for anime in animes:
#     for tag in anime['Tags'].replace(' ', '').split(','):
#         if not(tag in janres_temp):
#             janres_temp.append(tag)
# print(janres_temp)

# if (1):
#     print('haha')
# if not (0):
#     print('haha2')