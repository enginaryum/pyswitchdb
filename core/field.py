import collections
import datetime
from validators import *


class Field(object):
  def __init__(self, unique=False, *args, **kwargs):
    super(Field, self).__init__()
    self.unique = unique


class String(Field):
  def __init__(self, required=False, unique=False, max_length=None, *args, **kwargs):
    super(String, self).__init__(*args, **kwargs)
    self.validators = [TypeValidator([str, unicode])]
    if max_length:
      self.max_length = max_length
      self.validators.append(MaxLengthValidator(max_length))
    if required:
      self.validators.append(RequiredValidator())
    self.unique = unique


class Integer(Field):
  def __init__(self, required=False, custom_pk=False, unique=False, max=None, min=None, *args, **kwargs):
    super(Integer, self).__init__(*args, **kwargs)
    self.validators = [TypeValidator([int, long, float, complex])]
    if max:
      self.max = max
      self.validators.append(MaxValueValidator(max))
    if min:
      self.min = min
      self.validators.append(MinValueValidator(min))
    self.unique = unique
    if required:
      self.validators.append(RequiredValidator())
    self.custom_pk = custom_pk


class Bool(Field):
  def __init__(self, *args, **kwargs):
    super(Bool, self).__init__(*args, **kwargs)
    self.validators = [TypeValidator(bool)]


class Date(Field):
  def __init__(self, required=False, *args, **kwargs):
    super(Date, self).__init__(*args, **kwargs)
    self.validators = [TypeValidator(datetime.datetime)]
    self.required = required
    if required:
      self.validators.append(RequiredValidator())


class Array(Field):
  def __init__(self, field, required=False, *args, **kwargs):
    super(Array, self).__init__(*args, **kwargs)
    self.field = field
    self.validators = [TypeValidator(list)]
    self.required = required
    if required:
      self.validators.append(RequiredValidator())


class ObjectID(Field):
  def __init__(self, required=False, ref='', *args, **kwargs):
    super(ObjectID, self).__init__(*args, **kwargs)
    self.ref = ref
    self.validators = []
    self.validators.append(ObjectIdValidator())
    self.required = required
    if required:
      self.validators.append(RequiredValidator())


class Json(Field):
  def __init__(self, json, required=False, *args, **kwargs):
    super(Json, self).__init__(*args, **kwargs)
    self.json = json
    self.validators = [TypeValidator(dict)]
    self.validators.append(JsonValidator(json))
    self.required = required
    if required:
      self.validators.append(RequiredValidator())


class Enum(Field):
  def __init__(self, choice_cl, required=False, default=None, *args, **kwargs):
    super(Enum, self).__init__(*args, **kwargs)
    self.choice_cl = choice_cl
    self.required = required
    self.default = default
    self.validators = [TypeValidator(choice_cl.Meta.choice_type)]
    self.validators.append(MaxLengthValidator(choice_cl.Meta.max_length))
    if required:
      self.validators.append(RequiredValidator())
