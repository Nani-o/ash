from __future__ import unicode_literals
from ash.completer import AnsibleCompleter
from prompt_toolkit.document import Document

from prompt_toolkit.completion import Completion

import pytest

def get_completions(completer, text, complete_event):
    position = len(text)

    return set(completer.get_completions(Document(text=text, cursor_position=position), complete_event))

# def test_root_command_completion(completer, complete_event):
#     text = "G@"
#     result = get_completions(completer, text, complete_event)
#     assert result == set([Completion(text="G@rBag3", start_position=-2, display_meta=None)])

def test_root_command_completion_with_meta(completer, complete_event):
    text = "exi"
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
