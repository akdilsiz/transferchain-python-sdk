import json


class TupleMixin(object):
    '''Namedtuple mixin was used because we want to leave some values empty.'''

    def __new__(cls, *args, **kwargs):
        if not kwargs:
            return super(TupleMixin, cls).__new__(cls, *args, **kwargs)

        defaults = {f: None for f in cls._fields}
        defaults.update({k: v for k, v in kwargs.items() if k in cls._fields})
        return super(TupleMixin, cls).__new__(cls, *args, **defaults)

    def dump(self):
        '''Named tuple to json'''
        data = {k: getattr(self, k) for k in self._fields}
        return json.dumps(data).encode('utf-8')
