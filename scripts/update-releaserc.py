import os
import subprocess
from common.params import Params as p

for repo in p.repos:
    try:
        # Change to the Github directory
        os.chdir(f'githubRepo/{repo["githubName"]}')

        # Create a new branch
        subprocess.call(['git', 'checkout', p.branchName])

        # Copy the releaserc file to the root of the repository
        os.system('cp ../../files-to-migrate/.releaserc .')

        # Add the new files
        subprocess.call(['git', 'add', '.releaserc'])

        # Commit the new files
        subprocess.call(['git', 'commit', '-m', p.commitMessage])

        # Push the new branch to the remote repository
        subprocess.call(['git', 'push'])

        # # Change back to the root directory
        os.chdir("../..")
    except:
        print('Failed to push the new releaserc file.')
        print('Exiting program.')
        exit()
