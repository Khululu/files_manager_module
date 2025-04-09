import json

def read_json_param(json_file: str, param: str = '*'):
    jsfile = open(json_file, 'r', encoding='utf-8')
    jsettings = json.load(jsfile)
    if param == '*':
        return jsettings
    else:
        return jsettings[f'{param}']

def update_json_value(file_path: str, key: str, value):
    try:
        # Читаем текущие данные из JSON-файла
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Обновляем только указанный ключ, если он существует
        if key in data:
            data[key] = value
        else:
            print(f"⚠️ Ключ '{key}' не найден в файле.")

        # Записываем обновленные данные обратно в файл
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"✅ Значение ключа '{key}' обновлено.")

    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"❌ Ошибка: {e}")
