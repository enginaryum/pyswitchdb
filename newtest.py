from models import *

kwargs = {'age': 10, 'name': 'namenew'}
a = RDB({'age': 1, 'name': 'name'})

print a
print a['age']
print a['name']
print a.age
print a.name
print getattr(a, 'age')
print getattr(a, 'name')
print a.keys()
print a.items()
print a.values()
a.clear()
print a



RDB.create(**kwargs)
RDB.create(kwargs)


RDB.lists()

c = RDB.list(query={
    "count": 100,
    "page": 0,
    "where": [],
    "order": {
        "type": "DESC",
        "by": "id"
    }})
for a in c:
    print a.name