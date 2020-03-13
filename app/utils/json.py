import json
from typing import Union


def get_json(path: str) -> Union[dict, list]:
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)
