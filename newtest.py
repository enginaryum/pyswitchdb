from models import *

a = Model(age=10, name= 'AAA')
b = Model({'age': 20, 'name': 'BBB'})
kwargs = {'age': 10, 'name': 'CCC'}
c= Model(**kwargs)
print a
print b
print c
print a.age
print a.name
print a['age']
print a['name']
a.age = 3
print a.keys()
print a.keys()
print a.items()
print a.values()
print a.has_key('name')
a.name = 'anothername'
print a.age
print a.name
a['age'] = 11
print a['age']
print a
a['name'] = 'degisiklikname'
print a.name
a.save()
print a
a.name = 'yenison'
print a
print RDB.sort('-age').find(name='namenew')
newObject = RDB.create(name='another name', age=13)
print newObject._id
print RDB.find(name='namenew')
_list = RDB.find()
for a in _list:
    print a.name
print RDB.findOne(name='name')