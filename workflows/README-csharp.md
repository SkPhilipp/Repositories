# C# Workflows

## Common Issues

### NETSDK1045

Seen in https://imgur.com/71ls9dt

Modify the Target Framework of each C# project to a dotnet version installed by the workflows.

### At `dotnet nuget add source`

Seen in https://imgur.com/AHFpi0S

The GitHub Packages secret is not valid on this repository. Make the organization secret available to the repository, or refresh the secret.

### At `dotnet sonarscanner end`

Seen in https://imgur.com/6JH3pTy

The project likely does not yet exist in sonarcloud.io/, navigate to the website and create a new project there for the repository.
