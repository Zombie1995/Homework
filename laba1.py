import string
import json

f = open('pokemon_full.json')
s = f.read()
jsn = json.loads(s)

#########task1#########
print('Task1:')
print(len(s))

#########task2#########
print('Task2:')
temp1 = s.translate(s.maketrans(dict.fromkeys(string.punctuation)))
temp2 = len(temp1.replace(' ', ''))
print(temp2)

#########task3#########
print('Task3:')
s = ''
name = ''
for obj in jsn:
    if len(obj['description']) > len(s):
        s = obj['description']
        name = obj['name']
print(name)

#########task4#########
print('Task4:')
words_num = 0
abilities = []
for obj in jsn:
    for abil in obj['abilities']:
        if len(abil.split()) > words_num:
            words_num = len(abil.split())
            abilities = []
        if len(abil.split()) == words_num:
            abilities.append(abil)
print(abilities)

f.close()
