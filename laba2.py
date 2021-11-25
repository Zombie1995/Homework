import csv

f = open('anime.csv', encoding='utf-8', newline='')
animes = csv.DictReader(f)


#########functions#########
def check_multiple_params(mult_params, key,
                          anime_list_param, anime_temp_list_param):
    if mult_params != ['']:
        rmv = True
        for anime in anime_temp_list_param:
            for param in mult_params:
                anime_params = anime[key].replace(' ', '').split(',')
                if param in anime_params:
                    rmv = False
                    break
            if rmv:
                anime_list_param.remove(anime)
            rmv = True


def check_one_param(param, key, anime_list_param, anime_temp_list_param):
    if param != '':
        for anime in anime_temp_list_param:
            if not (anime[key] == param):
                anime_list_param.remove(anime)


def check_yes_or_not(param, key, check_param,
                     anime_list_param, anime_temp_list_param):
    if param != '':
        if param == 'Y':
            for anime in anime_temp_list_param:
                if anime[key] == check_param:
                    anime_list_param.remove(anime)
        if param == 'N':
            for anime in anime_temp_list_param:
                if anime[key] != check_param:
                    anime_list_param.remove(anime)


def custom_key(anime):
    try:
        result = float(anime['Rating Score'])
        return result
    except ValueError:
        return 0


#########task1#########
print('Жанры?')
janres = input().replace(' ', '').split(',')
if janres != ['']:
    for num in range(len(janres)):
        janres[num] = janres[num].capitalize()
# Обоснование:
# for janre in janres:
#     janre = janre.capitalize()
# так не работает
# for num in range(len(janres)):
#     janres[num] = janres[num].capitalize()
# так работает
print('Тип? (Че это?)')
anime_type = input()
print('Многосерийное аниме? (Y, N)')
is_serial = input()
print('Законченное аниме? (Y, N)')
is_finished = input()
print('Предпочтительные студии?')
studios = input().replace(' ', '').split(',')
# остальное думаю не имеет смысла опрашивать, не знаю

anime_list = list()
anime_list_temp = list()
anime_list = [anime for anime in animes]
anime_list_temp = anime_list.copy()

check_multiple_params(janres, 'Tags', anime_list, anime_list_temp)
anime_list_temp = anime_list.copy()

check_multiple_params(studios, 'Studios', anime_list, anime_list_temp)
anime_list_temp = anime_list.copy()

check_one_param(anime_type, 'Type', anime_list, anime_list_temp)
anime_list_temp = anime_list.copy()

check_yes_or_not(is_serial, 'Episodes', '1', anime_list, anime_list_temp)
anime_list_temp = anime_list.copy()

check_yes_or_not(is_finished, 'Finished', 'False', anime_list, anime_list_temp)
anime_list_temp = anime_list.copy()

f.close()

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
    url = 'https://www.anime-planet.com/images/anime/covers/thumbs/' \
          + str(anime['Anime-PlanetID']) + '.jpg'
    img_data = requests.get(url).content
    handler = open(str(i) + '.jpg', 'wb')
    handler.write(img_data)
    handler.close()
    i += 1
    if i > 5:
        break

#########workspace#########

# for anime in animes:
#     anime_list.append(anime)

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
