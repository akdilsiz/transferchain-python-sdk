class TupleMixin(object):

    def __new__(cls, *args, **kwargs):
        if not kwargs:
            return super(TupleMixin, cls).__new__(cls, *args, **kwargs)

        defaults = {f: None for f in cls._fields}

        defaults.update({k: v for k, v in kwargs.items() if k in cls._fields})
        return super(TupleMixin, cls).__new__(cls, *args, **defaults)
