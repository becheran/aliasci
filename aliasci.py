import argparse
import toml
import os
from pathlib import Path

from enum import Enum
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class ConsoleType(Enum):
    BASH = 'bash'
    POWERSHELL = 'ps'
    CMD = 'cmd'
    FISH = 'fish'
    CMDER = 'cmder'


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert a cli toml file to different command line scripts used to permanently set an alias for "
                    "different tools")
    parser.add_argument('config_file',
                        type=argparse.FileType(encoding='UTF-8'),
                        default='./aliases.toml',
                        nargs='?',
                        help='The config file containing a list of command line arguments'),
    parser.add_argument('--out', '-o',
                        type=str,
                        default='./out/',
                        help='The out folder for all generated scripts.')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)
    return args


def load_toml_config(toml_string):
    toml_json = toml.loads(toml_string)
    if 'all' not in toml_json:
        eprint(f"The [all] section is missing in the toml file.")
        sys.exit(1)
    possible_keys = [e.value for e in ConsoleType]
    possible_keys.append("all")
    for key in toml_json:
        if key not in possible_keys:
            eprint(f"Unknown key {key}")
            sys.exit(1)
    return toml_json


def _merge(config, key):
    if key in config:
        return {**config['all'], **config[key]}
    return config['all']


def _script_name(console_type: ConsoleType):
    if console_type is ConsoleType.POWERSHELL:
        return 'powershell_aliases.ps1'
    elif console_type is ConsoleType.BASH:
        return 'bash_aliases.sh'
    elif console_type is ConsoleType.CMD:
        return 'cmd_aliases.cmd'
    elif console_type is ConsoleType.FISH:
        return 'fish_aliases.sh'
    elif console_type is ConsoleType.CMDER:
        return 'cmder_aliases.cmd'
    else:
        raise NotImplementedError(
            f'Not implemented console type "{console_type}" to script file name')


def generate_script(config, console_type):
    script = str()
    # Some consoles need a she bang
    if console_type is ConsoleType.FISH:
        script += '#!/usr/bin/env fish\n'
    if console_type is ConsoleType.BASH:
        script += '#!/usr/bin/env bash\n'

    merged_config = _merge(config, console_type.value)
    aliases_cmds = str()
    for (key, value) in merged_config.items():
        if console_type is ConsoleType.POWERSHELL:
            aliases_cmds += f'function get-{key} {{ param($var) {value} $var }}\n'
            aliases_cmds += f'Set-Alias -Name {key} -Value get-{key} -Force -Option AllScope\n'
        elif console_type is ConsoleType.BASH:
            aliases_cmds += f'alias {key}=\'{value}\'\n'
        elif console_type is ConsoleType.FISH:
            aliases_cmds += f'alias {key}="{value}"\n'
            aliases_cmds += f'funcsave {key}\n'
        elif console_type is ConsoleType.CMD:
            aliases_cmds += f'doskey {key}={value} $*\n'
        elif console_type is ConsoleType.CMDER:
            aliases_cmds += f'cmd /c alias {key}={value} $*\n'
        else:
            raise NotImplementedError(
                f'Missing generate script impl for console type "{console_type}"')
    script += aliases_cmds

    # Some consoles need additional steps to save keys persistently
    if console_type is ConsoleType.CMD:
        doskey_dir = 'c:\\windows\\bin\\'
        doskey_file_path = f'{doskey_dir}doskey.bat'
        script += f'if not exist {doskey_dir} mkdir {doskey_dir}\n'
        script += f'echo @echo off>{doskey_file_path}\n'
        for line in aliases_cmds.splitlines():
            script += f'echo {line}>>{doskey_file_path}\n'
        script += r'REG ADD "HKCU\Software\Microsoft\Command Processor" /t REG_SZ ' \
                  r'/v AutoRun /d c:\windows\bin\doskey.bat /f'
    elif console_type is ConsoleType.POWERSHELL:
        script += f'\n@"\n{aliases_cmds.replace("$", "`$")}\n"@ | Out-File -FilePath $PROFILE'
    elif console_type is ConsoleType.BASH:
        script += f"sed '/# aliasci_start/,/#aliasci_end/d' -i ~/.bashrc\n"
        script += f'echo "# aliasci_start">>~/.bashrc\n'
        for line in aliases_cmds.splitlines():
            script += f'echo "{line}">>~/.bashrc\n'
        script += f'echo "# aliasci_end">>~/.bashrc\n'
    return script


def main():
    args = parse_args()
    print(
        f'Generate aliases scripts for config file "{args.config_file.name}"')

    config = load_toml_config(args.config_file.read())

    Path(args.out).mkdir(parents=True, exist_ok=True)
    for console_type in ConsoleType:
        script = generate_script(config, console_type)
        with open(os.path.join(args.out, _script_name(console_type)), "w+") as f:
            f.write(script)
    print('Finished successfully. ')


if __name__ == '__main__':
    main()
