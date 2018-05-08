#!/usr/bin/env python

"""
Execution class file
"""
from subprocess import call, Popen, PIPE, STDOUT


class Execution(object):
    """Class that handle execution of ansible and ansible-playbook commands
    with parameters supplied in arguments
    """

    # def __init__(self):

    def execute_command(self, command, show=True):
        if show:
            try:
                proc = call(command)
            except KeyboardInterrupt:
                return
            return
        else:
            proc = Popen(command,
                         stdout=PIPE,
                         stderr=PIPE,
                         universal_newlines=True)
            exit_code = proc.wait()
            result = ""
            for line in proc.stdout:
                result = result + line
            return result
