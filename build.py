import os
import os.path
import shutil

default_lib_folder = "lib" 

# Add __init__.py to all directories
for d in os.listdir(default_lib_folder):
    if not os.path.isfile(os.path.join(default_lib_folder, d)):
        open(os.path.join(default_lib_folder, d, "__init__.py"), "w").close()


# Add __init__.py to lib root
open(os.path.join(default_lib_folder, "__init__.py"), "w").close
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


# README.md can be generated


# Copy setup.py, README.md
files_to_copy = ["setup.py", "README.md"]
for file in files_to_copy:
    shutil.copyfile(file, os.path.join(default_lib_folder, file))

print(" and ".join(files_to_copy) + " have been copied")

shutil.rmtree("scailo_sdk")
os.rename(default_lib_folder, "scailo_sdk")