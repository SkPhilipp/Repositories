# C# Workflows

## Common Issues

### NETSDK1045

Seen in https://imgur.com/71ls9dt

Modify the Target Framework of each C# project to a dotnet version installed by the workflows.
Alternatively modify the workflow to install the referenced dotnet version.

### At `dotnet nuget add source`

Seen in https://imgur.com/AHFpi0S

The GitHub Packages secret is not valid on this repository. Make the organization secret available to the repository, or refresh the secret.

### At `dotnet sonarscanner end`

Seen in https://imgur.com/6JH3pTy

The project likely does not yet exist in sonarcloud.io/, navigate to the website and create a new project there for the repository.

### At `dotnet nuget push`

Seen in https://imgur.com/gL1z6VN

The project has no RepositoryUrl configured in its .csproj file.

Example .csproj file;

```
<Project Sdk="Microsoft.NET.Sdk">

    <PropertyGroup>
        (...)
        <RepositoryUrl>https://github.com/EffortGames/YOUR_REPOSITORY.git</RepositoryUrl>
    </PropertyGroup>

</Project>
```
