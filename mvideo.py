from selenium import webdriver
from time import sleep
from pymongo import MongoClient

def insert_db(data):
    """вставляем данные в базу  mongodb"""
    client = MongoClient('localhost', 27017)
    db = client['mvideo_goods']
    db.mvideo_goods.insert_many(data)
    return db.mvideo_goods.find({})


driver = webdriver.Chrome('/Users/dmitrijsibircev/Desktop/Data_Science/internet_data/lesson_7/venv/chromedriver')
driver.get('https://www.mvideo.ru')
sleep(10)

while True:
    sleep(3)
    elem = driver.find_elements_by_class_name('sel-hits-button-next')[2]
    if elem.get_attribute('class') == 'next-btn sel-hits-button-next disabled':
        break
    elem.click()

links = driver.find_elements_by_class_name('gallery-list-item height-ready')
for link in links:
    data = link.find_elements('data-product-info')
    print(insert_db(data))
    print(data)

driver.quit()