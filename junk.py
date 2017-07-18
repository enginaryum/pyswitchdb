#
# class Model(SwitchClient):
#     data = {}
#     def __init__(self, dict=None, *args, **kwargs):
#         super(Model, self).__init__()
#         if dict:
#             for k, v in dict.iteritems():
#                 self[k] = v
#         for arg in args:
#             if isinstance(arg, dict):
#                 for k, v in arg.iteritems():
#                     self[k] = v
#         if kwargs:
#             for k, v in kwargs.iteritems():
#                 self[k] = v
#
#     def __cmp__(self, dict):
#         return cmp(self, dict)
#
#     __hash__ = None
#
#     def __len__(self):
#         return len(self) - 1
#
#     def __getitem__(self, key):
#         if key in self:
#             return self[key]
#         if hasattr(self.__class__, "__missing__"):
#             return self.__class__.__missing__(self, key)
#         raise KeyError(key)
#
#
#     def __repr__(self):
#         _repr = {}
#         for k in self.keys():
#             _repr[k] = self[k]
#         return repr(_repr)
#
#     def __setitem__(self, key, val):
#         self[key] = val
#
#     def __setattr__(self, key, value):
#         self.__setitem__(self, key, value)
#
#     def __getattr__(self, key):
#         if self[key]:
#             return self[key]
#         return self.__getitem__(key)
#
#     def __delitem__(self, key):
#         del self.data[key]
#
#     def clear(self):
#         self.data.clear()
#
#     def copy(self):
#         if self.__class__ is Model:
#             return Model(self.data.copy())
#         import copy
#         data = self.data
#         try:
#             self.data = {}
#             c = copy.copy(self)
#         finally:
#             self.data = data
#         c.update(self)
#         return c
#
#     def keys(self):
#         keys = self.data.keys()
#         keys.remove('access_token')
#         return keys
#
#     def items(self):
#         return self.items()
#
#     def iteritems(self):
#         return self.iteritems()
#
#     def iterkeys(self):
#         return self.iterkeys()
#
#     def itervalues(self):
#         return self.itervalues()
#
#     def values(self):
#         return self.values()
#
#     def values_list(self, list=None):
#         if list:
#             return map(lambda x: self[x], list)
#         else:
#             return self
#
#     def has_key(self, key):
#         return key in self.data
#
#     def get(self, key, failobj=None):
#         if key not in self:
#             return failobj
#         return self[key]
#
#     def setdefault(self, key, failobj=None):
#         if key not in self:
#             self[key] = failobj
#         return self[key]
#
#     def pop(self, key, *args):
#         return self.pop(key, *args)
#
#     def popitem(self):
#         return self.popitem()
#
#     def __contains__(self, key):
#         return key in self.data
#
#     @classmethod
#     def fromkeys(cls, iterable, value=None):
#         d = cls()
#         for key in iterable:
#             d[key] = value
#         return d

