from ash.execution import Execution
import pytest

@pytest.fixture
def execution():
    return Execution()

def test_execution_command(execution):
    command = ["echo", "-n", "test_command"]
    result = execution.execute_command(command, False)
    assert result == "test_command"

def test_execution_ansible_module(execution, capfd):
    command = ["ansible", "-m", "ping", "localhost"]
    execution.execute_command(command)
    out, err = capfd.readouterr()
    assert "localhost | SUCCESS =>" in out

def test_execution_ansible_playbook(execution, playbook_file_test_project, capfd):
    command = ["ansible-playbook", playbook_file_test_project]
    execution.execute_command(command)
    out, err = capfd.readouterr()
    assert "ok=1" in out
