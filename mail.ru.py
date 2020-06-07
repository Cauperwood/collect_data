from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')

def insert_db(data):
    """вставляем данные в базу  mongodb"""
    client = MongoClient('localhost', 27017)
    db = client['mail']
    db.mail.insert_one(data)
    return db.mail.find({})

driver = webdriver.Chrome('/Users/dmitrijsibircev/Desktop/Data_Science/internet_data/lesson_7/venv/chromedriver', options=chrome_options)

driver.get('https://mail.ru/')

elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172')
driver.find_element_by_id('mailbox:submit').click()


time.sleep(1)


elem = driver.find_element_by_id('mailbox:password')
elem.send_keys('NextPassword172')
elem.send_keys(Keys.RETURN)
time.sleep(0)

driver.get('https://e.mail.ru/inbox')


links = set()
while True:
    time.sleep(2)
    articles = driver.find_elements_by_class_name("js-letter-list-item")
    if not articles[-1]:
        break
    [links.add(mail.get_attribute('href')) for mail in articles]
    actions = ActionChains(driver)
    actions.move_to_element(articles[-1])
    actions.perform()

links = list(links)
for link in links:
    driver.get(link)
    author = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'letter-contact'))
    )
    author = author.get_attribute('title')
    subject = driver.find_element_by_tag_name('h2').text
    text = driver.find_element_by_class_name('letter__body').text
    insert_db({'author': author, 'subject': subject, 'text': text})

driver.quit()

driver.quit()