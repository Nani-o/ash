from __future__ import unicode_literals
from ash.completer import AnsibleCompleter
from ash.ash import Ash, ROOT_COMMANDS, LIST_COMMANDS
from ash.configuration import Config, CONFIGS_DEF
from prompt_toolkit.document import Document

from prompt_toolkit.completion import Completion

import pytest

@pytest.fixture
def completer():
    return AnsibleCompleter(inventory=Ash._get_inventory(),
        root_commands=ROOT_COMMANDS,
        list_commands=LIST_COMMANDS,
        config_definitions=CONFIGS_DEF,
        config=Config())

@pytest.fixture
def complete_event():
    from mock import Mock
    return Mock()

def get_completions(completer, text, complete_event):
    position = len(text)

    return set(completer.get_completions(Document(text=text, cursor_position=position), complete_event))

# def test_root_command_completion(completer, complete_event):
#     text = "G@"
#     result = get_completions(completer, text, complete_event)
#     assert result == set([Completion(text="G@rBag3", start_position=-2, display_meta=None)])

def test_root_command_completion_with_meta(completer, complete_event):
    text = "ex"
    result = get_completions(completer, text, complete_event)
    assert set((x.text, x.display_meta) for x in result) == set([('exit', 'Quit program')])

def test_list_command_completion(completer, complete_event):
    text = "list tar"
    result = get_completions(completer, text, complete_event)
    assert set(x.text for x in result) == set(['target'])

def test_module_command_completion(completer, complete_event):
    text = "module us"
    result = get_completions(completer, text, complete_event)
    assert set(x.text for x in result) == set(['user'])

def test_module_args_command_completion(completer, complete_event):
    text = "module user na"
    result = get_completions(completer, text, complete_event)
    assert set(x.text for x in result) == set(['name='])

# def test_playbook_command_completion(completer, complete_event):
#     text = "playbook pin"
#     result = get_completions(completer, text, complete_event)
#     assert set(x.text for x in result) == set(['target'])

def test_set_command_completion(completer, complete_event):
    text = "set playbook_fo"
    result = get_completions(completer, text, complete_event)
    assert set(x.text for x in result) == set(['playbook_folders'])

def test_target_command_completion(completer, complete_event):
    text = "target local"
    result = get_completions(completer, text, complete_event)
    assert set(x.text for x in result) == set(['localhost'])


# ROOT_COMMANDS = OrderedDict([
#     ('list', 'List hosts targeted/in group/in inventory'),
#     ('module', 'Choose a module to use'),
#     ('play', 'Execute playbook or module on target'),
#     ('playbook', 'Choose a playbook to use'),
#     ('set', 'Set configurations in-memory'),
#     ('reset', 'Remove all arguments set'),
#     ('shellmode', 'Enter shell commands directly on target'),
#     ('target', 'Target an Ansible host or group')
# ])

# LIST_COMMANDS = OrderedDict([
#     ('hosts', 'List all hosts from inventory'),
#     ('groups', 'List all groups from inventory'),
#     ('target', 'List all targeted hosts'),
#     ('tasks', 'List all tasks that would be executed'),
#     ('tags', 'List all tags of a playbooks')
# ])
