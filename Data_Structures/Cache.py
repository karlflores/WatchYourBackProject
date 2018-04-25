from time import time
class Cache:
    def __init__(self):
        self.cache = {}
        self.keys = []
        self.time_start = time()
        self.time_accessed = self.time_start - time()

    def get(self,key):
        if key in cache:
            result = self.cache[key]
            self.keys.remove(key)
            pass


