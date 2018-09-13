from infi.clickhouse_orm.database import Database
from infi.clickhouse_orm.models import Model
from infi.clickhouse_orm.fields import *
from infi.clickhouse_orm.engines import MergeTree


db = Database('default')

    # db.raw('CREATE TABLE IF NOT EXISTS rates')


# db.raw('DROP TABLE IF EXISTS rates')
class Rates(Model):
   event_date = DateField()
   event_time = DateTimeField()
   code = StringField()
   time = Int32Field()
   close = Float32Field()
   high = Float32Field()
   low = Float32Field()
   open = Float32Field()
   volumefrom = Float32Field()
   volumeto = Float32Field()

   engine = MergeTree('event_date', ['event_date', 'time', 'code'])

db.create_table(Rates)

def send_base(one):
    """insert to base"""
    db.insert([Rates(
        code=one['code'],
        event_date=conver_in_year(one['time']),
        event_time=conver_with_days(one['time']),
        time=one['time'],
        close=one['close'],
        high=one['high'],
        low=one['low'],
        open=one['open'],
        volumefrom=one['volumefrom'],
        volumeto=one['volumeto'])
    ])

def conver_in_year(num):
    ''' конвертация с Timestamp in human time '''
    # num = '1528011180'
    convert_num = datetime.datetime.fromtimestamp(int(f"{num}")).strftime('%Y-%m-%d')
    # print(convert_num)
    return convert_num


def conver_with_days(num):
    # num = '1528011180'
    convert_num = datetime.datetime.fromtimestamp(int(f"{num}")).strftime('%Y-%m-%d %H:%M:%S')
    # print(convert_num)
    return convert_num

# print(db.raw('SHOW TABLES'))
# print(db.raw('SELECT * FROM rates'))