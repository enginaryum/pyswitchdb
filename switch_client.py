import requests
import hashlib
import json
import time
from credentials import api_key, api_secret, server

base_url = 'https://{}.switchapi.com/{}'
count = 100
page = 0
order = {"type": "DESC", "by": "id"}
where = []
query_defaults = {'count': 100, "page": 0, "order": {"type": "DESC", "by": "id"}, "where": []}
default_keys = ['base_url', 'api_key', 'api_secret', 'server', 'count', 'page', 'order', 'where', 'query_defaults']
access_token = None


class Query(object):
    count = 100
    page = 0
    order = {"type": "DESC", "by": "id"}
    where = []
    query_defaults = {'count': 100, "page": 0, "order": {"type": "DESC", "by": "id"}, "where": []}

    def __init__(self, count=None, page=None, order=None, where=None):
        self.count = count
        self.page = page
        self.order = order
        self.where = where


class SwitchClient(object):
    @classmethod
    def sort(self, _by):
        q = query_defaults
        if _by.startswith('-'):
            q['order']['by'] = _by
            q['order']['type'] = "DESC"
        else:
            q['order']['type'] = "ASC"
            q['order']['by'] = _by[1:]
        self._query = q
        return self

    @classmethod
    def get_list_name(cls):
        if isinstance(cls, type):
            try:
                return cls.__name__
            except:
                return cls().__class__.__name__
        return cls.__class__.__name__

    @staticmethod
    def get_access_token():
        try:
            with open('sw_db_credentials.json') as data_file:
                data = json.load(data_file)
                if long(data["time_stamp"]) - 86400 <= long((time.time() + 0.5) * 1000):
                    access_token = _get_access_token(api_secret, api_key, server)["access_token"]
                    data["access_token"] = access_token
                    data["time_stamp"] = _default_expire_time()
                    data_file.seek(0)
                    json.dump(data, data_file)
                    data_file.truncate()
                return data["access_token"]
        except IOError:
            val = _get_access_token(api_secret, api_key, server)
            access_token = val["access_token"]
            expire_time = val["expire_time"]
            _credentials_save(access_token, expire_time)
            return access_token

    def __init__(self, access_token=None):
        self.access_token = access_token
        if access_token is None and not self.access_token:
            try:
                with open('sw_db_credentials.json') as data_file:
                    data = json.load(data_file)
                    if long(data["time_stamp"]) - 86400 <= long((time.time() + 0.5) * 1000):
                        access_token = _get_access_token(api_secret, api_key, server)["access_token"]
                        data["access_token"] = access_token
                        data["time_stamp"] = _default_expire_time()
                        data_file.seek(0)
                        json.dump(data, data_file)
                        data_file.truncate()
                    self.access_token = data["access_token"]
            except IOError:
                val = _get_access_token(api_secret, api_key, server)
                access_token = val["access_token"]
                expire_time = val["expire_time"]
                self.access_token = access_token
                _credentials_save(access_token, expire_time)

    @classmethod
    def lists(self):
        headers = {
            "APIKey": api_key,
            "AccessToken": _get_access_token(api_secret, api_key, server)["access_token"],
            "Content-type": "application/json"
        }
        try:
            return json.loads(requests.get(base_url.format(server, "Lists"), headers=headers).text)['Response']
        except Exception as e:
            print e

    def clear_query(self):
        if self._query:
            self._query = {}

    @classmethod
    def find(self, **kwargs):
        headers = {
            "APIKey": api_key,
            "AccessToken": self.get_access_token(),
            "Content-type": "application/json",
            "List": self.get_list_name()
        }
        for k, v in query_defaults.iteritems():
            try:
                if not self._query[k]:
                    self._query[k] = v
            except KeyError:
                self._query[k] = v
        self._query['list'] = headers['List']
        _where = []
        for k, v in kwargs.iteritems():
            _where.append({"type": "equal", "column": k, "value": v})
        self._query['where'] = _where
        try:
            response = requests.post(base_url.format(server, "List"), headers=headers, json=self._query)
            return map(lambda x: self(x), json.loads(response.text))
        except Exception as e:
            print e

    @classmethod
    def findOne(self, **kwargs):
        headers = {
            "APIKey": api_key,
            "AccessToken": self.get_access_token(),
            "Content-type": "application/json",
            "List": self.get_list_name()
        }
        for k, v in query_defaults.iteritems():
            try:
                if not self._query[k]:
                    self._query[k] = v
            except KeyError:
                self._query[k] = v
        self._query['list'] = headers['List']
        self._query['count'] = 1
        _where = []
        for k, v in kwargs.iteritems():
            _where.append({"type": "equal", "column": k, "value": v})
        self._query['where'] = _where
        try:
            response = requests.post(base_url.format(server, "List"), headers=headers, json=self._query)
            return map(lambda x: self(x), json.loads(response.text))
        except Exception as e:
            print e

    @classmethod
    def add(cls, json_data=None, **kwargs):
        _json = {}
        if json_data:
            _json = json_data
        else:
            for k, v in kwargs.iteritems():
                _json[k] = v
        headers = {
            "APIKey": api_key,
            "AccessToken": cls.get_access_token(),
            "List": cls.get_list_name(),
        }
        try:
            resp = json.loads(requests.post(base_url.format(server, "Add"), headers=headers, json=_json).text)
            if resp['Response'] == 'Success':
                _json['_id'] = resp['ListItemId']
                return _json
            else:
                return False
        except Exception as e:
            print e

    def _set(self, list_item_id, json_data):
        headers = {
            "APIKey": api_key,
            "AccessToken": self.get_access_token(),
            "List": self.get_list_name(),
            "ListItemId": list_item_id,
            "Content-type": "application/json"
        }
        try:
            return json.loads(requests.post(base_url.format(server, "Set"), headers=headers,
                                            json=json_data).text)
        except Exception as e:
            print e

    def delete(self, list_item_id):
        headers = {
            "APIKey": api_key,
            "AccessToken": self.get_access_token(),
            "List": self.get_list_name(),
            "ListItemId": list_item_id,
            "Content-type": "application/json"
        }
        try:
            data = requests.delete(base_url.format(server, "Set"), headers=headers)
            return json.loads(data.text)
        except Exception as e:
            print e

    class Meta:
        abstract = True


