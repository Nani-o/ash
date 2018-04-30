#!/usr/bin/env python

"""
Execution class file
"""
import sys
import shutil
from subprocess import Popen, PIPE, STDOUT
import subprocess

import ansible.constants as C
from ansible.cli.playbook import PlaybookCLI
from ansible.cli.adhoc import AdHocCLI

class Execution(object):
    """
    Class that handle execution of ansible and ansible-playbook commands with parameters
    supplied in arguments
    """

    # def __init__(self):

    def execute_command(self, command, output_to_stdout=True, show_command_running=True):
        if show_command_running:
            print("Executing : " + ' '.join(command))
        if output_to_stdout:
            try:
                proc = subprocess.call(command)
            except KeyboardInterrupt:
                return
            return
        else:
            proc = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            exit_code = proc.wait()
            result = ""
            for line in proc.stdout:
                result = result + line
            return result

    def execute_ansible(self, method, action=None, module_args=None,host=None, args=None):
        command = []
        if method == "playbook":
            command.append("ansible-playbook")
            command.append(action)
            if args:
                command += args.split(' ')
            command.append('-l')
            command.append(host)
            mycli = PlaybookCLI(command)
        elif method == "module":
            command.append("ansible")
            command.append("-m")
            command.append(action)
            if module_args:
                command.append("-a")
                command.append(module_args)
            if args:
                command += args.split(' ')
            command.append(host)
            mycli = AdHocCLI(command)
        print("Command : " + ' '.join(command))
        try:
            mycli.parse()
            mycli.run()
        finally:
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
