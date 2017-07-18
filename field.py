import collections
from django.core import validators


class Field(object):
    def __init__(self, verbose_name=None, name=None, primary_key=False,
                 max_length=None, unique=False, blank=False, null=False,
                 default=None, editable=True, choices=None, help_text='', validators=[], custom_pk=False):
        self.name = name
        self.verbose_name = verbose_name
        self._verbose_name = verbose_name
        self.primary_key = primary_key
        self.max_length, self._unique = max_length, unique
        self.blank, self.null = blank, null
        self.default = default
        self.editable = editable
        if isinstance(choices, collections.Iterator):
            choices = list(choices)
        self.choices = choices or []
        self.help_text = help_text
        self.validators = validators
        self.custom_pk = custom_pk


    # def check(self):
    #     if not self.blank and :


class String(Field):
    def __init__(self, *args, **kwargs):
        super(String, self).__init__(*args, **kwargs)
        self.validators.append(validators.MaxLengthValidator(self.max_length))
