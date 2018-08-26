#!/usr/bin/env python

"""
Cli class file
"""
from __future__ import unicode_literals

from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText

from os.path import expanduser
import sys


class Cli(object):
    """Class that handles the different interactions with user such as
    prompting user or show completions
    """

    def __init__(self, prompt_text, completer):
        self.prompt = prompt_text
        self.completer = completer
        history_file_path = expanduser("~/.ash_history")
        self.history = FileHistory(history_file_path)
        self.session = PromptSession(history=self.history)
        self.colors = {
            # Default
            '':       '#ffffff',
            # Defined colors
            'white':  '#ffffff',
            'cyan':   '#00ffff',
            'yellow': '#ffff00',
            'red':    '#ff0000',
            'green':  '#00ff00',
        }
        self.style = Style.from_dict(self.colors)

    def get_prompt_fragments(self):
        result = []
        for segment, color in self.prompt:
            result.append(('class:' + color, segment.decode('utf-8')))
        return result

    def show_message(self, message, message_color):
        text = FormattedText([('class:' + message_color, message.decode('utf-8'))])
        print_formatted_text(text, style=self.style)

    def show_prompt(self):
        while True:
            try:
                prompt_fragments = self.get_prompt_fragments()
                text = self.session.prompt(
                    prompt_fragments,
                    style=self.style,
                    completer=self.completer,
                    auto_suggest=AutoSuggestFromHistory()
                )
                return text
            except EOFError:
                self.exit()
            except KeyboardInterrupt:
                continue

    def exit(self):
        print("GoodBye !!")
        sys.exit(0)
