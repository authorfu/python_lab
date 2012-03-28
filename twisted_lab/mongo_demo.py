from pymongo import Connection
from sec_timer import loop_in_sec
import json

connection = Connection()

db = connection.mongo_lab

test = db.test


data = {'name': 'yanjianbo', 'email': 'yanshiyi1983@163.com'}
ds = json.dumps(data)

for i in loop_in_sec(1):
    test.insert(data)

print '%d items inserted' %i
