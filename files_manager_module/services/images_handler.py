import os
from PIL import Image, ExifTags

from ..objects.files_objects import ImageFile
from cm_tools_remake.config.user_config import user_config
from .renamer import safe_new_name
from cm_tools_remake.services.message_handler import message
from ..config.files_manager_module_config import static_fmm_config


#config = user_config


def convert_to_jpg(image: ImageFile):
    if str(image) == 'ImageFile':
        if image.need_convertation and image.valid:
            if image.file_extension in static_fmm_config.extensions['images']:
                new_file_name = safe_new_name(image.file_name.lower().replace(f'.{image.file_extension}', '-conv.jpg'), image)
                new_file_path = f'{image.catalog}\\{new_file_name}'
                rgb_conv = ['png', 'tiff', 'heic', 'tif']
                same_conv = ['bpm', 'jfif', 'webp', 'bmp']
                img = Image.open(f'{image.file_path}')
                exif = img.getexif()
                if exif:
                    orientation_key = next((k for k, v in ExifTags.TAGS.items() if v == 'Orientation'), None)
                    if orientation_key and orientation_key in exif:
                        orientation = exif[orientation_key]
                        if orientation == 3:
                            img = img.rotate(180, expand=True)
                        elif orientation == 6:
                            img = img.rotate(270, expand=True)
                        elif orientation == 8:
                            img = img.rotate(90, expand=True)
                if image.file_extension in rgb_conv:
                    rgb_img = img.convert('RGB')
                    out_img = rgb_img
                    out_img.save(f'{new_file_path}')
                    os.remove(f'{image.file_path}')
                elif image.file_extension in same_conv:
                    out_img = img
                    out_img.save(f'{new_file_path}')
                    os.remove(f'{image.file_path}')
                image.file_extension = 'jpg'
                image.file_path = new_file_path
                image.file_name = new_file_name
                image.need_convertation = False
    else:
        message(f'file {image} is not image')


def cutter(image: ImageFile):
    if type(image) == ImageFile:
        if image.file_size >= 1:
            img = Image.open(image.file_path)
            exif = img.getexif()
            if exif:
                orientation_key = next((k for k, v in ExifTags.TAGS.items() if v == 'Orientation'), None)
                if orientation_key and orientation_key in exif:
                    orientation = exif[orientation_key]
                    if orientation == 3:
                        img = img.rotate(180, expand=True)
                    elif orientation == 6:
                        img = img.rotate(270, expand=True)
                    elif orientation == 8:
                        img = img.rotate(90, expand=True)
            ns = img.size[0] / 720
            hs = int(img.size[1] / ns)
            sizes = (720, hs)
            img.thumbnail(sizes)

            new_file_name = safe_new_name(image.file_name.lower().replace(f'.{image.file_extension}', f'-thmb.{image.file_extension}'), image)
            new_file_path = f'{image.catalog}\\{new_file_name}'
            img.save(new_file_path)
            os.remove(f'{image.file_path}')
            image.file_path = new_file_path
            image.file_name = new_file_name

def fix_extension(file: ImageFile):
    if file.valid == True and file.valid_extension == False:
        new_file_name = safe_new_name(f'{file.file_name}'.replace(file.file_extension, file.correct_extension), file)
        new_file_path = f'{file.catalog}\\{new_file_name}'
        os.rename(file.file_path, new_file_path)
        file.file_path = new_file_path
        file.file_name = new_file_name
        file.valid_extension = True
        file.file_extension = file.correct_extension
