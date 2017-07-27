import copy
from datetime import datetime

import json
import requests

from _base import base_url, query_defaults, default_keys, _get_access_token
from core.credentials import api_key, api_secret, server
from validators import ValidationError, UniqueValueError, IrrelevantKeyError, RequiredValidator

EMPTY_VALUES = [None, '', [], (), {}]


class SwitchClient(object):
  _query = {}
  access_token = None

  def __init__(self, access_token=None):
    self.access_token = access_token
    if access_token is None and not self.access_token:
      self.__class__.get_access_token()

  @classmethod
  def populate(cls, key):
    cls.check_query()
    cls._query['join'] = {"localField": key, "foreignField": "id", "nodeAs": key, "remoteList": getattr(getattr(cls, key), 'ref').__name__}
    return cls

  @classmethod
  def sort(cls, _by):
    cls.check_query()
    if _by.startswith('-'):
      cls._query['order']['by'] = _by[1:]
      cls._query['order']['type'] = "DESC"
    else:
      cls._query['order']['type'] = "ASC"
      cls._query['order']['by'] = _by
    return cls

  @classmethod
  def count(cls, count):
    cls.check_query()
    cls._query['count'] = count
    return cls

  @classmethod
  def page(cls, page):
    cls.check_query()
    cls._query['page'] = page
    return cls

  @classmethod
  def get_list_name(cls):
    return cls.__name__

  @classmethod
  def get_access_token(cls):
    if not cls.access_token:
      cls.access_token = _get_access_token(api_secret, api_key, server)["access_token"]
    return cls.access_token

  @classmethod
  def headers(cls):
    return {"APIKey": api_key, "AccessToken": cls.get_access_token(), "Content-type": "application/json"}

  @classmethod
  def listHeaders(cls):
    return {"APIKey": api_key, "AccessToken": cls.get_access_token(), "Content-type": "application/json", "List": cls.get_list_name()}

  @classmethod
  def create_custom_pk_for_cl(cls, cl):
    headers = cls.headers()
    headers["List"] = "CustomPkCounter"
    response = requests.post(base_url.format(server, "Add"), headers=headers, json={"cl": cl, "count": 1})
    if response.ok:
      return json.loads(response.text)

  @classmethod
  def handle_custom_pk(cls):
    query = query_defaults
    query['count'] = 1
    query['list'] = 'CustomPkCounter'
    query['where'].append({"type": "equal", "column": "cl", "value": cls.__name__})
    headers = cls.headers()
    last = json.loads(requests.post(base_url.format(server, "List"), headers=headers, json=query).text)
    if last not in EMPTY_VALUES:
      return last[0]['count'] + 1
    cls.create_custom_pk_for_cl(cls.__name__)
    return 1

  @classmethod
  def lists(cls):
    cls.fetchRequest('Lists')
    headers = cls.headers()
    try:
      return json.loads(requests.get(base_url.format(server, "Lists"), headers=headers).text)['Response']
    except Exception as e:
      print e

  @classmethod
  def check_query(cls):
    if cls._query == {}:
      cls._query = copy.deepcopy(query_defaults)

  @classmethod
  def clear_query(cls):
    cls._query = {}

  @classmethod
  def find(cls, filter=None, **kwargs):
    headers = cls.listHeaders()
    cls.check_query()
    cls._query['list'] = headers['List']
    if kwargs: map(lambda (x, y): cls._query['where'].append({"type": "equal", "column": x, "value": y}), [(k, v) for k, v in kwargs.iteritems()])
    if filter: map(lambda (x, y): cls._query['where'].append({"type": "equal", "column": x, "value": y}), [(k, v) for k, v in filter.iteritems()])
    try:
      import json
      response = requests.post(base_url.format(server, "List"), headers=headers, json=cls._query)
      if response.status_code == 401:
        cls.get_access_token()
      cls._query = {}
      if response.ok:
        _result = json.loads(response.text)
        if type(_result) == list:
          if len(_result) == 1:
            result = _result[0]
            newObj = cls()
            for key in result.iterkeys():
              newObj[key] = result[key]
            return newObj
          else:
            result = []
            for t in json.loads(response.text):
              newObj = cls()
              for key in t.iterkeys():
                newObj[key] = t[key]
              result.append(newObj)
            return result
    except Exception as e:
      print e

  @classmethod
  def findOne(cls, **kwargs):
    cls.check_query()
    cls._query['count'] = 1
    return cls.find(**kwargs)

  @classmethod
  def findOneById(cls, id):
    cls.check_query()
    cls._query['count'] = 1
    return cls.find(id=id)

  @staticmethod
  def getOrNone(i, k):
    try:
      return i[k]
    except KeyError:
      return None

  @classmethod
  def validateInstance(cls, instance):
    clsKeys = cls.keys()
    for k in instance.keys():
      if k not in clsKeys:
        raise IrrelevantKeyError(k)
    for key in clsKeys:
      try:
        # Query db to check unique statement
        field = getattr(cls, key)
        # Handle if field is custom_pk
        try:
          if field.custom_pk:
            setattr(instance, key, cls.handle_custom_pk())
        except AttributeError:
          pass

        val = cls.getOrNone(instance, key)
        # Handle no value statement
        noneOrEmpty = not val or val in EMPTY_VALUES
        if noneOrEmpty:
          # Set default value if instance have default but not assigned value on key
          try:
            if field.default:
              setattr(instance, key, field.default)
          except AttributeError:
            pass
          try:
            if field.required:
              raise ValidationError(RequiredValidator, key)
          except AttributeError:
            pass

        else:
          # Check if ObjectID field has value different from str;
          # if true create object and assign result's _id to ObjectID field
          if type(field).__name__ == 'ObjectID' and type(instance[key]) not in [str, unicode]:
            created = field.ref.create(instance[key])
            setattr(instance, key, created['_id'])

          # Query if field is unique
          if field.unique:
            _kwargs = {key: val}
            if len(cls.findOne(**_kwargs)) > 0:
              raise UniqueValueError(key, val)

          val = instance[key]
          # Validate
          for validator in field.validators:
            if not validator.validate(val):
              raise ValidationError(validator, key)

          # Validate objects in Array Field
          if type(field).__name__ == 'Array':
            try:
              for validator in field.field.validators:
                for _instance in val:
                  if not validator.validate(_instance):
                    raise ValidationError(validator, key)
            except KeyError:
              pass

      except KeyError:
        pass
    return True

  @classmethod
  def add(cls, json_data=None, **kwargs):
    _json = {}
    if json_data:
      _json = json_data
    if kwargs:
      _json.update(**kwargs)
    _json['created'] = str(datetime.now())
    # Handle validations and defaults
    rawObj = cls(_json)
    cls.validateInstance(rawObj)
    try:
      resp = cls.fetchRequest("Add", json_data=rawObj, listRequest=True)
      if resp['Response'] == 'Success':
        rawObj['_id'] = resp['ListItemId']
        return rawObj
      else:
        return False
    except Exception as e:
      print e

  @classmethod
  def bulk_insert(cls, json_array):
    return cls.fetchRequest("Add", json_data=json_array, listRequest=True)

  def _set(self, list_item_id, json_data):
    obj = type(self).findOneById(list_item_id)
    for k, v in obj.iteritems():
      if k not in default_keys:
        try:
          if json_data[k]:
            pass
        except KeyError:
          json_data[k] = v
    for k, v in json_data.iteritems():
      try:
        field = getattr(type(self), k)
        if type(field).__name__ == 'ObjectID' and type(v) not in [str, unicode]:
          json_data[k] = field.ref.create(v)['_id']
      except AttributeError:
        pass

    headers = self.__class__.listHeaders()
    headers['ListItemId'] = list_item_id
    try:
      # Query db and check response status, if success return json
      response = self.__class__.fetchRequest("Set", headers=headers, listRequest=True, json_data=json_data)
      if response['Response'] == 'Success':
        obj['_id'] = list_item_id
        return obj
    except Exception as e:
      print e

  def delete(self, list_item_id):
    headers = self.__class__.listHeaders()
    headers['ListItemId'] = list_item_id
    try:
      return json.loads(requests.delete(base_url.format(server, "Set"), headers=headers).text)
    except Exception as e:
      print e

  @classmethod
  def fetchRequest(cls, method, json_data=None, listRequest=False, headers=None):
    if headers:
      pass
    elif listRequest:
      headers = cls.listHeaders()
    else:
      headers = cls.headers()
    try:
      if json_data:
        response = requests.post(base_url.format(server, method), headers=headers, json=json_data)
      else:
        response = requests.post(base_url.format(server, method), headers=headers)
      if response.ok:
        return json.loads(response.text)
    except Exception as e:
      return e

  class Meta:
    abstract = True


