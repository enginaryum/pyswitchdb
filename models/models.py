from db.switch_client import Model
from db.field import *
from slugify import slugify
import datetime
from enums import *

budget = {'amount': '', 'currency': 'TL'}


class Budget(dict):
  amount = ''
  currency_str = 'TL'

  def __init__(self, amount, currency_str='TL'):
    super(Budget, self).__init__()
    self.amount = amount
    self.currency_str = currency_str

  def __repr__(self):
    return repr(str(self.amount) + ' ' + self.currency_str)


class TimeStamped(Model):
  created = String(default=str(datetime.datetime.now()))
  updated = String(default=str(datetime.datetime.now()))

  def save(self, **kwargs):
    self.updated = str(datetime.datetime.now())
    return super(TimeStamped, self).save(**kwargs)


class Slugged(Model):
  title = String()
  slug = String()

  def save(self, **kwargs):
    self.slug = slugify(self.title)
    super(Slugged, self).save(**kwargs)


class Country(Model):
  name = String()


class City(Model):
  country = String(required=True)
  title = String()
  slug = String()
  code = Integer()


class District(Model):
  city = Integer(required=True)
  title = String()
  slug = String()
  code = Integer()


class Hood(Model):
  district = String(required=True)
  name = String()


class Address(Model):
  country = ObjectID(ref=Country)
  city = ObjectID(ref=City)
  district = ObjectID(ref=District)
  hood = ObjectID(ref=Hood)


class Media(TimeStamped):
  file_path = String()
  media_type = Enum(MediaTypes)
