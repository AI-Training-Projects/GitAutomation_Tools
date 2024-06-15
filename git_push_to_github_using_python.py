import requests
import os 

# Set the required variables
username = "richlysakowski"
#access_token = "YourGitHubAccessToken"
access_token = os.getenv("GITHUB_ACCESS_TOKEN")
org = "AI-Training-Projects"  # The GitHub organization
repos = [
    "Ask_My_PDF",
    "Ask_Multiple_PDFs",
    "Streamlit_Cancer_Prediction"
]  # Add more repo names if needed

# Loop through the repos
for repo in repos:
    # Create the repo
    response = requests.post(
        f"https://api.github.com/orgs/{org}/repos",
        json={"name": repo},
        auth=(username, access_token)
    )
    
    if response.status_code == 201:
        print(f"Created repo: {repo}")
    else:
        print(f"Failed to create repo: {repo}")

