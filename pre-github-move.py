import os
import subprocess
import json
from common.params import Params as p

for repo in p.repos:
    #
    # Clone the repo and create a new branch
    #
    try:
        # Create a new directory for the Bitbucket repository
        if not os.path.exists('bitbucketRepo'):
            os.mkdir('bitbucketRepo')

        # Change to the Bitbucket directory
        os.chdir('bitbucketRepo')

        # Clone the repository
        cloneCommand = f'git clone git@bitbucket.org:learningpool/{repo["bitbucketName"]}.git'
        os.system(cloneCommand)

        # Change to the repository directory
        os.chdir(repo["bitbucketName"])

        # Create a new branch
        subprocess.call(['git', 'checkout', '-b', p.branchName])
    except:
        print('Failed to clone the repository and create a new branch.')
        print('Exiting program.')
        exit()

    #
    # Update the package.json
    #
    try:
        if p.manualPackageJsonBool == True:
            p.updatePackageJson(repo["githubName"])
        else:
            # Read the package.json and write it the data variable
            with open('package.json', 'r') as f:
                data = json.load(f)

            # Update the homepage key
            data['homepage'] = f'https://github.com/HT2-Labs/{repo["githubName"]}'

            # Update the private key
            data['private'] = 'true'

            # Update the 'repository' key
            data['repository'] = {
                'type': 'git',
                'url': f'git+https://github.com/HT2-Labs/{repo["githubName"]}.git'
            }

            # Add the Semantic Release devDependencies
            if p.addSemanticReleaseBool == True:
                data['devDependencies'] = {
                    "@semantic-release/commit-analyzer": "^9.0.2",
                    "@semantic-release/git": "^10.0.1",
                    "@semantic-release/github": "^8.0.7",
                    "@semantic-release/release-notes-generator": "^10.0.3",
                    "conventional-changelog-eslint": "^3.0.9",
                    "semantic-release": "19.0.3"
                }

                # Install the new dependencies
                subprocess.call([{p.packageManager}, 'install'])

            # Write the updated data back to the package.json file
            with open('package.json', 'w') as f:
                json.dump(data, f, indent=4)
    except:
        print('Failed to update the package.json file.')
        print('Exiting program.')
        exit()

    #
    # Create directories
    #
    try:
        if p.createDirectoriesBool == True:
            p.createDirectories()
    except:
        print('Failed to create directories.')
        print('Exiting program.')
        exit()

    #
    # Create files
    #
    try:
        if p.createFilesBool == True:
            p.createFiles()
    except:
        print('Failed to create files.')
        print('Exiting program.')
        exit()

    #
    # Push the new branch to the repo
    #
    try:
        # Add the new files
        gitAddCMD = ['git', 'add']  # Command to add files
        addFilesCMD = gitAddCMD + p.filesToAdd # Add files specified in the params.py file
        subprocess.call(addFilesCMD)

        # Commit the new files
        subprocess.call(['git', 'commit', '-m', p.commitMessage])

        # Push the new branch to the remote repository
        subprocess.call(['git', 'push', '-u', 'origin', p.branchName])

        # Change back to the root directory
        os.chdir("../..")
    except:
        print('Failed to push the new branch to the Bitbucket repository.')
        print('Exiting program.')
        exit()
