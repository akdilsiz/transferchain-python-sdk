import base64
import pickledb


class DB(object):

    def __init__(self, path):
        self.db = pickledb.load(path, auto_dump=True, sig=True)

    def set(self, key, value):
        if isinstance(value, str):
            value = value.encode('utf-8')

        self.db.set(key, base64.b64encode(value).decode())

    def get(self, key):
        return base64.b64decode(self.db.get(key))

    def get_all(self):
        items = {}
        for k in self.db.getall():
            items[k] = self.get(k)
        return items

    def dump(self):
        self.db.dump()
