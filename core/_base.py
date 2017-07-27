import requests, hashlib, json, time

base_url = 'https://{}.switchapi.com/{}'
query_defaults = {'count': 100, "page": 0, "order": {"type": "DESC", "by": "id"}, "where": []}
default_keys = ['_id', 'id', '_query', 'access_token', 'pk']


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


# default 3000 days expire period(unix timestamp)
def _default_expire_time():
  return str(long((time.time() + 0.5) * 1000) + (30 * 8640000000))
