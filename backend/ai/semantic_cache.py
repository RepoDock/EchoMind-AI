import hashlib
import time


class SemanticCache:

    def __init__(self):

        self.cache = {}

        self.ttl = 3600


    def _key(
        self,
        question,
        file_id=None
    ):

        text = f"{file_id}:{question.lower().strip()}"

        return hashlib.md5(
            text.encode()
        ).hexdigest()


    def get(
        self,
        question,
        file_id=None
    ):

        key = self._key(
            question,
            file_id
        )

        item = self.cache.get(key)

        if item is None:
            return None

        if time.time() - item["time"] > self.ttl:

            del self.cache[key]

            return None

        return item["value"]


    def put(
        self,
        question,
        value,
        file_id=None
    ):

        key = self._key(
            question,
            file_id
        )

        self.cache[key] = {

            "time": time.time(),

            "value": value

        }