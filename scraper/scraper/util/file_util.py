import json
def read_json_file(json_file):
    try:
        with open(json_file, 'r') as file:
            json_object = json.load(file)
            return json_object
    except Exception as e:
        print(e)
        
def overwrite_json_file(json_file, data):
    with open(json_file, "r+") as file:
        file.seek(0)  # rewind
        json.dump(data, file)
        file.truncate()

def append_json_file(json_file, data):
    existing = read_json_file(json_file)
    with open(json_file, 'w+') as outfile:
        existing.append(data)
        outfile.write(json.dumps(existing))
        outfile.close()
        
def get_json_object(obj):
    return json.dumps(obj.__dict__)