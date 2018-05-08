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
    """Class that handles the different interactions with user such as
    prompting user or show completions
    """

    def __init__(self, prompt_text, completer):
        self.prompt = prompt_text
        self.completer = completer
        history_file_path = expanduser("~/.ash_history")
        self.history = FileHistory(history_file_path)
        self.tokens = {
            "white": {
                "token": Token.White,
                "hex":   '#ffffff'
            },
            "cyan": {
                "token": Token.Cyan,
                "hex":   '#00ffff'
            },
            "yellow": {
                "token": Token.Yellow,
                "hex":   '#ffff00'
            },
            "red": {
                "token": Token.Red,
                "hex":   '#ff0000'
            },
            "green": {
                "token": Token.Green,
                "hex":   '#00ff00'
            }
        }
        # Getting a dict like {Token: hexcode} for style_from_dict
        style_dict = {
            value["token"]: value["hex"]
            for (key, value)
            in self.tokens.iteritems()
        }
        # Adding color for user input
        style_dict[Token] = '#ffffff'
        # Converting to prompt_toolkit style
        self.style = style_from_dict(style_dict)

    def color_to_token(self, color):
        if color in self.tokens.keys():
            return self.tokens[color]["token"]
        return Token

    def get_prompt_tokens(self, cli):
        result = []
        for segment, color in self.prompt:
            result.append((self.color_to_token(color), segment))
        return result

    def show_message(self, message, message_color):
        result = []
        result.append((self.color_to_token(message_color), message))
        result.append((Token.White, '\n'))
        print_tokens(result, style=self.style)

    def show_prompt(self):
        while True:
            try:
                text = prompt(
                    get_prompt_tokens=self.get_prompt_tokens,
                    style=self.style,
                    completer=self.completer,
                    history=self.history,
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
