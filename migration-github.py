import os
import subprocess
from common.params import Params as p

for repo in p.repos:
    #
    # Create a new Github repository with the Bitbucket code
    #
    try:
        # Create the new Github repository
        githubCommand = f'gh repo create HT2-Labs/{repo["githubName"]} --private --team {p.primaryTeam}'
        subprocess.call(githubCommand.split())

        # Create a new directory for the Mirror repository
        if not os.path.exists('mirrorRepo'):
            os.mkdir('mirrorRepo')

        # Change to the Mirror directory
        os.chdir('mirrorRepo')

        # Clone the Bitbucket repository
        cloneBitbucketCommand = f'git clone --bare git@bitbucket.org:learningpool/{repo["bitbucketName"]}.git'
        os.system(cloneBitbucketCommand)

        # Change to the Bitbucket repository directory
        os.chdir(f'{repo["bitbucketName"]}.git')

        # Push the Bitbucket repository to the Github repository
        gitRepo = f'git@github.com:HT2-Labs/{repo["githubName"]}.git'
        subprocess.call(['git', 'push', '--mirror', gitRepo])
    except:
        print('Failed to create a new Github repository with the Bitbucket code.')
        print('Exiting program.')
        exit()

    #
    # Clone the Github repository we just created
    #
    try:
        # Create a new directory for the Github repository
        if not os.path.exists('../../githubRepo'):
            os.mkdir('../../githubRepo')

        # Change to the Github directory
        os.chdir('../../githubRepo')

        # Clone the Github repository
        cloneGithubCommand = f'git clone git@github.com:HT2-Labs/{repo["githubName"]}.git'
        os.system(cloneGithubCommand)

        # Change to the Github repository directory
        os.chdir(repo["githubName"])
    except:
        print('Failed to clone the Github repository we just created.')
        print('Exiting program.')
        exit()

    #
    # Enable/disable settings and create a PR
    #
    try:
        githubRepoName = f'HT2-Labs/{repo["githubName"]}'

        # Set the default branch
        if p.setDefaultBranch:
            defaultBranchCMD = f'gh repo edit {githubRepoName} --default-branch {p.defaultBranch}'
            os.system(defaultBranchCMD)

        # Disable merge commits
        if p.disableMergeCommits:
            disableMergeCommitsCMD = f'gh repo edit {githubRepoName} --enable-merge-commit=false'
            os.system(disableMergeCommitsCMD)

        # Disable allow rebase merging
        if p.disableAllowRebaseMerging:
            disableAllowRebaseMergingCMD = f'gh repo edit {githubRepoName} --enable-rebase-merge=false'
            os.system(disableAllowRebaseMergingCMD)

        # Enable automatically delete head branches
        if p.deleteHeadBranches:
            deleteHeadBranchesCMD = f'gh repo edit {githubRepoName} --delete-branch-on-merge'
            os.system(deleteHeadBranchesCMD)

        # Checkout the branch we created
        subprocess.call(['git', 'checkout', p.branchName])

        # Create the PR from the branch we created
        createPRCMD = f"gh pr create --title '{p.commitMessage}' --body '' --assignee @me --base {p.defaultBranch} --head {p.branchName}"
        os.system(createPRCMD)
    except:
        print('Failed to enable/disable settings and create a PR.')
        print('Exiting program.')
        exit()

    #
    # Ensure the latest tag has a 'v' at the beginning
    #
    try:
        if p.addSemanticReleaseBool == True:
            # Get the latest tag
            getLatestTag = 'git describe --tags --abbrev=0'
            result = subprocess.run(getLatestTag, shell=True, capture_output=True, text=True)
            latestTag = result.stdout.strip()
            
            # If latestTag exists and doesn't start with a 'v', create and push the new tag
            if latestTag:
                if latestTag.startswith('v'):
                    print(f'Tag already exists: {latestTag}')
                else:
                    # Checkout the latest tag
                    checkoutTag = f'git checkout {latestTag}'
                    subprocess.run(checkoutTag, shell=True)

                    # Create and push new tag with a 'v' at the start
                    newTag = f'v{latestTag}'
                    createTag = f'git tag {newTag}'
                    subprocess.run(createTag, shell=True)

                    pushTag = f'git push origin {newTag}'
                    subprocess.run(pushTag, shell=True)

                    print(f'Created and pushed new tag: {newTag}')
            else:
                print('No latest tag found.')
    except:
        print('Failed to ensure the latest tag has a v at the beginning.')
        print('Exiting program.')
        exit()

    #
    # Assign teams with correct permissions
    #
    try:
        for team in p.teams:
            assignTeam = f"gh api -X PUT -H 'Accept: application/vnd.github+json' -H 'X-GitHub-Api-Version: 2022-11-28' '/orgs/{p.org}/teams/{team['teamName']}/repos/{p.org}/{repo['githubName']}' -f 'permission={team['permission']}'"
            subprocess.run(assignTeam, shell=True)

        # Change back to the original directory
        os.chdir("../..")
    except:
        print('Failed to assign teams with correct permissions.')
        print('Exiting program.')
        exit()
