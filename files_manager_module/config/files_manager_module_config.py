from importlib.resources import files

from ..base.base_services.json_services import read_json_param


class FMM_Config:
    def __init__(self):
        self.config_path = files('files_manager_module.config').joinpath('files_manager_module_config.json')
        print(self.config_path)
        self.extensions = read_json_param(self.config_path, 'extensions')
        self.defaults = read_json_param(self.config_path, 'defaults')


static_fmm_config = FMM_Config()

#print(files('files_manager_module'))
