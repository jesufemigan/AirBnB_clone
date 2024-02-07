#!/usr/bin/python3
"""Entry point of command line interpreter"""


import cmd


class HBNBCommand(cmd.Cmd):
    """A console for HBNB"""
    prompt = "(hbnb) "

    def emptyline(self):
        """do nothing for empty line"""
        pass

    def do_quit(self, line):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, line):
        """exits the program"""
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
