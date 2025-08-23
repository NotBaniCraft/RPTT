import os
import requests
from customfunc import info, warn, error

repo = "NotBaniCraft/RPTT"
branch = "main"

def download(files, destination=None):
    if destination:
        os.makedirs(destination, exist_ok=True)
        dest_path = destination
    else:
        dest_path = "."

    for file_path in files:
        # direct raw URL from GitHub for public repos
        url = f"https://raw.githubusercontent.com/{repo}/{branch}/{file_path}"
        r = requests.get(url)

        if r.status_code == 200:
            filename = os.path.basename(file_path)
            full_path = os.path.join(dest_path, filename)
            with open(full_path, "wb") as f:
                f.write(r.content)
            info(f"Downloaded '{file_path}' to '{full_path}'")
        else:
            warn(f"Failed to download '{file_path}', status code {r.status_code}")

# usage example:
# download(["README.md", "src/main.py"], "myfolder")