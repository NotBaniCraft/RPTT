import os
import requests
import base64
import json
from customfunc import info
from customfunc import error
from customfunc import warn

repo = "NotBaniCraft/RPTT"
branch = "main"
token = os.getenv("GITHUB_TOKEN")

def download(files, destination=None):
    if not token:
        error("Error: GITHUB_TOKEN env variable not set")
        exit(1)
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    
    # Handle destination folder
    if destination:
        # Create the destination folder if it doesn't exist
        os.makedirs(destination, exist_ok=True)
        dest_path = destination
    else:
        # Use current directory (where script is running)
        dest_path = "."
    
    for file_path in files:
        url = f"https://api.github.com/repos/{repo}/contents/{file_path}?ref={branch}"
        r = requests.get(url, headers=headers)
        
        if r.status_code == 200:
            content = json.loads(r.text)
            file_data = base64.b64decode(content['content'])
            
            # Get just the filename (not the full path)
            filename = file_path.split("/")[-1]
            
            # Combine destination path with filename
            full_path = os.path.join(dest_path, filename)
            
            with open(full_path, "wb") as f:
                f.write(file_data)
            info(f"Downloaded '{file_path}'")
        else:
            warn(f"Failed to download '{file_path}'")
            warn(f"Status code: '{r.status_code}', Response: '{r.text}'")

# Usage examples:
#if __name__ == "__main__":
    # Download to current folder (where script is running)
    #download(["customfunc.py", "main.py"])
    
    # Download to specific folder
    #download(["customfunc.py", "registryfuncs.py"], "RPTTRoot/SystemApps")
    
    # Download to another folder
    #download(["devhelp.txt"], "docs")