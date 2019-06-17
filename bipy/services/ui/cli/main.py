"""Interface module to CLI (Console Line Interface)
    Author: Ajeet Singh
    Date: 06/16/2019
"""
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import HTML
from bipy.services.utils import Utility
from bipy.services.ui.cli import browser


class BipyCli:
    """The CLI class for BIPY. This class will capture all the inputs and delegates
        further accordingly
    """
    _warehouse_conn = None
    _repo_conn = None
    _util = None
    _config = None

    __CMD = "."
    __SUB_CMD = "."
    __INSTANCE = None
    __SESSION = None

    __MAIN_CMD_COMPLETER_LIST = [
        'BROWSE'
    ]
    __SUB_CMD_COMPLETER_LIST = [
        'CONNECT', 'SCHEMA', 'DATABASE', 'TABLE', 'VIEW',
        'MAT-VIEW', 'PROC', 'FUNC', 'PACKAGE', 'OVER'
    ]

    __MAIN_CMD_COMPLETER = WordCompleter(__MAIN_CMD_COMPLETER_LIST)
    __SUB_CMD_COMPLETER = WordCompleter(__SUB_CMD_COMPLETER_LIST)
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
        ('class:at', '>'),
        ('class:submode', '.'),
        ('class:cmdend', '>>>')
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
        self._util = Utility()
        self._config = self._util.CONFIG
        self.run()

    def run(self):
        """Run method will run endless until the command given is exit or quit
        """
        while self.__CMD is not None:
            if self.__CMD == ".":
                self.__CMD = self.__SESSION.prompt(self.__PROMPT_MODE,
                                                   auto_suggest=AutoSuggestFromHistory(),
                                                   style=self.__STYLE,
                                                   completer=self.__MAIN_CMD_COMPLETER,
                                                   bottom_toolbar=self.bottom_toolbar)
                if str(self.__CMD).lower() == "exit" or\
                        str(self.__CMD).lower() == "quit":
                    self.__CMD = None
                else:
                    self._parse_cmd(self.__CMD)
            else:
                self.__SUB_CMD = self.__SESSION\
                    .prompt(self.__PROMPT_MODE,
                            auto_suggest=AutoSuggestFromHistory(),
                            style=self.__STYLE,
                            completer=self.__SUB_CMD_COMPLETER,
                            bottom_toolbar=self.bottom_toolbar)
                if str(self.__SUB_CMD).lower() == "over":
                    self.set_prompt_mode(".")
                    self.set_sub_prompt_mode(".")
                elif str(self.__SUB_CMD).lower() == "exit" or\
                        str(self.__SUB_CMD).lower() == "quit":
                    self.__CMD = None
                else:
                    self._parse_sub_cmd(self.__SUB_CMD)

    def _parse_sub_cmd(self, raw_sub_cmd):
        """Parse sub cmd and act accordimgly
        """
        sub_cmds = str(raw_sub_cmd).split(' ')
        sub_cmd = sub_cmds[0]
        sub_cmds.remove(sub_cmd)
        sub_params = sub_cmds
        del sub_cmds
        if str(sub_cmd).upper() in self.__SUB_CMD_COMPLETER_LIST:
            self.set_sub_prompt_mode(sub_cmd)
            if self.__CMD == "BROWSE":
                if str(sub_cmd).upper() == "CONNECT":
                    self._connect(sub_params)
                elif str(sub_cmd).upper() == "SCHEMA":
                    self._list_schemas()
                elif str(sub_cmd).upper() == "HELP":
                    self._print_sub_cmd_help()
        elif sub_cmd != "":
            print("Invalid commamd provided!\
                  Please type HELP to get more information")
        else:
            self.set_prompt_mode(".")

    def _parse_cmd(self, raw_cmd):
        """ Parse the main command and act accordingly
        """
        cmds = str(raw_cmd).split(' ')
        cmd = cmds[0]
        cmds.remove(cmd)
        params = cmds
        del cmds
        if str(cmd).upper() in self.__MAIN_CMD_COMPLETER_LIST:
            self.set_prompt_mode(cmd)
            if str(cmd).upper() == "BROWSE":
                # Do nothing, wait for sub commands
                pass
            elif str(cmd).upper() == "HELP":
                self._print_cmd_help()
        elif cmd != "":
            print("Invalid command provided!\
                  Please type HELP to get more information")
        else:
            self.set_prompt_mode(".")

    def _print_cmd_help(self):
        """Print help for main commands"""
        print("Below commands are available...")
        for cmd in self.__MAIN_CMD_COMPLETER_LIST:
            print(cmd)
        print("")
        print("To get more info on a particular command, please type...")
        print("<Main Cmd> --help")

    def _print_sub_cmd_help(self):
        """Print help for sub commands"""
        print("To get more information for an sub command, please type...")
        print("<Main Cmd> HELP")
        print("")
        print("For further informatiom type...")
        print("<Main Cmd> {Sub Cmd} --help")

    def _list_schemas(self):
        schemas = browser.schemas(self._warehouse_conn)
        for schema in schemas:
            print(schema)

    def _connect(self, params):
        """Connects to either warehouse or repo based on params passed

            Args:
                params (String): The value should be WAREHOUSE OR REPO
        """
        if params.__len__() == 0:
            self._warehouse_conn = browser.connect()
        elif str(params[0]).lower() == "--help":
            print("CONNECT command usage:")
            print("CONNECT WAREHOUSE|REPO")
            print("WAREHOUSE or REPO are the only valid parameters for this command")
        else:
            print("Unknown parameter passed to CONNECT command.\
                  Type CONNECT --help to get more info")
        # self.set_prompt_mode(".")

    def bottom_toolbar(self):
        val = ("<left><b>Warehouse DB:</b>%s</left>\
               <Right><b>Repository DB:</b>%s</Right>" %
               (str(self._warehouse_conn) if self._warehouse_conn is not None else
                "{Not Connected}",
                str(self._repo_conn) if self._repo_conn is not None else
                "{Not Connected}"))
        return HTML(val)

    def set_prompt_mode(self, cmd):
        """Sets the prompt's string with value of current cmd mode

            Args:
                cmd (String): The new command that will be set
        """
        self.__CMD = cmd
        self.__PROMPT_MODE[0] = ('class:mode', str(cmd).upper())

    def set_sub_prompt_mode(self, sub_cmd):
        """Sets the prompt's sub cmd with value of current sub cmd mode
        """
        self.__SUB_CMD = "."
        self.__PROMPT_MODE[2] = ('class:submode', sub_cmd)


if __name__ == "__main__":
    b = BipyCli()
    b.run()
