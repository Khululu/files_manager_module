import os
from ..objects.files_objects import AbstractFile


def safe_new_name(suggested_name: str, file: AbstractFile):
    if os.path.exists(f'{file.catalog}\\{suggested_name}'):
        for i in range(100):
            index = suggested_name.rfind('.')
            sugo = f'{suggested_name[:index]}-{i}{suggested_name[index:]}'
            check_name = f'{file.catalog}\\{sugo}'
            if not os.path.exists(f'{check_name}'):
                break
        return sugo
    else:
        return f'{suggested_name}'
