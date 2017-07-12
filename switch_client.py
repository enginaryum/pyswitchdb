import requests
import hashlib
import json
import time
from credentials import api_key, api_secret, server

class SwitchClient(object):
    base_url = 'https://{}.switchapi.com/{}'
    api_key = api_key
    api_secret = api_secret
    server = server

    @classmethod
    def get_list_name(self):
        if isinstance(self, type):
            return self().__class__.__name__
        return self.__class__.__name__

    @classmethod
    def get_access_token(self):
        try:
            with open('sw_db_credentials.json') as data_file:
                data = json.load(data_file)
                if long(data["time_stamp"]) - 86400 <= long((time.time() + 0.5) * 1000):
                    access_token = _get_access_token(self.api_secret, self.api_key, self.server)["access_token"]
                    data["access_token"] = access_token
                    data["time_stamp"] = _default_expire_time()
                    data_file.seek(0)
                    json.dump(data, data_file)
                    data_file.truncate()
                return data["access_token"]
        except IOError:
            val = _get_access_token(self.api_secret, self.api_key, self.server)
            access_token = val["access_token"]
            expire_time = val["expire_time"]
            _credentials_save(access_token, expire_time)
            return access_token

    def __init__(self, access_token=None):
        if server is None:
            self.server = 'tr01'
            print 'Server name is not provided, using "'"tr01"'" as default'
        else:
            self.server = server
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        if access_token is None and not self.access_token:
            try:
                with open('sw_db_credentials.json') as data_file:
                    data = json.load(data_file)
                    if long(data["time_stamp"]) - 86400 <= long((time.time() + 0.5) * 1000):
                        access_token = _get_access_token(self.api_secret, self.api_key, self.server)["access_token"]
                        data["access_token"] = access_token
                        data["time_stamp"] = _default_expire_time()
                        data_file.seek(0)
                        json.dump(data, data_file)
                        data_file.truncate()
                    self.access_token = data["access_token"]
            except IOError:
                val = _get_access_token(self.api_secret, self.api_key, self.server)
                access_token = val["access_token"]
                expire_time = val["expire_time"]
                self.access_token = access_token
                _credentials_save(access_token, expire_time)

    @classmethod
    def lists(self):
        headers = {
            "APIKey": self.api_key,
            "AccessToken": _get_access_token(api_secret, api_key, server)["access_token"],
            "Content-type": "application/json"
        }
        try:
            return json.loads(requests.get(self.base_url.format(self.server, "Lists"), headers=headers).text)['Response']
        except Exception as e:
            print e

    @classmethod
    def list(self, query={}):
        headers = {
            "APIKey": self.api_key,
            "AccessToken": self.get_access_token(),
            "List": self.get_list_name(),
            "Content-type": "application/json"
        }
        query['list'] = self.get_list_name()
        try:
            _data = json.loads(requests.post(self.base_url.format(self.server, "List"), headers=headers, json=query).text)

            if isinstance(self, type):
                return map(lambda x: self(x),  _data)
            return map(lambda x: type(self)(x), _data)

        except Exception as e:
            print e

    @classmethod
    def add(self, json_data=None, **kwargs):
        _json = {}
        if json_data:
            _json=json_data
        else:
            for k, v in kwargs.iteritems():
                _json[k] = v
        headers = {
            "APIKey": self.api_key,
            "AccessToken": self.get_access_token(),
            "List": self.get_list_name(),
        }
        try:
            data = requests.post(self.base_url.format(self.server, "Add"), headers=headers,
                                 json=_json)
            print data.text
        except Exception as e:
            print e

    def update(self, list_item_id, json_data):
        headers = {
            "APIKey": self.api_key,
            "AccessToken": self.get_access_token(),
            "List": self.get_list_name(),
            "ListItemId": list_item_id,
            "Content-type": "application/json"
        }
        try:
            data = requests.post(self.base_url.format(self.server, "Set"), headers=headers,
                                 json=json_data)
            print data.text
        except Exception as e:
            print e

    def delete(self, list_item_id):
        headers = {
            "APIKey": self.api_key,
            "AccessToken": self.get_access_token(),
            "List": self.get_list_name(),
            "ListItemId": list_item_id,
            "Content-type": "application/json"
        }
        try:
            data = requests.delete(self.base_url.format(self.server, "Set"), headers=headers)
            print data.text
        except Exception as e:
            print e

    class Meta:
        abstract = True

class A(SwitchClient):
    def __init__(self):
        super(SwitchClient, self).__init__()

class Q(A):
    def __init__(self):
        super(Q, self).__init__()

from UserDict import UserDict

class Model(SwitchClient, UserDict):

    def __repr__(self):
        return repr(self.data)

    @classmethod
    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            return None

    def __getattr__(self, key):
        return self[key]

    def __init__(self, dict=None):
        super(Model, self).__init__()
        if dict is not None:
            self.data = {}
            self.data.update(dict)

    def clear(self):
        self.data.clear()

    def copy(self):
        if self.__class__ is Model:
            return Model(self.data)
        import copy
        return copy.copy(self)

    def keys(self):
        return self.data.keys()

    def items(self):
        return self.data.items()

    def values(self):
        return self.data.values()

    class Meta:
        abstract = False
        switchdb_model = True

    def save(self, **kwargs):
        if kwargs:
            if isinstance(kwargs, dict):
                for k, v in kwargs.iteritems():
                    self[k] = v
        return self.add(self.data)

    @classmethod
    def create(self, json_data=None, **kwargs):
        if json_data:
            self.add(json_data=json_data)
        return self.add(**kwargs)


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


class Field(object):


    def __init__(self, fieldname=None):
        Field.__init__(self)
        self["fieldname"] = fieldname

    def __repr__(self):
        return self.data[self.name]

    bool = False
    int = 0
    list = []
    dict = {}

class String(Field):

    def __init__(self, fieldname=None):
        Field.__init__(self)
        self["fieldname"] = fieldname

    def __setitem__(self, key, value):
        Field.__setitem__(self, key, value)
