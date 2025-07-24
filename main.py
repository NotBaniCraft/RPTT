import os
import sys
import subprocess
import time

if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)a
from customfunc import warn
from customfunc import info
from customfunc import error
from registryfuncs import get_registry
from registryfuncs import set_registry
from setup import download


def onos():
    from cmdprompt import cmdprompt # type: ignore
    cmdprompt()  # Assuming cmdprompt has a function named cmdprompt

def main():
    FirstTimeUse = get_registry("FirstTimeUse")
    if FirstTimeUse == "True":
        print("""Welcome to RPTT!
Version: a1
Would you like to install the OS? (Y/N)""")
        installdec = input().upper()
        if installdec == "Y":
            info("Creating directories...")
            os.makedirs("RPTTRoot", exist_ok=True)
            info("RPTTRoot dir created")
            os.makedirs(os.path.join("RPTTRoot", "SystemApps"), exist_ok=True)
            sys.path.append(os.path.join(base_path, 'RPTTRoot', 'SystemApps'))
            info("RPTTRoot/SystemApps dir created")
            os.makedirs(os.path.join("RPTTRoot", "Apps"), exist_ok=True)
            sys.path.append(os.path.join(base_path, 'RPTTRoot', 'Apps'))
            info("RPTTRoot/Apps dir created")
            info("Downloading files...")
            download(["RPTTRoot/SystemApps/cmdprompt.py"], "RPTTRoot/SystemApps")
            if input("Would you like to download rock paper scissors? (Y/N)").upper() == "Y":
                download(["RPTTRoot/Apps/rps.py"], "RPTTRoot/Apps")
            info("Initializing registries...")
            set_registry("FirstTimeUse", "False")
            print("Booting to RPTT...")
            onos()
        elif installdec == "N":
            print("bye then ig, run program again to install")
            return
        else:
            main()
    elif FirstTimeUse == "False":
        print("Booting to RPTT...")
        onos()
    elif FirstTimeUse is None:
        error("Critical files or configurations weren't found.")
        info("Initializing registries...")
        set_registry("FirstTimeUse", "True")
        print("Rebooting...")
        main()

# Run the program
if __name__ == "__main__":
    main()