class Model(dict, SwitchClient):
  def __init__(self, *args, **kwargs):
    super(Model, self).__init__(*args, **kwargs)
    if args:
      for arg in args:
        if isinstance(arg, dict):
          for k, v in arg.iteritems():
            self.__setitem__(k, v)
    if kwargs:
      map(lambda (x, y): self.__setitem__(x, y), [(k, v) for k, v in kwargs.iteritems()])

  @property
  def pk(self):
    return self.id

  def __getattr__(self, attr):
    return self.get(attr)

  def __setattr__(self, key, value):
    self.__setitem__(key, value)

  def __setitem__(self, key, value):
    super(Model, self).__setitem__(key, value)
    self.__dict__.update({key: value})

  def __delattr__(self, item):
    self.__delitem__(item)

  def __delitem__(self, key):
    super(Model, self).__delitem__(key)
    del self.__dict__[key]

  def save(self, **kwargs):
    # Update instance if function call has keyword arguments
    if kwargs:
      map(lambda (x, y): self.__setitem__(x, y), [(k, v) for k, v in kwargs.iteritems() if k not in default_keys])
    to_update = dict()
    map(lambda (x, y): to_update.update({x: y}), [(k, v) for k, v in self.iteritems() if k not in default_keys])

    # Update or create
    try:
      # Update if instance has _id
      if self._id:
        return self._set(self._id, json_data=to_update)
    except KeyError:
      # Create new instance if _id not provided
      saved = self.__class__.add(to_update)
      if saved:
        self.update(saved)
        return self
      else:
        return False

  @classmethod
  def create(cls, json_data=None, **kwargs):
    if json_data:
      created = cls.add(json_data=json_data)
      if created:
        return cls(created)
      else:
        return False
    else:
      created = cls.add(**kwargs)
      if created:
        return cls(created)
      else:
        return False

  @classmethod
  def keys(cls):
    bases = []
    import inspect
    print cls.__dict__.keys()
    for cl in inspect.getmro(cls):
      try:
        if cl.Meta.switchdb_model:
          bases.append(cl)
      except:
        pass
    keys = []
    for _list in [[key for key in cl.__dict__.keys() if not key.startswith('__') and key not in default_keys and not inspect.ismethod(getattr(cl, key))
    and not inspect.isclass(getattr(cl, key))] for cl in bases]:
      keys += _list
    return keys

  class Meta:
    abstract = False
    switchdb_model = True
