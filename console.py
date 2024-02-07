#!/usr/bin/python3
"""Entry point of command line interpreter"""


import cmd
from models.base_model import BaseModel
from models import storage


class_names = ['BaseModel']


class HBNBCommand(cmd.Cmd):
    """A console for HBNB"""
    prompt = "(hbnb) "
    missing_class = "** class name is missing **"
    not_exist_class = "** class doesn't exist **"
    missing_id = "** instance id missing **"
    instance_not_found = "** no instance found **"

    def do_create(self, line):
        """Creates a new instance of BaseModel, saves it(to the JSON file)
        and prints the id. Usage: <create classname>.
        Ex. create BaseModel
        """
        if not line:
            print(self.missing_class)
        elif line not in class_names:
            print(self.not_exist_class)
        else:
            new_cls = globals()[line]()
            new_cls.save()
            print(new_cls.id)

    def do_show(self, line):
        """Prints the string representation of an instance based on the class
        name and id. Usage: <show classname class_id>.
        Ex. show BaseModel 123-123
        """
        all_objects = storage.all()

        def find_obj():
            for key, value in all_objects.items():
                for i, j in value.items():
                    if value['id'] == line.split()[1]:
                        return value

        if not line:
            print(self.missing_class)
        elif not line.split()[0] in class_names:
            print(self.not_exist_class)
        elif len(line.split()) < 2:
            print(self.missing_id)
        elif line.split()[1]:
            print(str(BaseModel(**find_obj()) if find_obj() else
                  self.instance_not_found))

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
