#!/usr/bin/python3
"""Entry point of command line interpreter"""


import cmd
import os
import re
from shlex import split
import inspect
import importlib
from models import storage


def import_classes():
    models_path = os.path.join(os.path.dirname(__file__), 'models')
    class_objects = {}
    for file_name in os.listdir(models_path):
        if file_name.endswith('.py') and file_name != '__init__.py':
            module_name = file_name[:-3]
            module = importlib.import_module(f"models.{module_name}")
            members = inspect.getmembers(module, inspect.isclass)
            class_objects.update({name: obj for name, obj in members})
    return class_objects


class_objects = import_classes()


def parse(line):
    """A function that parses the command line argument in console"""
    curly_braces = re.search(r"\{(.*?)\}", line)
    brackets = re.search(r"\((.*?)\)", line)

    if curly_braces is None:
        if brackets is None:
            return [i.strip(',') for i in split(line)]
        else:
            lexer = split(line[:brackets.span()[0]])
            line_arg = [i.strip(',') for i in lexer]
            line_arg.append(brackets.group())
            return line_arg
    else:
        lexer = split(line[:curly_braces.span()[0]])
        line_arg = [i.strip(',') for i in lexer]
        line_arg.append(curly_braces.group())
        return line_arg


class HBNBCommand(cmd.Cmd):
    """A console for HBNB"""
    prompt = "(hbnb) "
    missing_class = "** class name is missing **"
    not_exist_class = "** class doesn't exist **"
    missing_id = "** instance id missing **"
    instance_not_found = "** no instance found **"

    def default(self, arg):
        """Handles custom command line arguments"""
        custom_command = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            line = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", line[1])
            if match is not None:
                command = [line[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in custom_command.keys():
                    call = f"{line[0]} {command[1]}"
                    return custom_command[command[0]](call)
        print(f"*** Unknown syntax: {arg}")
        return

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it(to the JSON file)
        and prints the id. Usage: <create classname>.
        Ex. create BaseModel
        """
        line = parse(arg)
        if not line:
            print(self.missing_class)
        elif line[0] not in class_objects.keys():
            print(class_objects)
            print(self.not_exist_class)
        else:
            new_cls = class_objects[line[0]]()
            new_cls.save()
            print(new_cls.id)

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class
        name and id. Usage: <show classname class_id>.
        Ex. show BaseModel 123-123
        """
        line_split = parse(arg)
        storage.reload()
        all_objects = storage.all()

        def find_obj():
            for value in all_objects.values():
                if value['id'] == line_split[1]:
                    return value

        if len(arg) == 0:
            print(self.missing_class)
        elif not line_split[0] in class_objects.keys():
            print(self.not_exist_class)
        elif len(arg) < 2:
            print(self.missing_id)
        elif line_split[1]:
            print(str(class_objects[line_split[0]](**find_obj()) if find_obj()
                      else self.instance_not_found))

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id.
        Usage: destroy <classname> <id>.
        E.g destroy BaseModel 123-1233
        """
        line_split = parse(arg)
        if len(arg) == 0:
            print(self.missing_class)
        elif not line_split[0] in class_objects.keys():
            print(self.not_exist_class)
        elif not line_split[1]:
            print(self.missing_id)
        elif line_split[1]:
            storage.reload()
            all_objects = storage.all()
            for key, value in all_objects.items():
                if value['id'] == line_split[1] \
                   and key.split('.')[0] == line_split[0]:
                    del all_objects[key]
                    storage.save()
                    return
            print(self.instance_not_found)

    def do_all(self, arg):
        """Prints all the string representation of all instances based
        or not on the classname.
        Usage: all <classname>.
        E.g all BaseModel or all.
        """
        line = parse(arg)
        all_instance = []
        if line:
            if line[0] not in class_objects.keys():
                print(self.missing_class)
            else:
                storage.reload()
                all_objects = storage.all()
                for value in all_objects.values():
                    if line[0] == value["__class__"]:
                        all_instance.append(
                            str(class_objects[value["__class__"]](**value)))
                print(all_instance)

    def do_update(self, arg):
        """Updates an instance based on the class name aand id by adding
        or updating attribute.
        Usage: update <classname> <id> <attribute name> "<attribute value>"
        E.g update BaseModel 123-123 name email "airbnb@mail.com"
        """
        storage.reload()
        all_objects = storage.all()
        line_split = parse(arg)
        if len(arg) == 0:
            print(self.missing_class)
            return
        if line_split[0] not in class_objects.keys():
            print(self.not_exist_class)
            return
        if len(line_split) < 2:
            print(self.missing_id)
            return
        if f"{line_split[0]}.{line_split[1]}" not in all_objects.keys():
            print(self.instance_not_found)
            return
        if len(line_split) == 2:
            print("** attribute name missing **")
            return
        if len(line_split) == 3:
            try:
                type(eval(line_split[2])) != dict
            except NameError:
                print("** value missing **")
                return
        if len(line_split) == 4:
            for value in all_objects.values():
                if value['id'] == line_split[1]:
                    value.update({line_split[2]: line_split[3]})
                    storage.save()
                    return
        elif type(eval(line_split[2])) == dict:
            for value in all_objects.values():
                if value['id'] == line_split[1]:
                    for k, v in eval(line_split[2]).items():
                        value.update({k: v})
                    storage.save()
                    return
        print(self.instance_not_found)

    def do_count(self, arg):
        """Count the instance of a class in the object"""
        line_split = parse(arg)
        count = 0
        all_objects = storage.all()
        for key in all_objects.keys():
            if key.split('.')[0] == line_split[0]:
                count += 1
        print(count)

    def emptyline(self):
        """do nothing for empty line"""
        pass

    def do_quit(self, line):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, line):
        """exits the program"""
        print("")
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
