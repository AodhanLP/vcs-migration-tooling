import os
import subprocess
import json

class Params:
    #
    # Variables
    #
    defaultBranch = 'master' # Default branch of the repository
    packageManager = 'npm' # Package manager used on the repository
    branchName = 'github-migration' # Your branch name
    commitMessage = f'Chore: {branchName} (TEST-001)' # Your commit message
    filesToAdd = ['.files', 'you.json', 'want.json', 'to.lock', 'add.yml'] # Files you want to add

    #
    # Booleans
    #
    manualPackageJsonBool = True # If you want to write your own instructions to update the package.json
    addSemanticReleaseBool = True # If you want to add Semantic Release dependencies to your package.json
    createDirectoriesBool = True # If you want to create directories - make sure to update the createDirectories function
    createFilesBool = True # If you want to create files - make sure to update the createFiles function

    #
    # Repository Settings
    #
    setDefaultBranch = True # Set the default branch for the repository to your defaultBranch variable
    disableMergeCommits = True # Disable merge commits on the repository
    disableAllowRebaseMerging = True # Disable allow rebase merging on the repository
    deleteHeadBranches = True # Delete branches on the repository after they are merged

    #
    # Team Permissions on Repositories
    #
    primaryTeam = 'Team' # The Github team you'd like as the primary team for the repositories
    org = 'My-Github-Org' # Your Github organisation name
    teams = [
        {
            "teamName": "My-Team", # Github team name
            "permission": "push" # pull, triage, push, maintain, admin
        },
        {
            "teamName": "My-Team-Reviewers", # Github team name
            "permission": "pull" # pull, triage, push, maintain, admin
        }
    ]

    #
    # Functions
    #
    def updatePackageJson(githubName): # Write your own instructions to update the package.json
        # Create a package.json file based on the bower.json
        subprocess.call(['cp', 'bower.json', 'package.json'])

        # Read the package.json and write it the data variable
        with open('package.json', 'r') as f:
            data = json.load(f)

        # Update the homepage key
        data['homepage'] = f'https://github.com/HT2-Labs/{githubName}'

        # Update the private key
        data['private'] = 'true'

        # Update the 'repository' key
        data['repository'] = {
            'type': 'git',
            'url': f'git+https://github.com/HT2-Labs/{githubName}.git'
        }

        if Params.addSemanticReleaseBool == True:
            # Check if 'devDependencies' key exists, if not, create it
            if 'devDependencies' not in data:
                data['devDependencies'] = {}

            # Add the Semantic Release devDependencies to the existing 'devDependencies'
            data['devDependencies'].update({
                "@semantic-release/commit-analyzer": "^9.0.2",
                "@semantic-release/git": "^10.0.1",
                "@semantic-release/github": "^8.0.7",
                "@semantic-release/release-notes-generator": "^10.0.3",
                "conventional-changelog-eslint": "^3.0.9",
                "semantic-release": "19.0.3"
            })

        # Add the Scripts key
        data['scripts'] = {
            "postversion": "cp package.json bower.json"
        }

        # Write the updated data back to the package.json file
        with open('package.json', 'w') as f:
            json.dump(data, f, indent=4)

        # Install the new dependencies
        subprocess.call(['yarn', 'install'])

    def createDirectories(): # Create directories in each repository
        # Create the .github directory if it doesn't already exist
        github_dir = '.github'
        if not os.path.exists(github_dir):
            os.mkdir(github_dir)

    def createFiles(): # Create files in each repository
        # Copy the CODEOWNERS file to the .github directory
        os.system('cp ../../files-to-migrate/adapt/CODEOWNERS .github/')

    #
    # List of repositories to migrate
    #
    repos = [
        {
            "bitbucketName": "testing-project", # Bitbucket repository name
            "githubName": "testing-project" # Github repository name
        },
        {
            "bitbucketName": "bitbucket-project", # Bitbucket repository name
            "githubName": "github-project" # Github repository name
        }
    ]
