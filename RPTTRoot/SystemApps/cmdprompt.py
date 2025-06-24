import sys
import os
import shutil
import subprocess
root = os.getcwd()
RPTTroot = os.path.join(root, "RPTTRoot")
sys.path.append(root)
from registryfuncs import set_registry
from registryfuncs import delete_registry
from registryfuncs import get_registry
from customfunc import warn
from customfunc import error
from customfunc import info
endphrase = get_registry("EndPhraseSetting")
if endphrase == None:
       set_registry("EndPhraseSetting", "EOF")

def cd(command):
    global current_directory, runningin, relative_path  # we'll use a global variable to keep track of the current directory

    # If the command is '..', we go up one directory
    if command == "..":
       new_dir = os.path.dirname(current_directory)
       if new_dir.startswith(os.path.join(os.getcwd(), "RPTTRoot")):  # Ensure we're still inside RPTTRoot
              current_directory = new_dir
              runningin = current_directory  # Update runningin after changing directory
              relative_path = f"RPTTRoot{runningin.split("RPTTRoot", 1)[-1]}"
              print(f"Changed directory to: {relative_path}")
       else:
              print("❌ Error: Cannot go beyond RPTTRoot.")
    else:
       # Otherwise, we just change to the specified directory
       new_dir = os.path.join(current_directory, command)
       if os.path.isdir(new_dir):
              current_directory = new_dir
              runningin = current_directory  # Update runningin after changing directory
              relative_path = f"RPTTRoot{runningin.split("RPTTRoot", 1)[-1]}"
              print(f"Changed directory to: {relative_path}")
       else:
              print(f"❌ Error: '{command}' is not a valid directory.")

def new(command):
       path = os.path.join(runningin, command)
       if os.path.splitext(command)[1]:
              try:
                     with open(path, "x"):
                            print(f"File created in '{relative_path}'.")
              except FileExistsError:
                     error(f"This file already exists in '{relative_path}'.")
       else:
              try:
                     os.makedirs(path)
                     print(f"Directory created in '{relative_path}'.")
              except FileExistsError:
                     error(f"This directory already exists in '{relative_path}'.")

def delete(command):
       path = os.path.join(runningin, command)
       if os.path.isfile(path):
              try:
                     os.remove(path)
                     print(f"Removed file in '{relative_path}'.")
              except FileNotFoundError:
                     print(f"File could not be found in '{relative_path}'.")
       elif os.path.isdir(path):
              try:
                     os.rmdir(path)
                     print(f"Removed directory in '{relative_path}'.")
              except FileNotFoundError:
                     print(f"Directory could not be found in '{relative_path}'.")
              except OSError:
                     print(f"Directory in '{relative_path}' is not empty. Are you sure you would like to delete it? (Y/N)")
                     deletedir = input()
                     if deletedir == "Y":
                            shutil.rmtree(path)
                            print(f"Removed directory in '{relative_path}'.")
       else:
              print("honestly bad luck idk whats wrong now")

def write(command):
       path = os.path.join(runningin, command)
       if os.path.isfile(path):
              with open(path, "w") as p:
                     print(f"What would you like to write to the file? Type '{endphrase}' to end editing. (You can edit this with the command 'editendwrd'.)")
                     while True:
                            writeto = input()
                            if writeto == endphrase:
                                   break
                            else:
                                   p.write(writeto + "\n")

def read(command):
       path = os.path.join(runningin, command)
       if os.path.isfile(path):
              with open(path, "r") as p:
                     print("File's content:")
                     print(p.read())

def append(command):
       path = os.path.join(runningin, command)
       if os.path.isfile(path):
              print(f"What would you like to append to the file? Type '{endphrase}' to end editing. (You can edit this with the command 'editendwrd'.)")
              appendto = input()
              with open(path, "a") as p:
                     p.write(appendto)

def open(command):
       path = os.path.join(runningin, command)
       if os.path.isfile(path):
              subprocess.Popen(['python', path])
                     

