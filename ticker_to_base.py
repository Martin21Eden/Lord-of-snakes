import requests
from cent import Client, CentException
import datetime
from sqlalchemy import create_engine
import time

url = "https://ws.cco-profile-develop.demo.almazor-it.info"
secret_key = "potato"
d1 = {}
our_pair = ['BTC_USD', 'ZEC_BTC', 'ETC_BTC', 'XRP_BTC', 'LTC_BTC', 'BCH_BTC', 'EOS_BTC', 'ETH_BTC']
pair_dict = {'BTC_USD' : 1, 'ZEC_BTC' : 1, 'ETC_BTC' : 1, 'XRP_BTC' : 1, 'LTC_BTC' : 1, 'BCH_BTC':1, 'EOS_BTC':1, 'ETH_BTC':1}


class Singleton:
    def __init__(self, klass):
        self.klass = klass
        self.instance = None
    def __call__(self, *args, **kwds):
        if self.instance == None:
            self.instance = self.klass(*args, **kwds)
        return self.instance


@Singleton
class Database:
    connection = None
    def get_connection(self):
        if self.connection is None:
            database = "ccoprofile_develop"
            user = "dmitry_martynuyk"
            password = "CSesD5wB9nmBa6Ye"
            host = "demo.almazor-it.info"
            port = 3306
            engine = create_engine(f"mysql+pymysql://'{user}':{password}@{host}/{database}",
                               connect_args=dict(host=host, port=port))
            self.connection = engine.connect()
            print('Connecting ..')
        # self.connection = MySQLdb.connect(host="localhost", user="root", passwd="razvan", db="mydatabase")
        return self.connection

    def get_id(self, pair):
        connection = Database().get_connection()
        result = connection.execute(f'SELECT `id` FROM `pairs` WHERE `code` = "{pair}"')
        id = None
        for row in result:
            id = row['id']
        return id


    def send_base(self, value):
        connection = Database().get_connection()
        connection.execute(f"INSERT INTO `tickers` ("
                         f"`pair_id`, `buy_price`, `sell_price`, `last_trade`, `high`, `low`, `avg`, `vol`, `vol_curr`, `open`, `close`, `updated`) VALUES ("
                         f"'{self.get_id(value['pair'])}', '{value['buy_price']}', '{value['last_trade']}', '{value['high']}', '{value['high']}', '{value['low']}', '{value['avg']}', '{value['vol']}', '{value['vol_curr']}', '{value['open']}', '{value['close']}', '{conver_with_days(value['updated'])}')")
      # time.sleep(0.2)



@Singleton
class Socket:
    connection = None
    def get_connection(self):
        if self.connection is None:
            self.connection = Client(url, secret_key, timeout=1)
            print('Connecting socket..')
            # self.connection = MySQLdb.connect(host="localhost", user="root", passwd="razvan", db="mydatabase")
        return self.connection

    def send(self, params):
        self.get_connection().add("publish", params)
        try:
            self.get_connection().send()
        except CentException as a:
            print(a)
        print(params)


def conver_with_days(num):
    convert_num = datetime.datetime.fromtimestamp(int(f"{num}")).strftime('%Y-%m-%d %H:%M:%S')
    return convert_num


def ticker():
    request = requests.post('https://api.exmo.com/v1/ticker/').json()
    for key, value in request.items():
        if key in our_pair:
            print(key)
            if pair_dict[key] == 1:
                pair_dict[key] = value['last_trade']
                # print(value)
                # print(pair_dict)
            else:
                value['interval'] = 'tick'
                value['open'] = pair_dict[key]
                value['close'] = str(value['last_trade'])
                d1[key] = value['close']
                pair_dict.update(d1)
                print(pair_dict)
                print(value)
                value['pair'] = str(''.join(key.split('_')))
                params = {
                    "channel": f"public:{''.join(key.split('_'))}",
                    "data": value
                }
                Socket().send(params)
                Database().send_base(value)
                print(value)
                time.sleep(0.5)

while 1:
    # time.sleep(1)
    ticker()



