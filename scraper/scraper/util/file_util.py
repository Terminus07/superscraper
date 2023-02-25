import json
import os
def read_json_file(json_file, errors=None):
    try:
        with open(json_file, 'r', errors=errors) as file:
            json_object = json.load(file)
            return json_object
    except Exception as e:
        print(e)
        
def create_json_file(json_file, data=None):
    try:
        print("Creating JSON file...")
        with open(json_file, "w") as file:
            if data is None:
                data = []
            json.dump(data, file)
    except Exception as e:
        print(e)
        
def overwrite_json_file(json_file, data):
    with open(json_file, "r+") as file:
        file.seek(0)  # rewind
        json.dump(data, file)
        file.truncate()

def append_json_file(json_file, data):
    existing = read_json_file(json_file)
    
    if existing is not None:
        with open(json_file, 'w+') as outfile:
            existing.append(data)
            outfile.write(json.dumps(existing))
            outfile.close()
    else:
        # create json file and dump empty object
        create_json_file(json_file)
        append_json_file(json_file, data)
        
def get_file_extension(file):
    return os.path.splitext(file)[1][1:]