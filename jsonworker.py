import json


def read_json(json_path: str):
    # Открываем JSON-файл для чтения
    with open(json_path, 'r') as json_file:
        # Используем функцию json.load() для загрузки данных из файла
        data = json.load(json_file)
    return data
