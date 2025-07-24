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

    if destination:
        os.makedirs(destination, exist_ok=True)
        dest_path = destination
    else:
        dest_path = "."

    for file_path in files:
        url = f"https://api.github.com/repos/{repo}/contents/{file_path}?ref={branch}"
        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            content = r.json()

            if isinstance(content, dict):  # single file
                file_data = base64.b64decode(content['content'])
                filename = file_path.split("/")[-1]
                full_path = os.path.join(dest_path, filename)

                with open(full_path, "wb") as f:
                    f.write(file_data)
                info(f"Downloaded file '{file_path}'")

            elif isinstance(content, list):  # folder
                for item in content:
                    if item['type'] == 'file':
                        sub_url = item['url']
                        sub_r = requests.get(sub_url, headers=headers)
                        sub_content = sub_r.json()

                        file_data = base64.b64decode(sub_content['content'])
                        filename = item['name']
                        full_path = os.path.join(dest_path, filename)

                        with open(full_path, "wb") as f:
                            f.write(file_data)
                        info(f"Downloaded file '{item['path']}'")

            else:
                warn(f"Unexpected content type for '{file_path}'")

        else:
            warn(f"Failed to download '{file_path}'")
            warn(f"Status code: {r.status_code}, Response: {r.text}")