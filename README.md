# vcs-migration-tooling
Tooling to support migrations from Bitbucket to Github. More information on the repository setup can be found on our Confluence space.

### Cloning the repository
- Run ```git clone git@github.com:HT2-Labs/vcs-migration-tooling.git```

### Define params and repos
- Create and update your ```params.py``` file
- Run ```cp common/params-dist.py common/params.py```

### Define files to migrate
- Create a ```files-to-migrate``` directory for any files you want to add
- Run ```mkdir files-to-migrate```

- Make sure you add any files you want to add to the repository into this directory
- Make sure you update the ```createDirectories``` function in your ```params.py``` file to create the correct directory structure
- Make sure you update the ```createFiles``` function in your ```params.py``` file to add the correct files to the repository
- Make sure you update the ```filesToAdd``` parameter in your ```params.py``` file to add the correct files to the staging area

### Update the package.json
- The ```Update the package.json``` section of the ```pre-github-move.py``` file is mandatory
- You can update the ```updatePackageJson``` function in your ```params.py``` file to update the ```package.json``` how you'd like, or alternatively use the default

### Enable/disable settings and create a PR
- The ```Enable/disable settings and create a PR``` section of the ```migration-github.py``` file is optional
- You can update the settings in your ```params.py``` file to update the repository settings how you'd like

### Ensure the latest tag has a 'v' at the beginning
- The ```Ensure the latest tag has a 'v' at the beginning``` section of the ```migration-github.py``` file is optional
- This will be enabled by default if the ```addSemanticReleaseBool``` is set to ```True```

### Assign teams with correct permissions
- The ```Assign teams with correct permissions``` section of the ```migration-github.py``` file is optional
- You can update the teams and permissions in your ```params.py``` file
