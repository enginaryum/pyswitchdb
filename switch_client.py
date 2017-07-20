from credentials import api_key, api_secret, server
import requests, json, functools
from _base import base_url, query_defaults, default_keys, _get_access_token
from validators import ValidationError

EMPTY_VALUES = [None, '', [], (), {}]


class Ordering(object):
	def __init__(self, cmp=None):
		self._data = []
		self._key = functools.cmp_to_key(cmp)
	
	def add(self, what): self._data.append(what)
	
	def value(self): return self._data
	
	def sort(self): self._data.sort(key=self._key)


class SwitchClient(object):
	_query = {}
	access_token = None
	
	def __init__(self, access_token=None):
		self.access_token = access_token
		if access_token is None and not self.access_token:
			self.__class__.get_access_token()
	
	@classmethod
	def order_by(cls, q, t): return Ordering(t).add(q).sort()
	
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
	def lists(cls):
		cls.fetchRequest('Lists')
		headers = cls.headers()
		try:
			return json.loads(requests.get(base_url.format(server, "Lists"), headers=headers).text)['Response']
		except Exception as e:
			print e
	
	@classmethod
	def check_query(cls):
		if cls._query == {}: cls._query = query_defaults
	
	@classmethod
	def clear_query(cls): cls._query = {}
	
	@classmethod
	def find(cls, filter=None, **kwargs):
		headers = cls.listHeaders()
		cls.check_query()
		cls._query['list'] = headers['List']
		
		if kwargs: map(lambda (x, y): cls._query['where'].append({"type": "equal", "column": x, "value": y}), [(k, v) for k, v in kwargs.iteritems()])
		if filter: map(lambda (x, y): cls._query['where'].append({"type": "equal", "column": x, "value": y}), [(k, v) for k, v in filter.iteritems()])
		try:
			response = requests.post(base_url.format(server, "List"), headers=headers, json=cls._query)
			if response.ok:
				cls.clear_query()
				result = []
				for t in json.loads(response.text):
					newObj = cls()
					for key in t.iterkeys():
						if key not in default_keys:
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
	def validateInstance(cls, instance):
		for key in instance.keys():
			try:
				for validator in getattr(cls, key).validators:
					if not validator.validate(instance[key]):
						raise ValidationError(validator, key)
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
		cls.validateInstance(cls(_json))
		try:
			resp = cls.fetchRequest("Add", json_data=_json, listRequest=True)
			if resp['Response'] == 'Success':
				_json['_id'] = resp['ListItemId']
				return _json
			else:
				return False
		except Exception as e:
			print e
	
	def _set(self, list_item_id, json_data):
		headers = self.__class__.listHeaders()
		headers['ListItemId'] = list_item_id
		try:
			return self.__class__.fetchRequest("Set", headers=headers, listRequest=True, json_data=json_data)
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
		if headers: pass
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
	
	
	class Meta: abstract = True


class Model(dict, SwitchClient):
	def __init__(self, *args, **kwargs):
		super(Model, self).__init__(*args, **kwargs)
		for arg in args:
			if isinstance(arg, dict):
				for k,v in arg.iteritems():
					self.__setitem__(k,v)
		# _args = [arg.iteritems() for arg in args if isinstance(arg, dict)]
		# map(lambda (x, y): self.__setitem__(x, y), [(k, v) for k, v in _args])
		if kwargs:
			map(lambda (x, y): self.__setitem__(x, y), [(k, v) for k, v in kwargs.iteritems()])
	
	@property
	def pk(self):
		return self._id
	
	@property
	def id(self): return self._id
	
	def __getattr__(self, attr): return self.get(attr)
	
	def __setattr__(self, key, value): self.__setitem__(key, value)
	
	def __setitem__(self, key, value):
		super(Model, self).__setitem__(key, value)
		self.__dict__.update({key: value})
	
	def __delattr__(self, item): self.__delitem__(item)
	
	def __delitem__(self, key):
		super(Model, self).__delitem__(key)
		del self.__dict__[key]
	
	def save(self, **kwargs):
		if kwargs:
			map(lambda (x, y): self.__setitem__(x, y), [(k, v) for k, v in kwargs.iteritems() if k not in default_keys])
		to_update = dict()
		map(lambda (x, y): to_update.update({x: y}), [(k, v) for k, v in self.iteritems() if k not in default_keys])
		try:
			if self['_id']:
				return self._set(self['_id'], json_data=to_update)
		except KeyError:
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
		return [key for key in cls.__dict__.keys() if not key.startswith('__')]
	
	
	class Meta:
		abstract = False
		switchdb_model = True
