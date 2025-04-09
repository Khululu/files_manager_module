from abc import ABC
import os, json
from PIL import Image
from pillow_heif import register_heif_opener

from ..config.files_manager_module_config import static_fmm_config



class AbstractFile(ABC):
    def __init__(self, file_path: str, file_extension: str):
        super().__init__()
        self.file_path = file_path
        self.file_name = self.get_file_name()
        self.file_extension = file_extension
        self.file_size = self.get_file_size()
        self.catalog = self.get_catalog()
        self.prerenaimed = False
        self.prepaired = False
        self.site_path = ''

    ### GETTERS
    def get_catalog(self):
        index = self.file_path.rfind('\\')
        return self.file_path[:index]

    def get_file_name(self):
        index = self.file_path.rfind('\\')
        return self.file_path[index+1:]

    def get_file_size(self) -> float:
        """
        Возвращает размер файла в мегабайтах.
        :return: Размер файла в мегабайтах.
        :raises FileNotFoundError: Если файл не найден.
        """
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"Файл не найден: {self.file_path}")

        file_size_bytes = os.path.getsize(self.file_path)  # Размер файла в байтах
        file_size_mb = file_size_bytes / (1024 * 1024)  # Перевод в мегабайты
        return round(file_size_mb, 2)


class ArchiveFile(AbstractFile):
    def __init__(self, file_path, file_extension):
        super().__init__(file_path, file_extension)

    def __str__(self):
        return 'ArchiveFile'

class AudioFile(AbstractFile):
    def __init__(self, file_path, file_extension):
        super().__init__(file_path, file_extension)

    def __str__(self):
        return 'AudioFile'

class DocumentFile(AbstractFile):
    def __init__(self, file_path, file_extension):
        super().__init__(file_path, file_extension)
        self.role = ''
        self.number = ''
        self.date_accepted = ''
        self.tltle = ''
        self.fullname = ''
        self.publicate_to = []
        # НПА? дата, номер, тайтл, разделы

    def __str__(self):
        return 'DocumentFile'

class ImageFile(AbstractFile):
    def __init__(self, file_path, file_extension):
        super().__init__(file_path, file_extension)
        register_heif_opener()
        # валидность расширения
        self.verify_image()
        #self.need_convertation = False

    def __str__(self):
        return 'ImageFile'

    def resize(self):
        pass

    def verify_image(self) -> dict:
        """
        Проверяет, является ли файл изображением, используя библиотеку Pillow.
        Поддерживаются расширения:
            png, jpg, jpeg, webp, bmp, gif, jfif, tiff, heic
        Непроверенные расширения:
            tif
        :param file_path: Путь к файлу.
        :return: True, если расширение указано верно, иначе False.
        :return: None, если файл не является изображением или расширениене поддерживается.
        """
        classify_images = {
                    'jpeg': ['jpg', 'jpeg', 'jfif', 'mpo'],
                    'png': ['png'],
                    'webp': ['webp'],
                    'bmp': ['bmp'],
                    'gif': ['gif'],
                    'tiff': ['tiff'],
                    'heif': ['heic', 'heif'],
                    'mpo': ['jpg', 'jpeg', 'jfif', 'mpo']
                }
        supported_extensions = ['jpg', 'jpeg', 'jfif', 'png', 'webp', 'bmp', 'gif', 'tiff', 'heic', 'heif']
        if self.file_extension in supported_extensions:
            try:
                with Image.open(self.file_path) as img:
                    img.verify()  # Проверяет целостность изображения
                    extension = img.format
                    if extension == None:
                        self.valid = False
                    else:
                        extension = extension.lower()
                        self.valid = True
                        if self.file_extension in classify_images[extension]:
                            self.valid_extension = True
                            self.need_convertation = True
                        else:
                            self.valid_extension = False
                            self.need_convertation = True
                            self.correct_extension = extension
                        if self.file_extension in ['jpg', 'jpeg'] and self.valid_extension:
                            self.need_convertation = False

            except Exception as e:
                message(f"Файл {self.file_path} не является изображением: {e}")
                self.valid = False
        else:
            self.valid = False


class ScriptFile(AbstractFile):
    def __init__(self, file_path, file_extension):
        super().__init__(file_path, file_extension)

    def __str__(self):
        return 'ScriptFile'

class VideoFile(AbstractFile):
    def __init__(self, file_path, file_extension):
        super().__init__(file_path, file_extension)

    def __str__(self):
        return 'VideoFile'

def fileFactory(file_path: str):
    ### ИСПРАВИТЬ ПУТЬ К data.json
    extensions = static_fmm_config.extensions

    index = file_path.rfind('.')
    extension = file_path[index+1:].lower()
    if os.path.isfile(file_path):
        match extension:
            case _ if extension in extensions['archives']:
                return ArchiveFile(file_path, extension)
            case _ if extension in extensions['audios']:
                return AudioFile(file_path, extension)
            case _ if extension in extensions['documents']:
                return DocumentFile(file_path, extension)
            case _ if extension in extensions['images']:
                return ImageFile(file_path, extension)
            case _ if extension in extensions['scripts']:
                return ScriptFile(file_path, extension)
            case _ if extension in extensions['videos']:
                return VideoFile(file_path, extension)
    return None
