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
from bipy.services.integration import browser
from bipy.services.ui.cli import help


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
        'BROWSE', 'HELP', 'EXIT', 'QUIT'
    ]
    __SUB_CMD_COMPLETER_LIST = [
        'CONNECT', 'SCHEMAS', 'DATABASES', 'TABLES', 'VIEWS',
        'MAT-VIEWS', 'PROCS', 'FUNCS', 'PACKAGES', 'DONE', 'HELP',
        'EXIT', 'QUIT', 'VIEW-DEF', 'COLUMNS', 'COLUMN-NAMES',
        'COLUMN-TYPE'
    ]

    __MAIN_CMD_COMPLETER = WordCompleter(__MAIN_CMD_COMPLETER_LIST, ignore_case=True)
    __SUB_CMD_COMPLETER = WordCompleter(__SUB_CMD_COMPLETER_LIST, ignore_case=True)
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
                # Do nothing, wait for sub commands
                pass
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
                if str(sub_cmd).upper() == "CONNECT":
                    self._connect(sub_params)
                elif str(sub_cmd).upper() == "SCHEMAS":
                    self._list_schemas(sub_params)
                elif str(sub_cmd).upper() == "TABLES":
                    self._list_tables(sub_params)
                elif str(sub_cmd).upper() == "VIEWS":
                    self._list_views(sub_params)
                elif str(sub_cmd).upper() == "VIEW-DEF":
                    self._print_view_def(sub_params)
                elif str(sub_cmd).upper() == "COLUMNS":
                    self._list_columns(sub_params)
                elif str(sub_cmd).upper() == "COLUMN-NAMES":
                    self._list_column_names(sub_params)
                elif str(sub_cmd).upper() == 'COLUMN-TYPE':
                    self._print_column_type(sub_params)
                elif str(sub_cmd).upper() == "HELP":
                    help.print_browse_sub_cmd_help(self.__SUB_CMD_COMPLETER_LIST)
        elif sub_cmd != "":
            print("Invalid sub commamd provided! Please type <Main Cmd> HELP to get more information")
        else:
            self.set_prompt_mode(".")

    def _print_column_type(self, sub_params):
        """Print details of column type that exists under a given table

            Args:
                sub_params (Array): An array of string params. It should
                                    have a table & column name as of params
        """
        if sub_params.__len__() == 0:
            print("Missing table & column name parameter. Please use --help to get more info")
        elif sub_params[0].lower() != "--help" and sub_params[0] != "":
            if sub_params.__len__() == 2:
                print("============================== COLUMN TYPE ============================")
                table = sub_params[0]
                column = sub_params[1]
                column_type = browser.column_type(table, column)
                print("==>Table: %s, Column: %s, Type: %s" % (table, column, column_type))
                print("===================================================================")
            else:
                print("Missing column name param. Please use --help to get more info")
        elif sub_params[0].lower() == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("Print column type details of an column under an provided table")
            print("USAGE: COLUMN-TYPE <table-name> <column-name>")
            print("NOTE: both parameters are mandatory")
            print("")

    def _list_column_names(self, sub_params):
        """Print details of all column names that exists under a given table

            Args:
                sub_params (Array): An array of string params. It should
                                    have a table name as one of param
        """
        if sub_params.__len__() == 0:
            print("Missing table name parameter. Please use --help to get more info")
        elif sub_params[0].lower() != "--help" and sub_params[0] != "":
            print("============================== COLUMNS NAMES ============================")
            table = sub_params[0]
            columns = browser.column_names(table)
            for col in columns:
                print("==>%s" % (col))
            print("===================================================================")
        elif sub_params[0].lower() == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("List all columns with details under an provided table")
            print("USAGE: COLUMN-NAMES <table-name>")
            print("NOTE: parameter <table-name> is mandatory")
            print("")

    def _list_columns(self, sub_params):
        """Print details of all columns that exists under a given table

            Args:
                sub_params (Array): An array of string params. It should
                                    have a table name as one of param
        """
        if sub_params.__len__() == 0:
            print("Missing table name parameter. Please use --help to get more info")
        elif sub_params[0].lower() != "--help" and sub_params[0] != "":
            print("============================== COLUMNS ============================")
            table = sub_params[0]
            columns = browser.columns(table)
            for col in columns:
                print("==>%s" % (col))
            print("===================================================================")
        elif sub_params[0].lower() == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("List all columns with details under an provided table")
            print("USAGE: COLUMNS <table-name>")
            print("NOTE: parameter <table-name> is mandatory")
            print("")

    def _print_view_def(self, sub_params):
        """Print the definition of view passed as argument

            Args:
                sub_params (Array): An array of string params. Should
                                    have name of view as one of param
        """
        if sub_params.__len__() == 0:
            print("Missing View name paramete. Please type --help to get more information")
        elif sub_params[0].lower() != "--help" and sub_params[0] != "":
            view = sub_params[0]
            schema = None
            if sub_params.__len__() == 2:
                schema = sub_params[1]
            print("========================= VIEW DEF =============================")
            print(browser.view_definition(view, schema))
            print("================================================================")
        elif sub_params[0].lower() == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("VIEW-DEF command displays the SQL definition of an view")
            print("USAGE: VIEW-DEF <view-name> [schema-name]")
            print("NOTE: The <view-name> is a mandatory parameter & [schema-name] is optional")
            print("")

    def _list_views(self, sub_params):
        """List all available views under an schema in configured warehouse

            Args:
                sub_params (Array): An of string parameters. Can have name of schema as params
        """
        if sub_params.__len__() == 0:
            print("========================== VIEWS ==============================")
            views = browser.views(self._warehouse_conn)
            for vw in views:
                print("==>%s" % (vw))
            print("================================================================")
        elif sub_params[0].lower() != "--help" and sub_params[0] != "":
            print("========================== VIEWS ==============================")
            schema = sub_params[0]
            views = browser.views(self._warehouse_conn, schema)
            for vw in views:
                print("==>%s" % (vw))
            print("================================================================")
        elif sub_params[0] == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("VIEW sub command can be used with or without parameter")
            print("The parameter passed should be an name of schema which should exist in warehouse")
            print("USAGE: VIEW <schema name>")
            print("NOTE: If no schema is provided, views from all schemas will be listed")
            print("")
        else:
            print("========================== VIEWS ==============================")
            views = browser.views(self._warehouse_conn)
            for vw in views:
                print("==>%s" % (vw))
            print("================================================================")

    def _list_tables(self, sub_params):
        """List all available tables available under an schema in configured warehouse

            Args:
                sub_params (Array): An array of string parameters. Can have name of schema as params
        """
        if sub_params.__len__() == 0:
            print("========================== TABLES ==============================")
            tables = browser.tables(self._warehouse_conn)
            for tbl in tables:
                print("==>%s" % (tbl))
            print("================================================================")
        elif sub_params[0].lower() != "--help" and sub_params[0] != "":
            print("========================== TABLES ==============================")
            schema = sub_params[0]
            tables = browser.tables(self._warehouse_conn, schema)
            for tbl in tables:
                print("==>%s" % (tbl))
            print("================================================================")
        elif sub_params[0] == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("TABLE sub command can be used with or without parameter")
            print("The parameter passed should be an name of schema which should exist in warehouse")
            print("USAGE: TABLE <schema name>")
            print("NOTE: If no schema is provided, tables from all schemas will be listed")
            print("")
        else:
            print("========================== TABLES ==============================")
            tables = browser.tables(self._warehouse_conn)
            for tbl in tables:
                print("==>%s" % (tbl))
            print("================================================================")

    def _list_schemas(self, sub_params):
        """List all available schemas  in the configured warehouse database

            Args:
                sub_params (Array): An array of string parameters
        """
        if sub_params.__len__() == 0:
            print("====================== SCHEMAS ==========================")
            schemas = browser.schemas(self._warehouse_conn)
            for schema in schemas:
                print("==>%s" % (schema))
            print("=========================================================")
        elif str(sub_params[0]).lower() == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("List all available schemas in the configured warehouse database")
            print("No parameters are required to run this command")
            print("")
        else:
            print("ERROR: Command executed with invalid arguments. Please --help to get more information")

    def _connect(self, params):
        """Connects to either warehouse or repo based on params passed

            Args:
                params (Array): An array of string parameters
        """
        if params.__len__() == 0:
            self._warehouse_conn = browser.connect()
        elif str(params[0]).lower() == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("Connects to an Warehouse database configured in the system")
            print("No parameters are required to run this command")
            print("")

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
