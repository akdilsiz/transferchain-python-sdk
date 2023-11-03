import base64
import pickledb


class DB(object):
    '''
    Pickledb is used as key value storage. The data stored here is encrypted.
    '''
    def __init__(self, path):
        self.db = pickledb.load(path, auto_dump=True, sig=True)

    def set(self, key, value):
        '''insert value with key'''
        if isinstance(value, str):
            value = value.encode('utf-8')

        self.db.set(key, base64.b64encode(value).decode())

    def get(self, key):
        '''Return db item'''
        return base64.b64decode(self.db.get(key))

    def get_all(self):
        '''Return all items of db'''
        items = {}
        for k in self.db.getall():
            items[k] = self.get(k)
        return items

    def dump(self):
        '''Return db dump'''
        self.db.dump()
