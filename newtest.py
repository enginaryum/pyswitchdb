from models.models import *

a= Model()
keys = Model.keys()
for key in keys:
    val = getattr(a, key)
    print val

a = Model(age=10, name= 'AAA')
b = Model({'age': 20, 'name': 'BBB'})
kwargs = {'age': 10, 'name': 'CCC'}
c = Model(**kwargs)
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
print a.pk
print a.id
a.name = 'yenison'
print a
print Model.sort('-age').find(name='namenew')
newObject = Model.create(state='another name', startingPrice=13)
print newObject
print newObject.values()
print newObject.itervalues()
print newObject._id
print Model.find(name='namenew')
_list = Model.find()
for a in _list:
    print a.name
print Model.count(-1).find()
print Model.findOne(name='name')
Model.sort('-name').count(-1).page(1).find()
Model.populateAll().findOne()
Model.populate('user').findOne()
