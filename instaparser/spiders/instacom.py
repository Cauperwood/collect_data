# -*- coding: utf-8 -*-
import scrapy
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from instaparser.items import InstaparserItem
from scrapy.http import HtmlResponse


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'petrovilf898'
    insta_pass = '#PWD_INSTAGRAM_BROWSER:9:1591726153:AVdQAJpTzS6jdIQI+F/d1MdJMnH3pHWB01L75lh+gE2LBENWeNbV1k0PMs1mSTEczOQYC+NKUKEB3dvLw22aSghHemgPwLcY2GWYJo406xrUZazs4zNV6QkJAyOpSysQY29hD3c2h4+O9gr56C6b'
    inst_login_link = 'https://instagram.com/accounts/login/ajax/'
    parser_user = 'staud.clothing'

    # hash_posts = '7c8a1055f69ff97dc201e752cf6f0093'
    # hash_post = '552bb33f4e58c7805d13d4f95da7d3a1'
    hash_followers = 'c76146de99bb02f6415203be841dd25a'
    hash_follows = 'd04b0a864b4b54837c0d870b0e77e076'
    graphql_url = 'https://www.instagram.com/graphql/query/?'

    # def __init__(self, users):
    #     self.users_list = users
    #
    # def parse(self, response):
    #     csrf_token = self.fetch_csrf_token(response.text)
    #     yield scrapy.FormRequest(
    #             self.inst_login_link,
    #             method = 'POST',
    #             callback = self.parse_user,
    #             formdata={'username':self.insta_login,
    #                       'enc_password':self.insta_pass},
    #             headers={'X-CSRFToken':csrf_token}
    #     )
    #
    #     pass
    #
    # # def parse_user(self, response):
    # #     j_body = json.loads(response.text)
    # #     if j_body['authenticated']:
    # #         yield response.follow(
    # #             f'/{self.parser_user}',
    # #             callback=self.user_data_parse,
    # #         )
    #
    # def parse_user(self, response):
    #     j_body = json.loads(response.text)
    #     if j_body['authenticated']:
    #         for user in self.users_list:
    #             yield response.follow(
    #                 f'/{user}',
    #                 callback=self.user_data_parse,
    #             )
    #
    #
    # # def user_data_parse(self, response):
    # #     user_id = self.fetch_user_id(response.text, self.parser_user)
    # #     variables = {"id": user_id,
    # #                  "first": 24
    # #                  }
    # #     url_followers = f'{self.graphql_url}query_hash={self.hash_followers}&{urlencode(variables)}'
    # #
    # #     # 'query_hash=c76146de99bb02f6415203be841dd25a' \
    # #     # 'variables={"id"%3A"1384124957"%2C"include_reel"%3Atrue%2C"fetch_mutual"%3Atrue%2C"first"%3A24}'
    # #
    # #     yield response.follow(
    # #         url_followers,
    # #         callback=self.followers_parse,
    # #         cb_kwargs={'user_id': user_id,
    # #                    'variables': deepcopy(variables)}
    # #     )
    # #
    # #     url_follows = f'{self.graphql_url}query_hash={self.hash_follows}&{urlencode(variables)}'
    # #     yield response.follow(
    # #         url_follows,
    # #         callback=self.follows_parse,
    # #         cb_kwargs={'user_id': user_id,
    # #                    'variables': deepcopy(variables)}
    # #     )
    #
    #
    #
    #
    # def user_data_parse(self, response: HtmlResponse, user):
    #     user_info = response.xpath("//script[contains(text(), 'csrf_token')]/text()") \
    #         .extract_first().replace("window._sharedData = ", '').replace(";", '')
    #     user_info = json.loads(user_info).get('entry_data', {}) \
    #         .get('ProfilePage', {})[0] \
    #         .get('graphql', {}) \
    #         .get('user', {})
    #     info = {
    #         'user': user,
    #         'user_id': user_info.get('id'),
    #         'pic_url': user_info.get('profile_pic_url'),
    #         'is_private': user_info.get('is_private'),
    #         'full_name': user_info.get('full_name')
    #     }
    #     variables = {"id": info['user_id'],
    #                  "first": 50
    #                  }
    #     url_followers = f'{self.graphql_url}query_hash={self.hash_followers}&{urlencode(variables)}'
    #     yield response.follow(
    #         url_followers,
    #         callback=self.followers_parse,
    #         cb_kwargs={'info': info,
    #                    'variables': deepcopy(variables)}
    #     )
    #
    #     url_follows = f'{self.graphql_url}query_hash={self.hash_follows}&{urlencode(variables)}'
    #     yield response.follow(
    #         url_follows,
    #         callback=self.follows_parse,
    #         cb_kwargs={'info': info,
    #                    'variables': deepcopy(variables)}
    #     )
    #
    #
    # # def posts_parse(self,response,user_id, variables):
    # #     j_body = json.loads(response.text)
    # #     page_info = j_body.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
    # #     if page_info['has_next_page']:
    # #         variables['after'] = page_info['end_cursor']
    # #
    # #         url_posts = f'{self.graphql_url}query_hash={self.hash_posts}&{urlencode(variables)}'
    # #
    # #         yield response.follow(
    # #             url_posts,
    # #             callback=self.posts_parse,
    # #             cb_kwargs={'user_id': user_id,
    # #                        'variables': deepcopy(variables)}
    # #         )
    # #     posts = j_body.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
    # #     for post in posts:
    # #         item = InstaparserItem(
    # #             user_id = user_id,
    # #             photo = post['node']['display_url'],
    # #             likes = post['node']['edge_media_preview_like']['count'],
    # #             post_data = post['node']
    # #         )
    # #
    # #         yield item
    #
    # def followers_parse(self, response, info, variables):
    #     j_body = json.loads(response.text)
    #     page_info = j_body.get('data').get('user').get('edge_followed_by').get('page_info')
    #     followers = j_body.get('data').get('user').get('edge_followed_by').get('edges')
    #     for follower in followers:
    #         item = InstaparserItem(
    #             _id=f"{info['user_id']}_{follower['node']['id']}",
    #             follow_id=info['user_id'],
    #             follow_name=info['user'],
    #             follow_full_name=info['is_private'],
    #             follow_pic_url=info['pic_url'],
    #             follow_is_private=info['full_name'],
    #             follower_id=follower['node']['id'],
    #             follower_name=follower['node']['username'],
    #             follower_full_name=follower['node']['full_name'],
    #             follower_pic_url=follower['node']['profile_pic_url'],
    #             follower_is_private=follower['node']['is_private']
    #         )
    #
    #         yield item
    #
    #     if page_info.get('has_next_page'):
    #         variables['after'] = page_info['end_cursor']
    #
    #         url_posts = f'{self.graphql_url}query_hash={self.hash_followers}&{urlencode(variables)}'
    #
    #
    #
    #         yield response.follow(
    #             url_posts,
    #             callback=self.followers_parse,
    #             cb_kwargs={'info': info,
    #                        'variables': deepcopy(variables)}
    #         )
    #
    # def follows_parse(self, response, info, variables):
    #     j_body = json.loads(response.text)
    #     page_info = j_body.get('data', {}).get('user', {}).get('edge_follow', {}).get('page_info', {})
    #     follows = j_body.get('data', {}).get('user', {}).get('edge_follow', {}).get('edges', {})
    #     for foll in follows:
    #         item = InstaparserItem(
    #             _id=f"{foll['node']['id']}_{info['user_id']}",
    #             follower_id=info['user_id'],
    #             follower_name=info['user'],
    #             follower_full_name=info['is_private'],
    #             follower_pic_url=info['pic_url'],
    #             follower_is_private=info['full_name'],
    #             follow_id=foll['node']['id'],
    #             follow_name=foll['node']['username'],
    #             follow_full_name=foll['node']['full_name'],
    #             follow_pic_url=foll['node']['profile_pic_url'],
    #             follow_is_private=foll['node']['is_private']
    #         )
    #         yield item
    #     if page_info.get('has_next_page'):
    #         variables['after'] = page_info['end_cursor']
    #
    #         url_posts = f'{self.graphql_url}query_hash={self.hash_follows}&{urlencode(variables)}'
    #
    #         yield response.follow(
    #             url_posts,
    #             callback=self.follows_parse,
    #             cb_kwargs={'info': info,
    #                        'variables': deepcopy(variables)}
    #         )
    #
    # def fetch_csrf_token(self, text):
    #     matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
    #     return matched.split(':').pop().replace(r'"', '')
    #
    # def fetch_user_id(self, text, username):
    #     matched = re.search(
    #         '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
    #     ).group()
    #     return json.loads(matched).get('id')






    def __init__(self, users):
        self.users_list = users

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

    def parse_user(self, response):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            for user in self.users_list:
                yield response.follow(
                    f'/{user}',
                    callback=self.user_data_parse,
                    cb_kwargs={'user': user}
                )

    def user_data_parse(self, response: HtmlResponse, user):
        user_info = response.xpath("//script[contains(text(), 'csrf_token')]/text()") \
            .extract_first().replace("window._sharedData = ", '').replace(";", '')
        user_info = json.loads(user_info).get('entry_data', {}) \
            .get('ProfilePage', {})[0] \
            .get('graphql', {}) \
            .get('user', {})
        info = {
            'user': user,
            'user_id': user_info.get('id'),
            'pic_url': user_info.get('profile_pic_url'),
            'is_private': user_info.get('is_private'),
            'full_name': user_info.get('full_name')
        }
        variables = {"id": info['user_id'],
                     "first": 50
                     }
        url_followers = f'{self.graphql_url}query_hash={self.hash_followers}&{urlencode(variables)}'
        yield response.follow(
            url_followers,
            callback=self.followers_parse,
            cb_kwargs={'info': info,
                       'variables': deepcopy(variables)}
        )
        url_follows = f'{self.graphql_url}query_hash={self.hash_follows}&{urlencode(variables)}'
        yield response.follow(
            url_follows,
            callback=self.follows_parse,
            cb_kwargs={'info': info,
                       'variables': deepcopy(variables)}
        )

    def followers_parse(self, response, info, variables):
        j_body = json.loads(response.text)
        page_info = j_body.get('data', {}).get('user', {}).get('edge_followed_by', {}).get('page_info', {})
        followers = j_body.get('data', {}).get('user', {}).get('edge_followed_by', {}).get('edges', {})
        for follower in followers:
            item = InstaparserItem(
                _id=f"{info['user_id']}_{follower['node']['id']}",
                follow_id=info['user_id'],
                follow_name=info['user'],
                follow_full_name=info['is_private'],
                follow_pic_url=info['pic_url'],
                follow_is_private=info['full_name'],
                follower_id=follower['node']['id'],
                follower_name=follower['node']['username'],
                follower_full_name=follower['node']['full_name'],
                follower_pic_url=follower['node']['profile_pic_url'],
                follower_is_private=follower['node']['is_private']
            )

            yield item

        if page_info.get('has_next_page'):
            variables['after'] = page_info['end_cursor']

            url_posts = f'{self.graphql_url}query_hash={self.hash_followers}&{urlencode(variables)}'

            yield response.follow(
                url_posts,
                callback=self.followers_parse,
                cb_kwargs={'info': info,
                           'variables': deepcopy(variables)}
            )

    def follows_parse(self, response, info, variables):
        j_body = json.loads(response.text)
        page_info = j_body.get('data', {}).get('user', {}).get('edge_follow', {}).get('page_info', {})
        follows = j_body.get('data', {}).get('user', {}).get('edge_follow', {}).get('edges', {})
        for foll in follows:
            item = InstaparserItem(
                _id=f"{foll['node']['id']}_{info['user_id']}",
                follower_id=info['user_id'],
                follower_name=info['user'],
                follower_full_name=info['is_private'],
                follower_pic_url=info['pic_url'],
                follower_is_private=info['full_name'],
                follow_id=foll['node']['id'],
                follow_name=foll['node']['username'],
                follow_full_name=foll['node']['full_name'],
                follow_pic_url=foll['node']['profile_pic_url'],
                follow_is_private=foll['node']['is_private']
            )
            yield item
        if page_info.get('has_next_page'):
            variables['after'] = page_info['end_cursor']

            url_posts = f'{self.graphql_url}query_hash={self.hash_follows}&{urlencode(variables)}'

            yield response.follow(
                url_posts,
                callback=self.follows_parse,
                cb_kwargs={'info': info,
                           'variables': deepcopy(variables)}
            )

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

