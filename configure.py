#!/usr/bin/env python3
import os
import yaml
import requests

# load repositories/*
repository_filenames = [file for file in os.listdir('repositories') if file.endswith('.yml')]
repository_mapping = {}
for repository_filename in repository_filenames:
    repository_id = repository_filename.replace('.yml', '')
    repository_yml = yaml.load(open(f"repositories/{repository_filename}"), Loader=yaml.FullLoader)
    repository_mapping[repository_id] = repository_yml

# check for presence of arguments
if len(os.sys.argv) > 1:
    allowed_repositories = os.sys.argv[1:]
else:
    allowed_repositories = [repository_id for repository_id in repository_mapping]

# apply global settings
for repository_id in allowed_repositories:
    api_url = f"https://api.github.com/repos/EffortGames/{repository_id}"
    api_headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {os.environ['EG_GITHUB_TOKEN']}",
    }
    api_data = {
        "has_projects": False,
        "has_wiki": False,
        "use_squash_pr_title_as_default": True,
        "allow_update_branch": True,
        "delete_branch_on_merge": True,
    }
    api_response = requests.patch(api_url, headers=api_headers, json=api_data)
    # log errors, if any
    if api_response.status_code != 200:
        print(f"Failed to update repository {repository_id}")
        print(api_response.text)
