from __future__ import unicode_literals
import re

EMPTY_VALUES = [None, '', [], (), {}]
NON_FIELD_ERRORS = '__all__'


class ValidationError(Exception):
  def __init__(self, cl, value):
    self.message = str(type(cl).__name__ + ' @key: "' + value + '" ')

  def __str__(self):
    return repr(self.message)


class IrrelevantKeyError(Exception):
  def __init__(self, key):
    self.message = "Field is not declared: '" + key + "'"

  def __str__(self):
    return repr(self.message)


class UniqueValueError(Exception):
  def __init__(self, key, value):
    self.message = 'value: ' + value + ' @key: "' + key + '" '

  def __str__(self):
    return repr(self.message)


class JsonValidationError(Exception):
  def __init__(self, key):
    self.message = ' @key: "' + key + '" '

  def __str__(self):
    return repr(self.message)


class TypeValidator(object):
  def __init__(self, base):
    self.base = base

  def validate(self, a):
    if a in EMPTY_VALUES:
      return True
    if type(self.base) == list:
      return type(a) in self.base
    elif type(self.base) == int:
      try:
        int(a)
      except:
        pass
    return type(a) == self.base


class MaxLengthValidator(object):
  def __init__(self, base):
    self.base = base

  def validate(self, a):
    return self.base >= len(a)


class RequiredValidator:
  def __init__(self):
    pass

  @staticmethod
  def validate(val):
    return val not in EMPTY_VALUES


class ObjectIdValidator:
  def __init__(self):
    pass

  @staticmethod
  def validate(val):
    v1 = len(val) == 24
    v2 = any(l.isdigit() for l in val)
    v3 = any(l.isupper() for l in val)
    return v1 and v2 and not v3


class MaxValueValidator:
  def __init__(self, base):
    self.base = base

  def validate(self, val):
    return val < self.base


class MinValueValidator:
  def __init__(self, base):
    self.base = base

  def validate(self, val):
    return val > self.base


class JsonValidator:
  def __init__(self, base):
    self.baseKeys = base.keys()

  def validate(self, val):
    if len(self.baseKeys) > 0:
      for k in val.keys():
        if k not in self.baseKeys:
          raise JsonValidationError(k)
    return True
