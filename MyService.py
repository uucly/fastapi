import random
from typing import Optional


class MyService:
    id = random.randint(1, 100)

    def __init__(self):
        pass

    def get_infos(self, item_id, q) -> dict:
        return {"item_id": "item_id", "q": "q"}
