import json


def load_file(filename):
    try:
        with open(f"app/logs/{filename}", 'r', encoding='utf-8') as fout:
            data = json.load(fout)
            return data
    except FileNotFoundError:
        print(f"File {filename} not found")
        return None