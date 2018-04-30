from __future__ import unicode_literals
from ash.configuration import Config
import pytest

@pytest.fixture
def config(ashrc_test_file):
    return Config(ashrc_test_file)

def test_config_item_from_file(config):
    folders = ["/path/to/playbooks"]
    config_folders = config.configurations["playbook_folders"]
    assert config_folders == folders

def test_get_variable_from_file(config, ashrc_test_file):
    result = config.get_variable_from_file("test_key", ashrc_test_file)
    assert result == ["test_value"]
