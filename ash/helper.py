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
        self.inventory_file = inventory_file
        self.inventory = self._get_inventory(self.inventory_file)
        if config_file:
            self.config_file = config_file
        else:
            self.config_file = constants.CONFIG_FILE

    def _get_inventory(self, inventory_path=None):
        """Use the Ansible framework to return an inventory object"""
        helper = AdHocCLI(['ansible', '--list-hosts', 'all'])
        if inventory_path:
            helper.args += ['-i', inventory_path]
        helper.parse()
        loader, inventory, vm = helper._play_prereqs(helper.options)
        return inventory
