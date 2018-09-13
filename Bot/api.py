import requests
url = 'https://api.cco-profile-develop.demo.almazor-it.info/profile/v1/auth/'

header = None
def headers(**kwargs):
    payload = {'grant_type': 'password', 'client_id': '1_1odqv04f75og84w8g8goo0ck8k404ssc0wwk8ss444w8kw4040',
               'client_secret': '5k20u1xfodssg8wco00s80sccg8k44o4ckk800c4ssookg8owc'}

    if kwargs:
        payload.update(kwargs)
    else:
        payload = {'grant_type': 'password', 'client_id': '1_1odqv04f75og84w8g8goo0ck8k404ssc0wwk8ss444w8kw4040',
                   'client_secret': '5k20u1xfodssg8wco00s80sccg8k44o4ckk800c4ssookg8owc', 'email': 'client@domain.com',
                   'password': 'client@domain.com'}
    global header
    if not header:
        r = requests.post(url, data=payload).json()
        header = {'Authorization': f'Bearer {(r["access_token"])}'}
    return header




def api_query(command, data={}):
    url_order = 'https://api.cco-profile-develop.demo.almazor-it.info/market/v1/'
    if (command == "make_order"):
        request = requests.post(url_order + 'orders/', data=data, headers=headers()).json()
        print(request)
        return request
    elif(command == 'get_pairs'):
        request = requests.get(url_order + 'pairs/?tradable=1&limit=1000', headers=headers()).json()
        # print(request)
        return request

    #     ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/public?command=' + command))
    #     return json.loads(ret.read())
    # elif (command == "returnOrderBook"):
    #     ret = urllib2.urlopen(urllib2.Request(
    #         'https://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair'])))
    #     return json.loads(ret.read())
    # elif (command == "returnMarketTradeHistory"):
    #     ret = urllib2.urlopen(urllib2.Request(
    #         'https://poloniex.com/public?command=' + "returnTradeHistory" + '&currencyPair=' + str(
    #             req['currencyPair'])))
    #     return json.loads(ret.read())
    # elif (command == "returnChartData"):
    #     ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/public?command=returnChartData&currencyPair=' + str(
    #         req['currencyPair']) + '&start=' + str(req['start']) + '&end=' + str(req['end']) + '&period=' + str(
    #         req['period'])))
    #     return json.loads(ret.read())
    # else:
    #     req['command'] = command
    #     req['nonce'] = int(time.time() * 1000)
    #     post_data = urllib.urlencode(req)
    #
    #     sign = hmac.new(self.Secret, post_data, hashlib.sha512).hexdigest()
    #     headers = {
    #         'Sign': sign,
    #         'Key': self.APIKey
    #     }
    #
    #     ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data, headers))
    #     jsonRet = json.loads(ret.read())
    #     return self.post_process(jsonRet)

