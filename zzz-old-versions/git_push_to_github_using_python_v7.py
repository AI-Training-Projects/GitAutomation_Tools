"""Before creating a new repository, a GET request is made to the GitHub API to check if the repository already exists. If the response status code is 404 (Not Found), then the script proceeds with creating the repository. If the repository already exists, the creation step is skipped."""

import os
import subprocess
import requests
import logging
import yaml

def read_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config['username'], config['org'], config['folders']

logging.basicConfig(filename='git_automation.log', level=logging.INFO)

access_token = os.getenv("GITHUB_ACCESS_TOKEN")
username, org, folders = read_config()

for folder_path in folders:
    try:
        folder_name = os.path.basename(folder_path)
        os.chdir(folder_path)

        if not os.path.exists(".git"):
            subprocess.run(["git", "init"])
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", "automated initial commit"])
        else:
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", "automated update commit"])

        # Check if the repository already exists
        response = requests.get(
            f"https://api.github.com/repos/{org}/{folder_name}",
            headers={"Authorization": f"token {access_token}"}
        )

        # If the repository does not exist, create it
        if response.status_code == 404:
            response = requests.post(
                f"https://api.github.com/orgs/{org}/repos",
                json={"name": folder_name},
                headers={"Authorization": f"token {access_token}"}
            )
            response.raise_for_status()

        https_url = response.json()["clone_url"]
        https_url_with_token = https_url.replace("https://", f"https://{username}:{access_token}@")
        subprocess.run(["git", "remote", "add", "origin", https_url_with_token])
        subprocess.run(["git", "push", "-u", "origin", "master"])

        logging.info(f"Successfully processed folder: {folder_name}")
        os.chdir("..")

    except Exception as e:
        logging.error(f"Failed to process folder: {folder_name}. Error: {e}")