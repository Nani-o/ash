from ash.ash import Ash
import pytest

@pytest.fixture
def ash():
    return Ash()

def test_get_prompt(ash):
    a = ash
    a.hosts = "localhost"
    result = a.get_prompt()
    assert result == [('ash ', 'white'), ('[localhost] ', 'cyan'), ('> ', 'white')]

def test_exec_command_target(ash):
    command = "target localhost"
    ash.exec_command(command)
    assert ash.hosts == "localhost"

def test_exec_command_target_matching(ash, capsys):
    command = "target localhust"
    ash.exec_command(command)
    out, err = capsys.readouterr()
    print out
    assert ash.hosts == None and out == "No hosts matched\n"

def test_exec_command_module(ash):
    command = "module user name=sofiane state=present"
    ash.exec_command(command)
    assert ash.method == "module" and ash.action == "user" and ash.module_args == "name=sofiane state=present"

def test_exec_command_playbook(ash):
    command = "playbook /path/to/playbook.yml"
    ash.exec_command(command)
    assert ash.method == "playbook" and ash.action == "/path/to/playbook.yml"

def test_exec_command_module(ash):
    command = "module user name=sofiane state=present"
    ash.exec_command(command)
    assert ash.method == "module" and ash.action == "user" and ash.module_args == "name=sofiane state=present"

def test_exec_command_args(ash):
    command = "args -f 5 --extra-var var=value"
    ash.exec_command(command)
    assert ash.arguments == "-f 5 --extra-var var=value"

def test_exec_command_list(ash, capsys):
    ash.hosts = "GROUP1"
    command = "list"
    ash.exec_command(command)
    out, err = capsys.readouterr()
    assert out == "host1\n"

def test_exec_command_play_module(ash, capsys):
    ash.hosts = "localhost"
    ash.method = "module"
    ash.action = "ping"
    command = "play"
    ash.exec_command(command)
    out, err = capsys.readouterr()
    assert "localhost | SUCCESS =>" in out

def test_exec_command_play_playbook(ash, playbook_file_test_project, capsys):
    ash.hosts = "localhost"
    ash.method = "playbook"
    ash.action = playbook_file_test_project
    command = "play"
    ash.exec_command(command)
    out, err = capsys.readouterr()
    print(out)
    print(err)
    assert "ok=2" in out
