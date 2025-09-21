import os
import os.path
import shutil
import re

default_lib_folder = "lib" 

# Creates the init file for the project root (nothing will be exported)
def create_init_file_for_root(folder):
    init_file = open(os.path.join(folder, "__init__.py"), "w")
    init_file.flush()
    init_file.close()

# Creates the init file and exports all the modules in the folder. __init__.py will be created and stored within the folder
def create_init_file(folder):
    init_file = open(os.path.join(folder, "__init__.py"), "w")
    init_file.write("from .scailo_pb2 import *")
    init_file.flush()
    init_file.close()

# Creates the init file for buf folder
def create_init_file_for_buf(folder):
    init_file = open(os.path.join(folder, "__init__.py"), "w")
    init_file.write("from .validate import *")
    init_file.flush()
    init_file.close()

# Create the init file for the validate folder inside buf
def create_init_file_for_validate(folder):
    init_file = open(os.path.join(folder, "__init__.py"), "w")
    init_file.write("from .validate_pb2 import *")
    init_file.flush()
    init_file.close()

# Add __init__.py to all directories
for d in os.listdir(default_lib_folder):
    if not os.path.isfile(os.path.join(default_lib_folder, d)):
        if d == "buf":
            create_init_file_for_buf(os.path.join(default_lib_folder, d))
        else:    
            create_init_file(os.path.join(default_lib_folder, d))

# Add __init__.py to lib/buf/validate
create_init_file_for_validate(os.path.join(default_lib_folder, "buf", "validate"))

# Add __init__.py to lib root
create_init_file_for_root(os.path.join(default_lib_folder))
print("added __init__.py")

# Rename files
files = os.listdir(default_lib_folder)
for file in files:
    if file.endswith(".py"):
        t = file.removesuffix(".py")
        l = "_".join(t.split("."))
        l = l.replace("_connect", "_api")
        os.rename(f"{default_lib_folder}/{file}", f"{default_lib_folder}/{l}.py")

print("files have been renamed")

def process_api_file(file):
    api_file = ""
    api_file_match_pattern = r"import (.*)?.scailo_pb2"
    with open(file, "r") as f:
        api_file = f.read()

    start = 0
    end = 0

    all_submodules_to_import = []

    for match in re.finditer(api_file_match_pattern, api_file):
        if start == 0:
            start = match.start()
        end = match.end()
        all_submodules_to_import.append(re.findall(api_file_match_pattern, match.group())[0])

    if start > 0 and end > 0:
        sub_str = api_file[start: end]
        api_file = api_file.replace(sub_str, "from scailo_sdk import "+", ".join(all_submodules_to_import))
    return api_file

def process_pb2_file(file):
    pb2_file = ""
    pb2_file_match_pattern = r"from (.*) import (.*)?_pb2 as (.*)"
    with open(file, "r") as f:
        pb2_file = f.read()

    start = 0
    end = 0

    all_import_statements = []

    for match in re.finditer(pb2_file_match_pattern, pb2_file):
        if start == 0:
            start = match.start()
        end = match.end()
        matches = re.findall(pb2_file_match_pattern, match.group())[0]
        str = "from scailo_sdk." + matches[0] + " import " + matches[1]+"_pb2 as "+matches[2]
        all_import_statements.append(str)

    # print(all_import_statements)

    if start > 0 and end > 0:
        sub_str = pb2_file[start: end]
        pb2_file = pb2_file.replace(sub_str, "\n".join(all_import_statements))
    return pb2_file


def handle_api_files():
    api_files_list = []
    all_files = os.listdir(default_lib_folder)
    for f in all_files:
        if f != "__init__.py" and f.endswith("scailo_pb2_api.py"):
            api_files_list.append(f)
    for file in api_files_list:
        processed_api_file = process_api_file(os.path.join(default_lib_folder, file))
        with open(os.path.join(default_lib_folder, file), "w") as f:
            f.write(processed_api_file)

def handle_pb2_files():
    pb2_files_list = []
    for d in os.listdir(default_lib_folder):
        if os.path.isdir(os.path.join(default_lib_folder, d)) and d != "buf":
            file_to_check = os.path.join(default_lib_folder, d, "scailo_pb2.py")
            if os.path.isfile(file_to_check):
                pb2_files_list.append(file_to_check)

    for file in pb2_files_list:
        processed_pb2_file = process_pb2_file(file)
        with open(file, "w") as f:
            f.write(processed_pb2_file)

handle_api_files()
handle_pb2_files()


# README.md can be generated


sdk_folder = "scailo_sdk"

try:
    shutil.rmtree(sdk_folder)
except:
    pass
os.rename(default_lib_folder, sdk_folder)