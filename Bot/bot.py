import sys, getopt
from api import *
import os, inspect
from adminka import db, Bot

file_name = str(inspect.getfile(inspect.currentframe()).split('/')[-1])
print(file_name)

bot = Bot.query.filter_by(name=file_name).first()
print(bot.name)
bot.pid = os.getpid()
db.session.commit()
print(os.getpid())


emails = ['Sheep0' + str(num) + 'ETHBTCSELL@domain.com' for num in range(1, 22)]
def types():
    hope = next(pop)
    # global type
    if hope in [x for x in range(1, 6)]:
        type = "SELL"
        print(hope)
        return type
    elif hope in [x for x in range(6, 13)]:
        type = "BUY"
        return type
    elif hope in [x for x in range(13, 15)]:
        type = "SELL"
        return type
    elif hope in [x for x in range(15, 17)]:
        type = "BUY"
        return type
    elif hope in [x for x in range(17, 19)]:
        type = "SELL"
        return type
    elif hope in [x for x in range(19, 21)]:
        type = "BUY"
        return type
    elif hope == 21:
        type = "SELL"
        return type



def main(argv):
    email = 'client@domain.com'
    type = 'SELL'
    amount = 1
    pair = 1
    start = None

    try:
        opts, args = getopt.getopt(argv, "h:a:p:t:e:s:", ["amount=", "pair=", "type=", "email=", "start="])
    except getopt.GetoptError as o:
        print(o)
        print('bot.py -a <amount> -p <pairs> -t <type> -e <email> -s <start>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('bot.py -a <amount> -p <pair> -t <type> -e <email> -s <start>')
            sys.exit()
        elif opt in ("-a", "--amount"):
            amount = arg
        elif opt in ("-p", "--pair"):
            pair = arg
        elif opt in ("-t", "--type"):
            type = arg
        elif opt in ("-e", "--email"):
            email = arg
        elif opt in ("-s", "--start"):
            start = arg



    if start:
        for lol in emails:
            headers(email=lol, password=lol)
            list_id = [x['id'] for x in api_query('get_pairs')]
            if int(pair) in list_id:
                api_query('make_order', {'pair': pair, 'transaction_type': types(), 'quantity': 1})

    else:
        a = 0
        while a != int(amount):
            headers(email=email, password=email)
            a += 1
            list_id = [x['id'] for x in api_query('get_pairs')]
            if int(pair) in list_id:
                api_query('make_order', {'pair': pair, 'transaction_type': type, 'quantity': 1})


def number():
    for num in range(1, 22):
        yield num

pop = number()

if __name__ == "__main__":
    main(sys.argv[1:])