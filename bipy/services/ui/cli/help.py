"""Module to print help for various commands available through CLI
    Author: Ajeet Singh
    Date: 06/17/2019
"""


def print_main_cmd_help(cmd_list):
    """Print help for main commands"""
    print("Below commands are available...")
    for cmd in cmd_list:
        print(cmd)
    print("")
    print("To get more info on a particular command, please type...")
    print("<Main Cmd> --help")


def print_browse_sub_cmd_help(sub_cmd_list):
    """Print help for sub commands"""
    print("Below sub commands available...")
    for cmd in sub_cmd_list:
        print(cmd)
    print("")
    print("For further informatiom type...")
    print("<Sub Cmd> --help")


def print_connect_sub_cmd_help(sub_cmd_list):
    """Print help for sub commands"""
    print("Below sub commands available...")
    for cmd in sub_cmd_list:
        print(cmd)
    print("")
    print("For further informatiom type...")
    print("<Sub Cmd> --help")
