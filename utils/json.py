import json


class JsonUtils:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_json(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def write_json(self, data, indent=4, ensure_ascii=None, sort_keys=None):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data_json = json.load(file)
        with open(self.file_path, 'w', encoding='utf-8') as file:
            data_json.update(data)
            json.dump(data_json, file, indent=indent, sort_keys=sort_keys, ensure_ascii=ensure_ascii)

    def write_json_unsafe(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


class JsonWrite(JsonUtils):
    def first_write(self, id: str, time=10800, sort="Время", display='Фото'):
        data = {id: {"time": time, "sort": sort, "display": display}}
        self.write_json(data=data, indent=4)

    def get_member(self, key):
        return self.get_json().get(key)