# -*- coding: utf-8 -*-
import scrapy
import re

class InstacomSpider(scrapy.Spider):
    name = 'instacom'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    insta_login = 'petrov'
    insta_passwd = '#PWD_INSTAGRAM_BROWSER:9:1591723544:AVdQAGDz+ABMg1oN4C3HAjl0o4jNswq/7QJOWaA16EA87Ytr89YagoUnJq329SvEa7xY6tq2O9RDEcn8khGC0LXPOcm42zw4U4ucFTAhEYP0IGZgBhrpm6oD+Vip8ZuALsGd2u4t1mR0aw1u+CuK'
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'

    def parse(self, response):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.parse_user,
            formdata={'username': self.insta_login,
                      'enc_password': self.insta_pass},
            headers={'X-CSRFToken': csrf_token}
        )

        pass

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')