class Model(dict, SwitchClient):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """

    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

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
        if kwargs:
            if isinstance(kwargs, dict):
                for k, v in kwargs.iteritems():
                    self[k] = v
        to_update = {}
        for k, v in self.iteritems():
            if k not in ['_id', 'access_token']:
                if getattr(self, k) and k not in default_keys:
                    to_update[k] = getattr(self, k)
                    self.__setitem__(k, getattr(self, k))
                else:
                    to_update[k] = v
        try:
            if self['_id']:
                return self._set(self._id, to_update)
        except KeyError:
            created = self.add(to_update)
            if created:
                self['_id'] = created['_id']
                return self
            else:
                return False

    @classmethod
    def create(self, json_data=None, **kwargs):
        if json_data:
            created = self.add(json_data=json_data)
            if created:
                self['_id'] = created
                return self
            else:
                return False
        else:
            created = self.add(**kwargs)
            if created:
                return self(created)
            else:
                return False
    class Meta:
        abstract = False
        switchdb_model = True


def _get_access_token(api_secret, api_key, server):
    expire_time = _default_expire_time()
    m = hashlib.md5(api_secret + expire_time)
    headers = {
        "APIKey": api_key,
        "Signature": m.hexdigest(),
        "Expire": expire_time
    }

    r = requests.get("https://{}.switchapi.com/Token".format(server), headers=headers)

    try:
        access_token = json.loads(r.text)["AccessToken"]
        return {"access_token": access_token, "expire_time": expire_time}
    except Exception as e:
        print e


def _credentials_save(access_token, time_stamp):
    try:
        f = open('sw_db_credentials.json', 'w')
        f.write(json.dumps({'access_token': "{}".format(access_token), 'time_stamp': "{}".format(time_stamp)},
                           ensure_ascii=False))
        f.close()
    except Exception as e:
        print e
        return False
    return True


# default 30 days expire period(unix timestamp)
def _default_expire_time():
    return str(long((time.time() + 0.5) * 1000) + (30 * 86400))
