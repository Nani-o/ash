from ash.execution import Execution
import pytest

@pytest.fixture
def execution():
    return Execution()

def test_execution_command(execution):
    command = ["echo", "-n", "test_command"]
    result = execution.execute_command(command, output_to_stdout=False, show_command_running=False)
    assert result == "test_command"

def test_execution_ansible_module(execution, capsys):
    execution.execute_ansible(method="module",
        action="ping",
        host="localhost")
    out, err = capsys.readouterr()
    assert "localhost | SUCCESS =>" in out

def test_execution_ansible_playbook(execution, playbook_file_test_project, capsys):
    execution.execute_ansible(method="playbook",
        action=playbook_file_test_project,
        host="localhost")
    out, err = capsys.readouterr()
    assert "ok=2" in out
