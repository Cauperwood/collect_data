# import quandl
#
# quandl.ApiConfig.api_key = "6yCthmrFHkis-U_scS9T"
# data = quandl.get("WIKI/UAL")
# print(data)
# data.shape()
import requests
from pprint import pprint
import json

main_link = 'https://cloud.iexapis.com/stable/stock/ual/batch'
token = 'pk_5c1840a3d10f4266b81fe546be43b3ef'
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'Accept': '*/*'}
params = {'types': 'chart',
	'token': token}
response = requests.get(main_link, headers=header, params=params)
if response.ok:
    data = json.loads(response.text)
pprint(data)

