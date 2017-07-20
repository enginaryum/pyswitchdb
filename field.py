import collections
import datetime
from validators import *


class Field(object):
	def __init__(self, *args, **kwargs):
		super(Field, self).__init__()


class String(Field):
	def __init__(self, max_length=None, *args, **kwargs):
		super(String, self).__init__(*args, **kwargs)
		self.validators = [TypeValidator([str, unicode])]
		if max_length:
			self.max_length = max_length
			self.validators.append(MaxLengthValidator(max_length))


class Integer(Field):
	def __init__(self,  max=None, min=None, *args, **kwargs):
		super(Integer, self).__init__(*args, **kwargs)
		self.validators = [TypeValidator(int)]
		if max:
			self.max = max
			self.validators.append(MaxValueValidator(max))
		if min:
			self.min = min
			self.validators.append(MinValueValidator(min))


class Bool(Field):
	def __init__(self,  *args, **kwargs):
		super(Bool, self).__init__(*args, **kwargs)
		self.validators = [TypeValidator(bool)]


class Date(Field):
	def __init__(self, *args, **kwargs):
		super(Date, self).__init__(*args, **kwargs)
		self.validators = [TypeValidator(datetime.datetime)]


class Array(Field):
	def __init__(self,  *args, **kwargs):
		super(Array, self).__init__(*args, **kwargs)
		self.validators = [TypeValidator(list)]


class ObjectID(Field):
	def __init__(self, ref='',  *args, **kwargs):
		super(ObjectID, self).__init__(*args, **kwargs)
		self.ref = ref
		self.validators = [TypeValidator(str)]
		self.validators.append(ObjectIdValidator())
