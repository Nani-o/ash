#!/usr/bin/env python
"""
Autocompletion example that displays the autocompletions like readline does by
binding a custom handler to the Tab key.
"""

from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.completion import Completer, Completion

import re
import json
import os
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from ansible.plugins.loader import module_loader, fragment_loader
from ansible.utils import plugin_docs
from ansible import constants as C


class AnsibleCompleter(Completer):
    def __init__(self, inventory, root_commands,
                 list_commands, config_definitions, config):
        self.inventory = inventory
        self.root_commands = root_commands
        self.list_commands = list_commands
        self.config_definitions = config_definitions
        self.config = config

        self.hosts = [x.name for x in self.inventory.list_hosts()]
        self.groups = self.inventory.list_groups()

        self.modules = self.list_modules()

    def get_module_meta(self, module):
        in_path = module_loader.find_plugin(module)

        if in_path and not in_path.endswith('.ps1'):
            module_vars, a, _, _ = plugin_docs.get_docstring(in_path, fragment_loader)
        else:
            module_vars = None
        return module_vars

    def list_modules(self):
        modules = set()

        module_paths = module_loader._get_paths()
        for path in module_paths:
            if path is not None:
                modules.update(self._find_modules_in_path(path))

        return modules

    def _find_modules_in_path(self, path):
        if os.path.isdir(path):
            for module in os.listdir(path):
                if module.startswith('.'):
                    continue
                elif os.path.isdir(module):
                    self._find_modules_in_path(module)
                elif module.startswith('__'):
                    continue
                elif any(module.endswith(x) for x in C.BLACKLIST_EXTS):
                    continue
                elif module in C.IGNORE_FILES:
                    continue
                elif module.startswith('_'):
                    fullpath = '/'.join([path, module])
                    if os.path.islink(fullpath):  # avoids aliases
                        continue
                    module = module.replace('_', '', 1)

                module = os.path.splitext(module)[0]  # removes the extension
                yield module

    def _module_completion(self):
        """Retrieve module names and args for the module command completion"""
        if len(self.word_list) >= 3:
            module = self.word_list[1]
            meta = self.get_module_meta(module)
            if meta:
                options = meta['options']
                matched_options = self._match_input(self.cur_word, options)
                self.completions = [x + "=" for x in matched_options]
        else:
            self.completions = self._match_input(self.cur_word, self.modules)

    def _playbook_completion(self):
        """Retrieve file paths for the playbook command completion"""
        files_list = []
        exclude_folders = [
            "group_vars",
            "host_vars",
            "roles"
        ]
        for folder in self.config.configurations["playbook_folders"]:
            if os.path.isdir(folder):
                for root, dirs, files in os.walk(folder):
                    if os.path.basename(root) not in exclude_folders:
                        files_list += [
                            os.path.join(root, file)
                            for file in files
                            if (
                                file.endswith(".yml")
                                or file.endswith(".yaml")
                            )
                            and (self.cur_word in os.path.join(root, file))
                        ]
        self.completions = files_list

    def _target_completion(self):
        """Retrieve informations from the inventory for target completion"""
        pattern = r'([&|!|^]*)([^:!&]*)([:]*)'
        matches = re.findall(pattern, self.cur_word)
    
        if matches[len(matches)-2][2] == ':':
            real_cur_word = ''
        else:
            real_cur_word = matches[len(matches)-2][1]
    
        string_before_cur_word = ''.join([
            ''.join(x) for x
            in matches
            if x[2] == ':'
        ])
    
        if matches[len(matches)-2][2] != ':':
            string_before_cur_word += matches[len(matches)-2][0]
    
        self.completions = [
            string_before_cur_word + x for x
            in self.hosts + self.groups
            if x.startswith(real_cur_word)
            and x not in [
                y[1] for y
                in matches
            ]
        ]

    def _list_completion(self):
        """Retrieve elements for the list command completion"""
        self.completions = OrderedDict(
            (key, value) for key, value
            in self.list_commands.iteritems()
            if key.startswith(self.cur_word)
        )
        update = OrderedDict(
            (x, "A group from inventory") for x
            in self.groups
            if x.startswith(self.cur_word)
        )
        self.completions.update(update)

    def _set_completion(self):
        """Retrieve configuration variables for the set command completion"""
        self.completions = OrderedDict(
            (key, value["description"]) for key, value
            in self.config_definitions.iteritems()
            if key.startswith(self.cur_word)
        )

    def _match_input(self, input, struct):
        if isinstance(struct, dict):
            result = OrderedDict(
                (key, value) for key, value
                in struct.iteritems()
                if key.startswith(input))
        elif isinstance(struct, list) or isinstance(struct, set):
            result = [x for x in struct if x.startswith(input)]
        return result

    def get_completions(self, document, complete_event):
        self.cur_text = document.text_before_cursor
        self.cur_word = document.get_word_before_cursor(WORD=True)
        self.word_list = self.cur_text.split(' ')
        complete_playbook = "playbook_folders" in self.config.configurations
        self.completions = []

        if len(self.word_list) == 1:
            self.completions = self._match_input(self.cur_word, self.root_commands)
        else:
            if self.word_list[0] == "module":
                self._module_completion()
            elif self.word_list[0] == "playbook" and complete_playbook:
                self._playbook_completion()
            elif len(self.word_list) == 2:
                if self.word_list[0] == "target":
                    self._target_completion()
                elif self.word_list[0] == "list":
                    self._list_completion()
                elif self.word_list[0] == "set":
                    self._set_completion()

        if isinstance(self.completions, list):
            self.completions.sort()

        for word in self.completions:
            if isinstance(self.completions, dict):
                meta = self.completions[word].decode('utf-8')
            else:
                meta = None

            yield Completion(word.decode('utf-8'), -len(self.cur_word), display_meta=meta)
