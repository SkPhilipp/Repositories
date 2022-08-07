# C# Workflows

## Common Issues

### Error "NETSDK1045"

![Error log](https://i.imgur.com/71ls9dt.png)

Modify the Target Framework of each C# project to a dotnet version installed by the workflows.
Alternatively modify the workflow to install the referenced dotnet version.

### Error at `dotnet nuget add source`

![Error log](https://i.imgur.com/AHFpi0S.png)

The GitHub Packages secret is not valid on this repository. Make the organization secret available to the repository, or refresh the secret.

### Error at `dotnet sonarscanner end`

![Error log](https://i.imgur.com/6JH3pTy.png)

The project likely does not yet exist in sonarcloud.io/, navigate to the website and create a new project there for the repository.

### Error at `dotnet nuget push`

![Error log](https://i.imgur.com/gL1z6VN.png)

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
