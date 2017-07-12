from models import *


lists = SwitchClient.lists()

def get_class_names():
    classes = []
    import sys, inspect
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            try:
                if obj.Meta:
                    if name is not 'Model' and not obj.Meta.abstract and obj.Meta.switchdb_model:
                        classes.append(name)
            except AttributeError:
                pass
    return classes


def handle_new_classes():
    """
        If a new model registered, create a list for that model  
    """
    map(lambda model: create_list(model), [r for r in get_class_names() if r not in lists])


def create_list(model):
    """
        New list create function in a given SwitchClient db 
    """
    # TODO write function
    pass


handle_new_classes()

print MyModel.lists()

# TODO: Check all models.py files in project dir
# import os
# basedir = "C:\Projects\switchdb"
# for file in os.listdir(basedir):
#     if file == "model.py":
#         print(os.path.join(basedir, file))



# TODO: Cache builds
# filename = 'registered_classes.json'
# def get_registered_classes():
#     """
#         exist = registered_classes.json
#         exist ? overwrite registered_classes.json : open and overwrite
#         :return class names of registered models in json format
#     """
#     import json
#     try:
#         f = open(filename, 'w')
#         json_data = {'classes': get_class_names()}
#         f.write(json.dumps(json_data, ensure_ascii=False))
#         f.close()
#         return json_data
#     except Exception as e:
#         print e


