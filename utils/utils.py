import os
import json


def save_to_json(dest_path, data, filename):
    if filename[-4:] != 'json':
        filename += '.json'

    with open(os.path.join(dest_path, filename), 'w', encoding='utf-8') as f:
        for line in data:
            json.dump(line, f, ensure_ascii=False)
            f.write('\n')
