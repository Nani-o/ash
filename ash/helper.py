#!/usr/bin/env python
"""
AnsibleHelper class file

"""

from ansible import constants
from ansible.cli.adhoc import AdHocCLI


class AnsibleHelper(object):
    """
    This class is aimed to manage all ansible related side of this program
    """

    def __init__(self, inventory_file=None, config_file=None):
        self._set_inventory(inventory_file)
        if config_file:
            self.config_file = config_file
        else:
            self.config_file = constants.CONFIG_FILE

    def _set_inventory(self, inventory_path=None):
        """Use the Ansible framework to return an inventory object"""
        helper = AdHocCLI(['ansible', '--list-hosts', 'all'])
        if inventory_path:
            helper.args += ['-i', inventory_path]
        helper.parse()
        loader, inventory, vm = helper._play_prereqs(helper.options)
        self.inventory_file = inventory_path
        self.inventory = inventory


class AnsibleCommand(object):
    """
    This class is aimed to represent an ansible command for execution and display
    """

    def __init__(
	self, type, action, hosts=None, module_args=None,
	forks=None, extra_vars=None, extra_args=None
    ):
	self.type = type
        self.action = action

        self.hosts = hosts
        self.module_args = module_args
        self.forks = forks
        self.extra_vars = extra_vars
        self.extra_args = extra_args

        self.COMMAND_TYPES = ['module', 'playbook']

        self._generate()

    def _generate(self):
	if self.type not in self.COMMAND_TYPES:
            print("Type not supported")

	if self.type == 'module':
            if not self.hosts:
                print("Target missing for adhoc command")
            else:
                self._generate_adhoc_command()
	elif self.type == 'playbook':
            self._generate_playbook_command()
        self._to_printable_command()

    def _generate_adhoc_command(self):
        """Use parameters to generate an Ansible adhoc command"""
        self.executable_command = ["ansible", "-m", self.action]
        if self.module_args:
            self.executable_command.append("-a")
            self.executable_command.append(self.module_args)
        self._generate_common_part()
        self.executable_command.append(self.hosts)

    def _generate_playbook_command(self):
        """Use parameters to generate an Ansible playbook command"""
        self.executable_command = ["ansible-playbook"] + self.action
        self._generate_common_part()
        if self.hosts:
            self.executable_command.append("-l")
            self.executable_command.append(self.hosts)

    def _generate_common_part(self, **kwargs):
        """Return the command part not specific to adhoc or playbook"""
        if self.forks:
            self.executable_command.append("-f")
            self.executable_command.append(self.forks)
        if self.extra_vars:
            self.executable_command.append("--extra-vars")
            self.executable_command.append(self.extra_vars)
        if self.extra_args:
            self.executable_command += self.extra_args

    def _to_printable_command(self):
        """Return the command to run in a shell with current parameters"""
        result = []
        for segment in self.executable_command:
            if ' ' in segment:
                escaped_segment = '"{}"'.format(segment.replace('"', '\\"'))
                result.append(escaped_segment)
            else:
                result.append(segment)
        self.printable_command = ' '.join(result)
