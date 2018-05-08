#!/usr/bin/env python

"""
Configuration manager class file
"""

import os
import yaml
import tempfile
import textwrap

CONFIG_FILE_NAME = '.ashrc'
CONFIGS_DEF = {
    "playbook_folders": {
        "type": list,
        "description": "list of folders for playbook search completion",
        "example": """
            playbook_folders:
              - /path/to/playbooks/folder/1
              - /path/to/playbooks/folder/2
        """
    },
}


class Config(object):
    """
    Class that handles the loading of a configuration file
    """

    def __init__(self, config_file_path=None):
        if not config_file_path:
            self.config_file_path = self.get_config_path()
        else:
            self.config_file_path = config_file_path
        self.configurations = self.load_config()

    def get_config_path(self):
        home = os.path.abspath(os.environ.get('HOME', ''))
        config_file_path = os.path.join(home, CONFIG_FILE_NAME)
        return config_file_path

    def load_config(self):
        config = self.load_yaml_file(self.config_file_path)
        config = dict(
            (key, value) for (key, value) in config.items()
            if key in CONFIGS_DEF.keys()
            and isinstance(value, CONFIGS_DEF[key]["type"])
        )
        return config

    def get_variable_from_file(self, value, path):
        yaml_dict = self.load_yaml_file(path)
        if yaml_dict:
            if value in yaml_dict:
                return yaml_dict[value]
        return None

    def load_yaml_file(self, path):
        try:
            with open(path, 'r') as f:
                yaml_dict = yaml.load(f)
        except IOError as e:
            yaml_dict = {}

        return yaml_dict
