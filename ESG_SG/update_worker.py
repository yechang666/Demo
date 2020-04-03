import os
import json
def store(file_name, data):
    with open(file_name, 'w') as json_file:
        json_file.write(json.dumps(data, indent=2))


def load(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)
        return data
def update_worker():




if __name__ == '__main__':


    update_worker()