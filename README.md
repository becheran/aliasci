# aliasci

[![Python application](https://github.com/becheran/aliasci/actions/workflows/app.yml/badge.svg)](https://github.com/becheran/aliasci/actions/workflows/app.yml)

Unified repository to store aliases and use them in different command line tools.

Use with *python 3* and run the following command to generate scripts for different CLIs to the *out* directory:

``` sh
python aliasci.py
```

Run the following command to display the help function and all command line args:

``` sh
python aliasci.py -h
```

For this repo a [GitLab CI job](https://gitlab.com/becheran/aliasci_ci) is used to generate alias defined in the [config toml file](./aliases.toml).

## Result

Download the latest scripts to set the aliases here:

- [bash](https://gitlab.com/becheran/aliasci_ci/-/jobs/artifacts/master/raw/out/bash_aliases.sh?job=generate_scripts)
- [cmd](https://gitlab.com/becheran/aliasci_ci/-/jobs/artifacts/master/raw/out/cmd_aliases.cmd?job=generate_scripts)
- [cmder](https://gitlab.com/becheran/aliasci_ci/-/jobs/artifacts/master/raw/out/cmder_aliases.cmd?job=generate_scripts)
- [fish](https://gitlab.com/becheran/aliasci_ci/-/jobs/artifacts/master/raw/out/fish_aliases.sh?job=generate_scripts)
- [ps](https://gitlab.com/becheran/aliasci_ci/-/jobs/artifacts/master/raw/out/powershell_aliases.ps1?job=generate_scripts)
