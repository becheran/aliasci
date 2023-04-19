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

<https://github.com/becheran/aliasci/releases/latest>
