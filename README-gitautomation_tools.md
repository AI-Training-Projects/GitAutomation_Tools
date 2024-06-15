

The folders list in the config.yaml file should contain the full paths to the repositories. 
The script extracts the folder names from these paths before interacting with the GitHub API, but uses the full paths to navigate to the repositories on your local machine.


# TODO: check to make sure a remote repo doesn't already exist
# TODO: add a final output message to let the user know the script has finished
# TODO: add the user's "default" git folder (in Windows in user "Documents" folder) as a separate config.yaml config variable.
