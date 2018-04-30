#!/usr/bin/env python

"""
Cli class file
"""

from prompt_toolkit import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from prompt_toolkit.shortcuts import print_tokens
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from os.path import expanduser
import sys

class Cli(object):
    """
    Class that handles the different interactions with user such as prompting user or show completions
    """

    def __init__(self, prompt_text, completer):
        self.prompt = prompt_text
        self.style = style_from_dict({
            # User input.
            Token:          '#ffffff',
            # Colors
            Token.White:    '#ffffff',
            Token.Cyan:     '#00ffff',
            Token.Yellow:   '#ffff00',
            Token.Red:      '#ff0000'
        })
        self.completer = completer
        history_file_path = expanduser("~/.ash_history")
        self.history = FileHistory(history_file_path)

    def get_prompt_tokens(self, cli):
        result = []
        for segment, color in self.prompt:
            if color == "white":
                result.append((Token.White, segment))
            elif color == "cyan":
                result.append((Token.Cyan, segment))
            elif color == "yellow":
                result.append((Token.Yellow, segment))
            elif color == "red":
                result.append((Token.Red, segment))

        return result

    def show_message(self, message, message_color):
        tokens = []
        if message_color == "red":
            tokens.append((Token.Red, message))
            tokens.append((Token.White, '\n'))
        else:
            print("This color does not exist")
            return

        print_tokens(tokens, style=self.style)

    def show_prompt(self):
        while True:
            try:
                text = prompt(get_prompt_tokens=self.get_prompt_tokens, style=self.style, completer=self.completer, history=self.history, auto_suggest=AutoSuggestFromHistory())
                return text
            except EOFError:
                self.exit()
            except KeyboardInterrupt:
                continue

    def exit(self):
        print("GoodBye !!")
        sys.exit(0)
