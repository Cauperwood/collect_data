from lxml import html
import requests
import re
import datetime
from pymongo import MongoClient
import pprint

class news_parser:
    main_link_yan = 'https://yandex.ru/news'
    main_link_mailn = 'https://news.mail.ru'
    main_link_lenta = 'https://lenta.ru'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept': '*/*'}

    @classmethod
    def lenta_news(cls):
        response = requests.get(cls.main_link_lenta, headers=cls.header)
        dom = html.fromstring(response.text)
        data_lenta_news = []
        result_name = dom.xpath('//div[@class="item"]/a/text()')
        result_link = dom.xpath('//div[@class="item"]/a/@href')
        for i in range(len(result_name)):
            data_lenta = {}
            data_lenta['name'] = result_name[i]
            data_lenta['sourse'] = cls.main_link_lenta
            data_lenta['link'] = cls.main_link_lenta + result_link[i]
            date_text = ''.join(re.findall(r'\d{4}\D\d{2}\D\d{2}', result_link[i]))
            date = re.sub(r'(\d{4})/(\d\d)/(\d\d)', r'\3.\2.\1', date_text)
            data_lenta['date'] = date
            data_lenta_news.append(data_lenta)
        return data_lenta_news

    @classmethod
    def yandex_news(cls):
        response = requests.get(cls.main_link_yan, headers=cls.header)
        dom = html.fromstring(response.text)
        yandex_news_data = []
        result_name = dom.xpath('//td[@class="stories-set__item"]//h2[@class="story__title"]/a/text()')
        result_link = dom.xpath('//td[@class="stories-set__item"]//h2[@class="story__title"]/a/@href')
        for i in range(len(result_name)):
            data_yandex_news = {}
            data_yandex_news['name'] = result_name[i]
            data_yandex_news['sourse'] = cls.main_link_yan
            data_yandex_news['link'] = cls.main_link_yan + result_link[i]
            date = datetime.date.today()
            data_yandex_news['date'] = date.strftime("%m.%d.%Y")
            yandex_news_data.append(data_yandex_news)
        return yandex_news_data

    @classmethod
    def mail_news(cls):
        mail_news_data = []
        response = requests.get(cls.main_link_mailn, headers=cls.header)
        dom = html.fromstring(response.text)

        result_name = dom.xpath("//div[@class='daynews__item']//span[@class='photo__title photo__title_new photo__title_new_hidden js-topnews__notification']/text()")
        result_link = dom.xpath("//div[@class='daynews__item']//a[@class='photo photo_small photo_scale photo_full js-topnews__item']/@href")
        mail_news_data.extend(cls.collect_mail(result_name, result_link))

        result_name = dom.xpath("//li[@class='list__item']/a/text()")
        result_link = dom.xpath("//li[@class='list__item']/a/@href")
        mail_news_data.extend(cls.collect_mail(result_name, result_link))

        result_name = dom.xpath("//li[@class='list__item']/span[@class='list__text']/a[@class='link link_flex']/span/text()")
        result_link = dom.xpath("//li[@class='list__item']/span[@class='list__text']/a[@class='link link_flex']/@href")
        mail_news_data.extend(cls.collect_mail(result_name, result_link))
        return mail_news_data


    @classmethod
    def collect_mail(cls, result_name, result_link):
        mail_news_data = []
        for i in range(len(result_name)):
            data_mail_news = {}
            data_mail_news['name'] = result_name[i]
            data_mail_news['sourse'] = cls.main_link_mailn
            data_mail_news['link'] = cls.main_link_mailn + result_link[i]
            date = datetime.date.today()
            data_mail_news['date'] = date.strftime("%m.%d.%Y")
            mail_news_data.append(data_mail_news)
        return mail_news_data

    @classmethod
    def start_parser(cls):
        news_of_the_day = []
        news_of_the_day.extend(cls.lenta_news())
        news_of_the_day.extend(cls.yandex_news())
        news_of_the_day.extend(cls.mail_news())
        return news_of_the_day

def insert_db(data):
    """вставляем данные в базу  mongodb"""
    client = MongoClient('localhost', 27017)
    db = client['day_news']
    db.day_news.insert_many(data)
    return db.day_news.find({})








insert_db(news_parser.start_parser())

client = MongoClient('localhost', 27017)
db = client['day_news']
for i in db.day_news.find({}):
    print(i)