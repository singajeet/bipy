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
from bipy.services.ui.cli import help
from bipy.services.ui.cli.browser_sub_cmds import BrowserSubCmds


class BipyCli:
    """The CLI class for BIPY. This class will capture all the inputs and delegates
        further accordingly
    """
    _warehouse_conn = None
    _repo_conn = None
    _util = None
    _config = None
    _sub_commands = None

    __CMD = "."
    __SUB_CMD = "."
    __INSTANCE = None
    __SESSION = None

    __COMPLETER_DICT_LIST = {
        'BROWSE': ['CONNECT', 'SCHEMAS', 'DATABASES', 'TABLES', 'VIEWS',
                   'MAT-VIEWS', 'PROCS', 'FUNCS', 'PACKAGES', 'DONE', 'HELP',
                   'EXIT', 'QUIT', 'VIEW-DEF', 'COLUMNS', 'COLUMN-NAMES',
                   'COLUMN-TYPE', 'PK-COLUMNS', 'PK-NAME', 'TABLE-OPTS',
                   'FK-COLUMNS', 'CLOSE', 'DISCONNECT'
                   ],
        'HELP': [],
        'EXIT': [],
        'QUIT': []
    }

    __MAIN_CMD_COMPLETER_LIST = list(__COMPLETER_DICT_LIST.keys())
    __SUB_CMD_COMPLETER_LIST = __COMPLETER_DICT_LIST['BROWSE']

    __MAIN_CMD_COMPLETER = WordCompleter(list(__COMPLETER_DICT_LIST.keys()), ignore_case=True)
    __SUB_CMD_COMPLETER = WordCompleter(__COMPLETER_DICT_LIST['BROWSE'], ignore_case=True)
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
        ('class:at', '#'),
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
        self._sub_commands = BrowserSubCmds()
        self.run()

    def run(self):
        """Run method will run endless until the command given is exit or quit
        """
        while self.__CMD is not None:
            if self.__CMD == ".":
                self.__CMD = self.__SESSION.prompt(self.__PROMPT_MODE, auto_suggest=AutoSuggestFromHistory(),
                                                   style=self.__STYLE, completer=self.__MAIN_CMD_COMPLETER,
                                                   bottom_toolbar=self.bottom_toolbar)
                if str(self.__CMD).upper() == "EXIT" or str(self.__CMD).upper() == "QUIT":
                    self.__CMD = None
                else:
                    self._parse_cmd(self.__CMD)
            else:
                self.__SUB_CMD = self.__SESSION.prompt(self.__PROMPT_MODE, auto_suggest=AutoSuggestFromHistory(),
                                                       style=self.__STYLE,
                                                       completer=self.__SUB_CMD_COMPLETER,
                                                       bottom_toolbar=self.bottom_toolbar)
                if str(self.__SUB_CMD).upper() == "DONE":
                    self.set_prompt_mode(".")
                    self.set_sub_prompt_mode(".")
                elif str(self.__SUB_CMD).upper() == "EXIT" or str(self.__SUB_CMD).upper() == "QUIT":
                    self.__CMD = None
                else:
                    self._parse_sub_cmd(self.__SUB_CMD)

    def _parse_cmd(self, raw_cmd):
        """ Parse the main command and act accordingly. It splits the whole string to array based on space
            character and treats the first element of array as command and rest as parameters

            Args:
                raw_cmd (String): The whole command string passed to this method
        """
        cmds = str(raw_cmd).split(' ')
        cmd = cmds[0]  # first element is command itself
        cmds.remove(cmd)  # rest are the parameters
        # params = cmds
        del cmds
        if str(cmd).upper() in self.__MAIN_CMD_COMPLETER_LIST:
            self.set_prompt_mode(cmd)
            if str(cmd).upper() == "BROWSE":
                self.__SUB_CMD_COMPLETER = WordCompleter(self.__COMPLETER_DICT_LIST['BROWSE'], ignore_case=True)
                self.__SUB_CMD_COMPLETER_LIST = self.__COMPLETER_DICT_LIST['BROWSE']
            elif str(cmd).upper() == "HELP":
                help.print_main_cmd_help(self.__MAIN_CMD_COMPLETER_LIST)
        elif cmd != "":
            print("Invalid command provided! Please type HELP to get more information")
        else:
            self.set_prompt_mode(".")

    def _parse_sub_cmd(self, raw_sub_cmd):
        """Parse sub cmd and act accordimgly. It splits the whole string to array based on space
            character and treats the first element of array as command and rest as parameters

            Args:
                raw_sub_cmd (String): The whole command string passed to this method
        """
        sub_cmds = str(raw_sub_cmd).split(' ')
        sub_cmd = sub_cmds[0]  # first element is command itself
        sub_cmds.remove(sub_cmd)  # rest are the parameters
        sub_params = sub_cmds
        del sub_cmds
        if str(sub_cmd).upper() in self.__SUB_CMD_COMPLETER_LIST:
            self.set_sub_prompt_mode(sub_cmd)
            if self.__CMD == "BROWSE":
                self._process_browse_sub_cmds(sub_cmd, sub_params)
        elif sub_cmd != "":
            print("Invalid sub commamd provided! Please type <Main Cmd> HELP to get more information")
        else:
            self.set_prompt_mode(".")

    def _process_browse_sub_cmds(self, sub_cmd, sub_params):
        """Process all sub commands available under main command BROWSE

            Args:
                sub_cmd (String): A sub command issues by the user
        """
        if str(sub_cmd).upper() == "CONNECT":
            self._warehouse_conn = self._sub_commands.connect(sub_params)
        elif str(sub_cmd).upper() == "SCHEMAS":
            self._sub_commands.list_schemas(sub_params)
        elif str(sub_cmd).upper() == "TABLES":
            self._sub_commands.list_tables(sub_params)
        elif str(sub_cmd).upper() == "VIEWS":
            self._sub_commands.list_views(sub_params)
        elif str(sub_cmd).upper() == "VIEW-DEF":
            self._sub_commands.print_view_def(sub_params)
        elif str(sub_cmd).upper() == "COLUMNS":
            self._sub_commands.list_columns(sub_params)
        elif str(sub_cmd).upper() == "COLUMN-NAMES":
            self._sub_commands.list_column_names(sub_params)
        elif str(sub_cmd).upper() == 'COLUMN-TYPE':
            self._sub_commands.print_column_type(sub_params)
        elif str(sub_cmd).upper() == "PK-COLUMNS":
            self._sub_commands.list_pk_columns(sub_params)
        elif str(sub_cmd).upper() == "PK-NAME":
            self._sub_commands.print_pk_name(sub_params)
        elif str(sub_cmd).upper() == "TABLE-OPTS":
            self._sub_commands.print_table_opts(sub_params)
        elif str(sub_cmd).upper() == "FK-COLUMNS":
            self._sub_commands.list_fk_columns(sub_params)
        elif str(sub_cmd).upper() == "CLOSE" or str(sub_cmd).upper() == "DISCONNECT":
            self._sub_commands.disconnect(sub_params)
            del self._warehouse_conn
        elif str(sub_cmd).upper() == "HELP":
            help.print_browse_sub_cmd_help(self.__SUB_CMD_COMPLETER_LIST)

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
        # self.__PROMPT_MODE[2] = ('class:submode', sub_cmd)


if __name__ == "__main__":
    b = BipyCli()
    b.run()
