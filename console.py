#!/usr/bin/python3
"""Entry point of command line interpreter"""


import cmd
import json
import os
import inspect
import importlib
from models import storage

models_path = os.path.join(os.path.dirname(__file__), 'models')
class_objects = {}
for file_name in os.listdir(models_path):
    # module = importlib.import_module(f"models.{module_name}")
    if file_name.endswith('.py') and file_name != '__init__.py':
        module_name = file_name[:-3]
        module = importlib.import_module(f"models.{module_name}")
        members = inspect.getmembers(module, inspect.isclass)
        class_objects.update({name: obj for name, obj in members})
    

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
        elif line not in class_objects.keys():
            print(class_objects)
            print(self.not_exist_class)
        else:
            new_cls = class_objects[line]()
            new_cls.save()
            print(new_cls.id)

    def do_show(self, line):
        """Prints the string representation of an instance based on the class
        name and id. Usage: <show classname class_id>.
        Ex. show BaseModel 123-123
        """
        storage.reload()
        all_objects = storage.all()
        
        line_split = line.split()

        def find_obj():
            for value in all_objects.values():
                if value['id'] == line_split[1]:
                    return value

        if not line:
            print(self.missing_class)
        elif not line_split[0] in class_objects.keys():
            print(self.not_exist_class)
        elif len(line.split()) < 2:
            print(self.missing_id)
        elif line_split[1]:
            print(str(class_objects[line_split[0]](**find_obj()) if find_obj() else
                  self.instance_not_found))
            

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id.
        Usage: destroy <classname> <id>.
        E.g destroy BaseModel 123-1233
        """
        line_split = line.split()
        if not line:
            print(self.missing_class)
        elif not line_split[0] in class_objects.keys():
            print(self.not_exist_class)
        elif not line_split[1]:
            print(self.missing_id)
        elif line_split[1]:
            storage.reload()
            all_objects = storage.all()
            for key, value in all_objects.items():
                if value['id'] == line_split[1] and key.split('.')[0] == line_split[0]:
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
        all_instance = []
        if line:
            if line not in class_objects.keys():
                print(self.missing_class)
            else:
                storage.reload()
                all_objects = storage.all()
                for value in all_objects.values():
                    if line == value["__class__"]:
                        all_instance.append(str(class_objects[value["__class__"]](**value)))
                print(all_instance)

    def do_update(self, line):
        """Updates an instance based on the class name aand id by adding
        or updating attribute.
        Usage: update <classname> <id> <attribute name> "<attribute value>"
        E.g update BaseModel 123-123 name email "airbnb@mail.com"
        """
        storage.reload()
        all_objects = storage.all()
        line_split = line.split()
        if not line:
            print(self.missing_class)
        elif line_split[0] not in class_objects.keys():
            print(self.not_exist_class)
        elif len(line_split) < 2:
            print(self.missing_id)
        elif line_split[1]:
            for value in all_objects.values():
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
