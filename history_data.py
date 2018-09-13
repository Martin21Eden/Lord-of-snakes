import requests
import datetime
import json
from Base import *


def fun_coin():
    ''' беру одну монету из списка и удаляю ее, сохраняю ее в ласт с новой датой '''

    with open('ICOHistoricalRates/data/data.txt', 'r+') as fon:
        data = json.load(fon)
        first_coin = data[0]
        del data[0]
        fon.seek(0)
        json.dump(data, fon, indent=4)
        fon.truncate()

    with open('ICOHistoricalRates/data/last.txt', 'r+') as json_file1:
        data1 = json.load(json_file1)
        data1[0] = first_coin
        data1[1]['time'] = 1522454400
        json_file1.seek(0)
        json.dump(data1, json_file1, indent=4)
        json_file1.truncate()


def coin():
    """Возвращаю первую монету со списка монет"""
    with open("ICOHistoricalRates/data/data.txt") as json_file:
        data = json.load(json_file)[0]
    return data


def lastcoin():
    """Возвращаю последнюю монету со сохр последнего json"""
    with open('ICOHistoricalRates/data/last.txt') as json_file1:
        last_coin = json.load(json_file1)[0]
    return last_coin


def save_last_data(coin, last_one):
    """сохраняю последнюю монету и json"""
    with open('ICOHistoricalRates/data/last.txt', 'w') as outfile:
        json.dump([coin, last_one], outfile)


def read_last_data():
    """возвращаю последнюю дату json"""
    with open('ICOHistoricalRates/data/last.txt') as json_file1:
        # last_coin = json.load(json_file1)[0]
        last_time = json.load(json_file1)[1]['time']
    return last_time

limit = 100
a = 0
pop_list = []
def last_date():
    """проверяю первый ли раз запускается скрипт и return last date"""
    global a
    if a == 0:
       lst_dt = read_last_data()
       a = a + 1
       return lst_dt
    else:
        return pop_list.pop(0)


def main():
    while True:
         url = f'https://min-api.cryptocompare.com/data/histoday?fsym={lastcoin()}&tsym=USD&limit={limit}&toTs={last_date()}'
         request = requests.get(url).json()
         pop_list.append(request['TimeFrom'])
         list_from_json = request["Data"]
         del list_from_json[0]
         last_one = list_from_json[-1]
         save_last_data(coin(), last_one)
         for one in list_from_json:
              if one['high'] == 0:
                    fun_coin()
              else:
                    one['code'] = coin()
                    Base.send_to_base(one)

