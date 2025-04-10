import json

# TODO: transfer to core module
def read_json_param(json_file: str, param: str = '*'):
    jsfile = open(json_file, 'r', encoding='utf-8')
    jsettings = json.load(jsfile)
    if param == '*':
        return jsettings
    else:
        return jsettings[f'{param}']

def update_json_value(file_path: str, key: str, value):
    try:
        # Reading current data from json file
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Updating only selected key
        if key in data:
            data[key] = value
        else:
            print(f"⚠️ Key '{key}' is not found.")

        # Writing updated data into file
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"✅ Key value '{key}' is updated.")

    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"❌ Error: {e}")