def registrycommand():
       regcommand = input("reg>> ")
       if regcommand == "help":
              print("""List of registry editor commands:
help - this command
add - Adds a key to the registry.
del - Removes a key from the registry.
edit - Edits a key in the registry.
read - Prints a key's value from the registry.
check - Checks if a key exists.
exit - Exits the registry editor.""")
       elif regcommand == "add":
              print("Enter the name of the key you would like to add.")
              regaddname = input("reg-add>> ")
              print("Enter the value of the key you would like to add.")
              regaddvalue = input("red-add>> ")
              set_registry(regaddname, regaddvalue)
              registrycommand()
       elif regcommand == "del":
              print("Enter the name of the key you would like to delete.")
              regdelname = input("reg-del>> ")
              delete_registry(regdelname)
              registrycommand()
       elif regcommand == "edit":
              print("Enter the name of the key you would like to edit.")
              regeditname = input("reg-edit>> ")
              print("Enter the value you would like to edit the key's value to.")
              regeditvalue = input("reg-edit>> ")
              set_registry(regeditname, regeditvalue)
              registrycommand()
       elif regcommand == "read":
              print("Enter the name of the key you want to read the value of.")
              regreadname = input("reg-read>> ")
              print(get_registry(regreadname))
              registrycommand()
       elif regcommand == "check":
              print("Enter the name of the key you would like to see if exists.")
              regcommandname = input("reg-check>> ")
              print(get_registry(regcommandname))
              registrycommand()
       elif regcommand == "exit":
              runcommand()
       else:
              warn("Command not found. Run \"help\" for a list of commands.")
              registrycommand()

def hardwarecommand():
       hwcommand = input("hw>> ")
       if hwcommand == "gpu":
              if get_registry("HWGPUName") == None:
                     print("GPU name is not set yet. What would you like to set it to?")
                     gpuinput = input("hw-gpu>> ")
                     set_registry("HWGPUName", gpuinput)
                     info("Set GPU name.")
              else:
                     print(get_registry("HWGPUName"))


def runcommand():
       endphrase = get_registry("EndPhraseSetting"); _ = endphrase # pylance make yourself pyright pls its being used😭🙏 why did i have to _ = endphrase
       command = input(">> ")
       if command == "help":
                     print("""List of commands:
help - this command mate
where - Prints where the application is running.
registry - Enters the command prompt registry editor. Aliases: reg, regedit
list - Lists the directories and files in the current directory.
cd - Changes directory to inputted directory. "cd .." goes back one directory.
new - Creates a new file or directory if no file extension.
del - Deletes a file or directory if no file extension. Alias: delete
write - Writes to the inputted file name.
read - Reads the content of the inputted file name.
append - Appends to the inputted file name.
shutdown - Exits the whole operating system.
open - Opens a file.""")  #cd doesnt actually change where cmdprompt.py is running in obv, just where commands like "where" or "list" would run
                     runcommand()
       elif command == "where":
              # To show the relative path from RPTTRoot, we ensure it starts with 'RPTTRoot'
              print(f"Running in: {relative_path}")  # Print the full path
              runcommand()
       elif command == "registry" or command == "reg" or command == "regedit":
              print("RPTT a1 Command Prompt Registry Editor, enter \"help\" for list of commands.")
              registrycommand()
       elif command == "list":
              try:
                     directory = runningin
                     # Get the list of files in the directory
                     files = os.listdir(directory)
        
                     # Print each file
                     if files:
                            print(f"Files in '{relative_path}':")
                     for file in files:
                            print(file)
                     if not files:
                            print(f"No files found in '{relative_path}'.")
              except FileNotFoundError:
                     print(f"❌ Error: The directory '{relative_path}' does not exist.")
              except PermissionError:
                     print(f"❌ Error: Permission denied for accessing '{relative_path}'.")
              runcommand()
       elif command.startswith("cd "):
              directory = command[3:].strip()  # Get the directory after 'cd'
              cd(directory)  # Call the cd function
              runcommand()
       elif command.startswith("new "):
              file = command[4:].strip()
              new(file)
              runcommand()
       elif command.startswith("del ") or command.startswith("delete "):
              if command.startswith("del "):
                     file = command[4:].strip()
              elif command.startswith("delete "):
                     file = command[7:].strip()
              delete(file)
              runcommand()
       elif command.startswith("write "):
              file = command[6:].strip()
              write(file)
              runcommand()
       elif command.startswith("read "):
              file = command[5:].strip()
              read(file)
              runcommand()
       elif command.startswith("append "):
              file = command[7:].strip()
              append(file)
              runcommand()
       elif command == "shutdown":
              sys.exit()
       elif command.startswith("open "):
              file = command[5:].strip()
              open(file)
              runcommand()
       elif command == "hw":
              hardwarecommand()
       else:
              warn("Command not found. Run \"help\" for a list of commands.")
              runcommand()

def cmdprompt():
       while True:
              print("""
Current Application: cmdprompt
RPTT Command Prompt Version a1
Type "help" for the list of commands.""")
              global current_directory, runningin, relative_path
              # Set default starting directory to RPTTRoot\SystemApps
              current_directory = os.path.join(os.getcwd(), "RPTTRoot", "SystemApps")  # Default to RPTTRoot\SystemApps
              runningin = current_directory  # Initialize runningin with the default directory
              relative_path = f"RPTTRoot{runningin.split("RPTTRoot", 1)[-1]}"
              runcommand()