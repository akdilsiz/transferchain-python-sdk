import pickledb


class Storage(object):

    def __init__(self, path):
        self.db = pickledb.load(path, auto_dump=True, sig=True)

    def set(self, key, value):
        self.db.set(key, value)

    def get(self, key):
        return self.db.get(key)

    def dump(self):
        self.db.dump()
