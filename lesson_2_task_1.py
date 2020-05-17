import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
import pandas.io.json as pd_json


main_link = 'https://spb.hh.ru'

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'Accept': '*/*'}
params = {'area': '2', 'st': 'searchVacancy', 'text': 'python'}
response = requests.get(main_link + '/search/vacancy', headers=header, params=params).text
soup = bs(response, 'lxml')
i=0
vacancy = []
while soup.find('a',{'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'}) != None:
    params = {'area': '2', 'st': 'searchVacancy', 'text': 'python', 'page': i}
    response = requests.get(main_link + '/search/vacancy', headers=header, params=params).text
    soup = bs(response, 'lxml')
    main_vacancy_block = soup.find('div', {'data-qa': 'vacancy-serp__results'})
    vacancy_block = main_vacancy_block.find('div', {'class': 'vacancy-serp'})
    vacancy_list = vacancy_block.findChildren(recursive=False)
    for data in vacancy_list:
        vacancy_data = {}
        if data.find('a', {'class': 'bloko-link HH-LinkModifier'}) != None:
            vacancy_name = data.find('a', {'class': 'bloko-link HH-LinkModifier'}).getText()
            if data.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}) !=None:
                vacancy_salary_from_to = data.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
            else:
                vacancy_salary_from_to = 'зп не указана'
            vacancy_link = data.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
            site_link = str(main_link)
            vacancy_data['name'] = vacancy_name
            if vacancy_salary_from_to != None:
                vacancy_data['salary'] = vacancy_salary_from_to
            vacancy_data['link'] = vacancy_link
            vacancy_data['site'] = site_link
            vacancy.append(vacancy_data)
    i +=1


data_vacansy = pd.DataFrame(vacancy)
print(data_vacansy)

