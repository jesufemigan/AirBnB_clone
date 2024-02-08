#!/usr/bin/python3
"""Entry point of command line interpreter"""


import cmd
import json
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
    
    def do_destroy(self, line):
        """Deletes an instance based on the class name and id.
        Usage: destroy <classname> <id>.
        E.g destroy BaseModel 123-1233
        """
        if not line:
            print(self.missing_class)
        elif not line.split()[0] in class_names:
            print(self.not_exist_class)
        elif len(line.split()) < 2:
            print(self.missing_id)
        elif line.split()[1]:
            all_objects = storage.all()
            for key, value in all_objects.items():
                if value['id'] == line.split()[1]:
                    del all_objects[key]
                    with open("file.json", "w", encoding="utf-8") as f:
                        json.dump(all_objects, f)
                    return
            print(self.instance_not_found)
    
    def do_all(self, line):
        """Prints all the string representation of all instances based
        or not on the classname.
        Usage: all <classname>.
        E.g all BaseModel or all.
        """
        if line:
            if line not in class_names:
                print(self.missing_class)
            else:
                all_objects = storage.all()
                for key, value in all_objects.items():
                    print(str(BaseModel(**value)))
                    
    def do_update(self, line):
        """Updates an instance based on the class name aand id by adding
        or updating attribute.
        Usage: update <classname> <id> <attribute name> "<attribute value>"
        E.g update BaseModel 123-123 name email "airbnb@mail.com"
        """
        all_objects = storage.all()
        line_split = line.split()
        if not line:
            print(self.missing_class)
        elif line_split[0] not in class_names:
            print(self.not_exist_class)
        elif len(line_split) < 2:
            print(self.missing_id)
        elif line_split[1]:
            for key, value in all_objects.items():
                if value['id'] == line.split()[1]:
                    if len(line_split) >= 3 and line.split()[2]:
                        if len(line_split) >= 4 and line.split()[3]:
                            value.update({line.split()[2]: line.split()[3]})
                            with open("file.json", "w", encoding="utf-8") as f:
                                json.dump(all_objects, f)
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                    return
            print(self.instance_not_found)
    
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
