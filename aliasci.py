import argparse
import toml
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


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert a cli toml file to different command line scripts used to permanently set an alias for different tools")
    parser.add_argument('config_file',
                        type=argparse.FileType(encoding='UTF-8'),
                        default='./aliases.toml',
                        nargs='?',
                        help='The config file containing a list of command line arguments')

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


def generate_script(config, console_type):
    script = str()
    merged_config = _merge(config, str(console_type))
    for (key, value) in merged_config.items():
        if console_type is ConsoleType.POWERSHELL:
            script += f'Set-Alias -Name {key} -Value {value}\n'
        elif console_type is ConsoleType.BASH or console_type is ConsoleType.FISH:
            script += f'alias {key}="{value}"\n'
        elif console_type is ConsoleType.CMD:
            script += f'doskey {key}={value} $*\n'
    return script


def main():
    args = parse_args()
    print(f'Generate aliases scripts for config file "{args.config_file.name}"')

    config = load_toml_config(args.config_file.read())

    Path("./out").mkdir(parents=True, exist_ok=True)
    for console_type in ConsoleType:
        script = generate_script(config, console_type)
        with open(f"./out/{_script_name(console_type)}", "w+") as f:
            f.write(script)


if __name__ == '__main__':
    main()
