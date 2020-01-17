import json
import os


def read_file(filepath):
    with open(filepath, 'r') as handler:
        return handler.read()


def write_json_file(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


def update_data_in_file(filename, data_for_updating):
    filepath = os.path.join(os.getcwd(), f'data/{filename}.json')
    if os.path.exists(filepath):
        # If a file exists but It's empty
        try:
            data = json.loads(filepath)
        except json.JSONDecodeError:
            data = {filename: []}
    else:
        data = {filename: []}
    
    data[filename].append(data_for_updating)
    write_json_file(filepath, data)

