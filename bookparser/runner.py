from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from bookparser import settings
from bookparser.spiders.book24 import Book24Spider
from bookparser.spiders.Labirint import LabirintSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    answer = input(' введите книжый раздел ')
    process.crawl(Book24Spider, name_branch=answer)
    # process.crawl(LabirintSpider, name_branch=answer)
    process.start()
