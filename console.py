#!/usr/bin/python3
"""Entry point of command line interpreter"""


import cmd


class HBNBCommand(cmd.Cmd):
    """A console for HBNB"""
    def do_quit(self):
        """exits the program"""
        return True
    def do_EOF(self):
        """exits the program"""
        return True


if __name == "__main__":

