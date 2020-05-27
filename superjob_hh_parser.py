import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
import json
# import pandas as pd
# import pandas.io.json as pd_json
import re
from pymongo import MongoClient


class parser:
    main_link_hh = 'https://spb.hh.ru'
    main_link_sj = 'https://russia.superjob.ru'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept': '*/*'}
    choose_vacancy = input('введите вакансию ')

    @staticmethod
    def salary_hh(data):
        if data.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}) != None:
            salary_data = data.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
            if 'до' in salary_data.split():
                salary_max = ''.join(re.findall('\d*', ''.join(salary_data.split()[1:])))
                salary_min = None
                currency = ''.join(re.findall('\D{3}', ''.join(salary_data.split()[1:])))
                return salary_max, salary_min, currency
            elif 'от' in salary_data.split():
                salary_max = None
                salary_min = ''.join(re.findall('\d*', ''.join(salary_data.split()[1:])))
                currency = ''.join(re.findall('\D{3}', ''.join(salary_data.split()[1:])))
                return salary_max, salary_min, currency
            else:
                salary_max = ''.join(re.findall('\d*', ''.join(salary_data.split('-')[1:])))
                salary_min = ''.join(re.findall('\d*', ','.join(salary_data.split('-')[:1])))
                currency = ''.join(re.findall('\D{3}', ''.join(salary_data.split()[1:])))
                return salary_max, salary_min, currency
        else:
            salary_max = None
            salary_min = None
            currency = None
            return salary_max, salary_min, currency

    @staticmethod
    def salary_sj(data):
        if data.find('span', {'class': 'f-test-text-company-item-salary'}) != None \
                and 'договорённости' not in data.find('span',
                                                      {'class': 'f-test-text-company-item-salary'}).getText().split():
            salary_data = data.find('span', {'class': 'f-test-text-company-item-salary'}).getText()
            if 'до' in salary_data.split():
                salary_max = ''.join(re.findall('\d*', ''.join(salary_data.split()[1:])))
                salary_min = None
                currency = ''.join(re.findall('\D{3}', ''.join(salary_data.split()[1:])))
                return salary_max, salary_min, currency
            elif 'от' in salary_data.split():
                salary_max = None
                salary_min = ''.join(re.findall('\d*', ''.join(salary_data.split()[1:])))
                currency = ''.join(re.findall('\D{3}', ''.join(salary_data.split()[1:])))
                return salary_max, salary_min, currency
            elif '—' in salary_data.split():
                salary_max = ''.join(re.findall('\d*', ''.join(salary_data.split()[2:])))
                salary_min = ''.join(re.findall('\d*', ''.join(salary_data.split()[:2])))
                currency = ''.join(re.findall('\D{3}', ''.join(salary_data.split()[1:])))
                return salary_max, salary_min, currency
            else:
                salary_max = ''.join(re.findall('\d*', ''.join(salary_data.split())))
                salary_min = None
                currency = ''.join(re.findall('\D{3}', ''.join(salary_data.split()[1:])))
                return salary_max, salary_min, currency
        else:
            salary_max = None
            salary_min = None
            currency = None

            return salary_max, salary_min, currency

    @classmethod
    def parser_hh(cls):
        i = 0
        vacancy_hh = []
        inteterest_vacancy = cls.choose_vacancy
        params = {'area': '2', 'st': 'searchVacancy', 'text': inteterest_vacancy}
        response = requests.get(cls.main_link_hh + '/search/vacancy', headers=cls.header, params=params).text
        soup = bs(response, 'lxml')
        while soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'}) != None:
            params = {'area': '2', 'st': 'searchVacancy', 'text': inteterest_vacancy, 'page': i}
            response = requests.get(cls.main_link_hh + '/search/vacancy', headers=cls.header, params=params).text
            soup = bs(response, 'lxml')
            main_vacancy_block = soup.find('div', {'data-qa': 'vacancy-serp__results'})
            vacancy_block = main_vacancy_block.find('div', {'class': 'vacancy-serp'})
            vacancy_list = vacancy_block.findChildren(recursive=False)
            for data in vacancy_list:
                vacancy_data = {}
                if data.find('a', {'class': 'bloko-link HH-LinkModifier'}) != None:
                    vacancy_name = data.find('a', {'class': 'bloko-link HH-LinkModifier'}).getText()
                    vacancy_link = data.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
                site_link = str(cls.main_link_hh)
                vacancy_data['name'] = vacancy_name
                vacancy_data['salary_max'], vacancy_data['salary_min'], vacancy_data['currency'] = cls.salary_hh(data)
                vacancy_data['link'] = vacancy_link
                vacancy_data['site'] = site_link
                vacancy_hh.append(vacancy_data)
            i += 1
        return vacancy_hh

    @classmethod
    def parser_sj(cls):
        params = {'keywords': cls.choose_vacancy}
        response = requests.get(cls.main_link_sj + '/vacancy/search/', headers=cls.header, params=params).text
        soup = bs(response, 'lxml')
        vacancy_sj = []
        vacancy_list = soup.find_all('div', {'class': 'Fo44F QiY08 LvoDO'})
        for data in vacancy_list:
            vacancy_data = {}
            #             if data.find('div', {'class': 'LvoDO'}) != None:
            vacancy_name = data.find('a', {'target': '_blank'}).getText()
            vacancy_link = cls.main_link_sj + data.find('a', {'target': '_blank'})['href']
            site_link = str(cls.main_link_sj)
            vacancy_data['name'] = vacancy_name
            vacancy_data['salary_max'], vacancy_data['salary_min'], vacancy_data['currency'] = cls.salary_sj(data)
            vacancy_data['link'] = vacancy_link
            vacancy_data['site'] = site_link
            vacancy_sj.append(vacancy_data)
        i = 2
        while soup.find('a', {'class': 'f-test-link-Dalshe'}) != None:
            params = {'keywords': cls.choose_vacancy, 'page': i}
            response = requests.get(cls.main_link_sj + '/vacancy/search/', headers=cls.header, params=params).text
            soup = bs(response, 'lxml')
            vacancy_list = soup.find_all('div', {'class': 'Fo44F QiY08 LvoDO'})
            for data in vacancy_list:
                vacancy_data = {}
                #                 if data.find('div', {'class': ['Fo44F', 'QiY08', 'LvoDO']}) != None:
                vacancy_name = data.find('a', {'target': '_blank'}).getText()
                vacancy_link = cls.main_link_sj + data.find('a', {'target': '_blank'})['href']
                site_link = str(cls.main_link_sj)
                vacancy_data['name'] = vacancy_name
                vacancy_data['salary_max'], vacancy_data['salary_min'], vacancy_data['currency'] = cls.salary_sj(data)
                vacancy_data['link'] = vacancy_link
                vacancy_data['site'] = site_link
                vacancy_sj.append(vacancy_data)
            i += 1
        return vacancy_sj


    @classmethod
    def start(cls): # запускает сбор данных и приводит строковые данные оплаты к типу int
        vacancy = []
        data_hh = cls.parser_hh()
        vacancy.extend(data_hh)
        data_sj = cls.parser_sj()
        vacancy.extend(data_sj)
        for sal in vacancy:
            if sal['salary_max'] != None:
                sal_max = sal['salary_max']
                sal['salary_max'] = int(sal_max)
            if sal['salary_min'] != None:
                sal_min = sal['salary_min']
                sal['salary_min'] = int(sal_min)
        return vacancy


data = parser.start()
# pprint(data)

def insert_db(data):
    """вставляем данные в базу  mongodb"""
    client = MongoClient('localhost', 27017)
    db = client['vacancy']
    db.vacancy.insert_many(data)
    return db.vacancy.find({})

insert_db(data)


def search_sal(salary):
    """ функция получает значение оплаты типа int и выводит вакансии с оплатой выше или равной заданной """
    client = MongoClient('localhost', 27017)
    db = client['vacancy']
    vac = []
    for item_max in db.vacancy.find({'$or': [{'salary_min': {'$gte': salary}}, {'salary_max': {'$gte': salary}}]}):
        vac.append(item_max)
    return vac

pprint(search_sal(int(input('введите минимальный порог оплаты '))))


# не успел

# def update_db(data, name_db):
#     client = MongoClient('localhost', 27017)
#     db = client['name_db']
#     for param in db.name_db.find({'link': {}})
#         if
#         db.name_db.insert_one(data)
#     return db.name_db.find({})
