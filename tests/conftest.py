import os
import pytest

from ash.ash import Ash, ROOT_COMMANDS, LIST_COMMANDS
from ash.configuration import Config, CONFIGS_DEF
from ash.completer import AnsibleCompleter
from ash.helper import AnsibleHelper

@pytest.fixture(scope="module")
def script_path():
    return os.path.realpath(__file__)

@pytest.fixture(scope="module")
def script_folder():
    return os.path.dirname(script_path())

@pytest.fixture(scope="module")
def ansible_test_project():
    return os.path.join(script_folder(), "ansible-test-project")

@pytest.fixture(scope="module")
def ashrc_test_file():
    return os.path.join(ansible_test_project(), "ashrc")

@pytest.fixture(scope="module")
def ansible_inventory_test_file():
    return os.path.join(ansible_test_project(), "hosts")

@pytest.fixture(scope="module")
def playbook_folder_test_project():
    return os.path.join(ansible_test_project(), "playbooks")

@pytest.fixture(scope="module")
def playbook_file_test_project():
    return os.path.join(playbook_folder_test_project(), "ping.yml")

@pytest.fixture(scope="module")
def config(ashrc_test_file):
    return Config(ashrc_test_file)

@pytest.fixture(scope="module")
def ash():
    return Ash()

@pytest.fixture
def helper():
    return AnsibleHelper()

@pytest.fixture
def inventory(helper, ansible_inventory_test_file):
    helper._set_inventory(ansible_inventory_test_file)
    return helper.inventory

@pytest.fixture
def completer(inventory, config):
    return AnsibleCompleter(inventory=inventory,
        root_commands=ROOT_COMMANDS,
        list_commands=LIST_COMMANDS,
        config_definitions=CONFIGS_DEF,
        config=config)

@pytest.fixture(scope="module")
def complete_event():
    from mock import Mock
    return Mock()
