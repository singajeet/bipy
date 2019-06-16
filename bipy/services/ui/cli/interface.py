"""Interface module to CLI (Console Line Interface)
    Author: Ajeet Singh
    Date: 06/16/2019
"""
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter


class BipyCli:
    """The CLI class for BIPY. This class will capture all the inputs and delegates further
        accordingly
    """
    __CMD = "START"
    __INSTANCE = None
    __SESSION = None
    __MAIN_CMD_COMPLETER_LIST = [
        'CONNECT', 'LIST', 'CREATE', 'DELETE', 'SAVE', 'QUIT', 'EXIT',
        'ADD', 'REMOVE', 'UPDATE', 'DISCONNECT', 'CLOSE', 'HELP'
    ]
    __MAIN_CMD_COMPLETER = WordCompleter(__MAIN_CMD_COMPLETER_LIST)
    __SUB_CMD_COMPLETER =   WordCompleter([
        'WAREHOUSE', 'META-REPO','SCHEMA', 'DATABASE', 'TABLE', 'VIEW',
        'MAT-VIEW', 'PROC', 'FUNC', 'PACKAGE'
    ])
    __STYLE = Style.from_dict({
        # User input (default text).
        '':          '#ff0066',

        # Prompt.
        'cmdend': '#884444',
        'at':       '#00aa00',
        'modelbl':    '#884444',
        'mode':     'ansicyan underline',
    })

    __PROMPT_MODE = [
        ('class:mode', '.'),
        ('class:at', '@'),
        ('class:modelbl', 'Mode'),
        ('class:cmdend', '>')
    ]

    def __new__(cls):
        """Singleton class
        """
        if BipyCli.__INSTANCE is None:
            BipyCli.__INSTANCE = object.__new__(cls)
        return BipyCli.__INSTANCE

    def __init__(self):
        """Default constructor
        """
        self.__SESSION = PromptSession()
        self.run()

    def run(self):
        """Run method will run endless until the command given is exit or quit
        """
        while self.__CMD is not None:
            self.__CMD = self.__SESSION.prompt(self.__PROMPT_MODE,
                                               auto_suggest=AutoSuggestFromHistory(),
                                               style=self.__STYLE,
                                               completer=self.__MAIN_CMD_COMPLETER)
            if str(self.__CMD).lower() == "exit" or str(self.__CMD).lower() == "quit":
                self.__CMD = None
            else:
                if str(self.__CMD).upper() in self.__MAIN_CMD_COMPLETER_LIST:
                    self.__PROMPT_MODE[0] = ('class:mode', str(self.__CMD).upper())
                else:
                    raise Exception("Invalid command provided, please type HELP to get more information")



if __name__ == "__main__":
    b = BipyCli()
    b.run()
