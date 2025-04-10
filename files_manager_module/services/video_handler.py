import subprocess, os, time

from ..objects.files_objects import VideoFile
from .renamer import safe_new_name
from ....core_module.core_module.message_handler import message

#config = user_config


def video_convertation(video: VideoFile, ffmpeg_path: str, target_extension: str = 'mp4', LARGE_VIDEO_CONVERTATION: bool = False):
    if os.path.exists(f'{ffmpeg_path}.exe'):
        if type(video) == VideoFile:
            print(video.file_path)
            if video.file_extension != target_extension:
                if video.file_size < 100 or LARGE_VIDEO_CONVERTATION:
                    try:
                        new_file_name = safe_new_name(video.file_name.lower().replace(video.file_extension, target_extension), video)
                        new_file_path = f'{video.catalog}\\{new_file_name}'
                        subprocess.call(f'{ffmpeg_path} -i {video.file_path} {new_file_path}')
                        os.remove(f'{video.file_path}')
                        video.file_name = new_file_name
                        video.file_path = new_file_path
                        video.file_extension = target_extension
                    except FileNotFoundError:
                        message('incorrect file path')
    else:
        message('ffmpeg is not installed')

def create_video_thumbnail(video: VideoFile, ffmpeg_path: str):
    if str(video) == 'VideoFile':
        print(1)
        try:
            print('v')
            for i in range(3):
                thumbnail_name = f'{video.catalog}\\{video.file_name.replace(f".{video.file_extension}", '')}_thumpnail_{i+1}.jpg'
                subprocess.call(f'{ffmpeg_path} -i {video.file_path} -ss 00:00:0{i+1} -frames:v 1 -q:v 2 {thumbnail_name}')
        except FileNotFoundError:
            message('incorrect file path')
