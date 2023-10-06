import json


class TupleMixin(object):

    def __new__(cls, *args, **kwargs):
        if not kwargs:
            return super(TupleMixin, cls).__new__(cls, *args, **kwargs)

        defaults = {f: None for f in cls._fields}
        defaults.update({k: v for k, v in kwargs.items() if k in cls._fields})
        return super(TupleMixin, cls).__new__(cls, *args, **defaults)

    def to_json(self, with_pascal_case=False):
        '''
        snake_case to PascalCase. max deep two!
        t = TestTuple(test_one=1, test_two=2)
        t.to_json(with_pascal_case=True) -> {"TestOne": 1, "TestTwo": 2}
        '''
        payload = {}
        for k in self._fields:
            key = k
            if with_pascal_case:
                key = k.title().replace('_', '')

            val = getattr(self, k)
            if isinstance(val, dict):
                tmp_val = {}
                for sub_k, sub_val in val.items():
                    sub_key = sub_k
                    if with_pascal_case:
                        sub_key = sub_k.title().replace('_', '')
                    tmp_val[sub_key] = sub_val
                val = tmp_val
            payload[key] = val
        return payload

    def dump(self, with_pascal_case=False):
        '''
        t = TestTuple(test_one=1, test_two=2)
        t.dump(with_pascal_case=True) -> '{"TestOne": 1, "TestTwo": 2}'
        '''
        return json.dumps(self.to_json(with_pascal_case)).encode('utf-8')
