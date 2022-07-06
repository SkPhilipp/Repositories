#!/usr/bin/env python
import os
import glob
import yaml
import subprocess

# load types/*
type_filenames = [file for file in os.listdir('types') if file.endswith('.yml')]
type_mapping = {}
for type_filename in type_filenames:
    type_id = type_filename.replace('.yml', '')
    type_yml = yaml.load(open(f"types/{type_filename}"), Loader=yaml.FullLoader)
    type_mapping[type_id] = type_yml

# expand types with workflow filenames
for type_id, type_yml in type_mapping.items():
    workflows = []
    for workflow_glob in type_yml['workflows']:
        workflow_filenames = [file for file in glob.glob(f"workflows/{workflow_glob}")]
        for workflow_filename in workflow_filenames:
            workflow_absolute_path = os.path.abspath(workflow_filename)
            workflows.append(workflow_absolute_path)
    type_yml['workflows'] = workflows

# load repositories/*, expanding them with referenced type and url
repository_filenames = [file for file in os.listdir('repositories') if file.endswith('.yml')]
repository_mapping = {}
for repository_filename in repository_filenames:
    repository_id = repository_filename.replace('.yml', '')
    repository_yml = yaml.load(open(f"repositories/{repository_filename}"), Loader=yaml.FullLoader)
    type_id = repository_yml['type']
    if type_id not in type_mapping:
        raise Exception(f"Type {type_id} referenced by repository {repository_id} was not found")
    type_yml = type_mapping[type_id]
    repository_yml.update(type_yml)
    repository_yml['url'] = f"https://github.com/EffortGames/{repository_id}.git"
    repository_mapping[repository_id] = repository_yml

# check for presence of arguments
if len(os.sys.argv) > 1:
    allowed_repositories = os.sys.argv[1:]
else:
    allowed_repositories = [repository_id for repository_id in repository_mapping]

for repository_id in allowed_repositories:
    repository_yml = repository_mapping[repository_id]
    print("---")
    print(f"Cloning {repository_id}")
    subprocess.run(["git", "clone", "--quiet", "--depth=1", repository_yml['url'], "repository_tmp"])
    os.chdir('repository_tmp')
    # ensure parent directory exists
    subprocess.run(["mkdir", "-p", ".github/workflows"])
    for workflow_absolute_path in repository_yml['workflows']:
        # copy each workflow into the repository
        workflow_filename = os.path.basename(workflow_absolute_path)
        workflow_target_path = f".github/workflows/{workflow_filename}"
        subprocess.run(["cp", workflow_absolute_path, workflow_target_path])
        subprocess.run(["git", "add", workflow_target_path])
    # check for any changes
    no_diffs = subprocess.run(["git", "diff", "--exit-code", "--quiet", "HEAD"]).returncode == 0
    if no_diffs:
        print(f"No changes in {repository_id}")
        os.chdir('..')
        rm_ok = subprocess.run(["rm", "-rf", "repository_tmp"])
        if not rm_ok:
            print(f"Failed to remove {repository_id}")
            exit(1)
        continue
    # commit and push
    print(f"Committing and pushing {repository_id}")
    subprocess.run(["git", "commit", "-m", "Update"])
    os.system('git push')
    os.chdir('..')
    rm_ok = subprocess.run(["rm", "-rf", "repository_tmp"])
    if not rm_ok:
        print(f"Failed to remove {repository_id}")
        exit(1)
