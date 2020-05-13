import requests
from pprint import pprint
import json

user_name = input('введите имя пользователя ')
main_link = f'https://api.github.com/users/{user_name}/repos'
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'Accept': '*/*'}
response = requests.get(main_link, headers=header)
if response.ok:
    data = json.loads(response.text)
# pprint(data) #выводит список словарей
d = []
for i in data:
    d.append(i["name"])
print(f'У пользователя {user_name} имеются следующие репозитории: {", ".join(d)}')

# print(data['name'])

# print(response.status_code)
# print(response.ok)
# # print(response.headers)
# print(response.text)
# # print(response.content) # тело в бинарном виде