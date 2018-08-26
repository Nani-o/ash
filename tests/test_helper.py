from ash.helper import AnsibleHelper
from ash.helper import AnsibleCommand
import pytest

def test_get_inventory(ansible_inventory_test_file):
    ansible_helper = AnsibleHelper()
    ansible_helper._set_inventory(ansible_inventory_test_file)
    result = ansible_helper.inventory.list_hosts("host1")
    assert 'host1' in [x.name for x in result]

testdata = [
    ("playbook", ["ping.yml"], "localhost", "10", None, ["-s"],
     ['ansible-playbook', 'ping.yml', '-f', '10', '-s', '-l', 'localhost'],
     'ansible-playbook ping.yml -f 10 -s -l localhost'),
    ("module", "ping", "localhost", None, "toto=True", None,
     ['ansible', '-m', 'ping', '--extra-vars', 'toto=True', 'localhost'],
     'ansible -m ping --extra-vars toto=True localhost')
]

@pytest.mark.parametrize("type,action,hosts,forks,extra_vars,extra_args,expected_executable,expected_printable", testdata)
def test_ansible_command(type, action, hosts, forks, extra_vars, extra_args, expected_executable, expected_printable):
    ansible_command = AnsibleCommand(type=type, action=action, hosts=hosts, forks=forks, extra_vars=extra_vars, extra_args=extra_args)
    assert ansible_command.executable_command == expected_executable
    assert ansible_command.printable_command == expected_printable
