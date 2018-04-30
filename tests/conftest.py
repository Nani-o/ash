import os
import pytest

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
def playbook_folder_test_project():
    return os.path.join(ansible_test_project(), "playbooks")

@pytest.fixture(scope="module")
def playbook_file_test_project():
    return os.path.join(playbook_folder_test_project(), "ping.yml")
