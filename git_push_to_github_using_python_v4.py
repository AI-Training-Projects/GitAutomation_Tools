import os
import subprocess
import requests
import logging
import yaml

# Use read_config function to get configuration from config.yaml file
def read_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config['username'], config['org'], config['folders']

# Set up logging
logging.basicConfig(filename='git_automation.log', level=logging.INFO)

# Get Access Token from environment variable
access_token = os.getenv("GITHUB_ACCESS_TOKEN")

# Get the configuration data from the config.yaml file
username, org, folders = read_config()

# Loop through the folders
for folder_path in folders:
    try:
        # Extract the folder name from the full path
        folder_name = os.path.basename(folder_path)

        # Navigate to the folder
        os.chdir(folder_path)

        # Initialize a new Git repo or update an existing one
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"])
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", "automated initial commit"])
        else:
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", "automated initial commit"])

        # Create a new GitHub repo
        response = requests.post(
            f"https://api.github.com/orgs/{org}/repos",
            json={"name": folder_name},
            auth=(username, access_token)
        )
        response.raise_for_status()

        # Push the local repo to the new GitHub repo
        subprocess.run(["git", "remote", "add", "origin", response.json()["ssh_url"]])
        subprocess.run(["git", "push", "-u", "origin", "master"])

        # Log the success
        logging.info(f"Successfully processed folder: {folder_name}")

        # Navigate back to the parent directory
        os.chdir("..")

    except Exception as e:
        # Log the error
        logging.error(f"Failed to process folder: {folder_name}. Error: {e}")
        
