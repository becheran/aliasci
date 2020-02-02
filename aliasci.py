import argparse
import sys
import toml

from enum import Enum
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class ConsoleType(Enum):
    BASH = 'bash'
    POWERSHELL = 'ps'
    FISH = 'fish'


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert a cli toml file to different command line scripts used to permanently set an alias for different tools")
    parser.add_argument('config_file', type=argparse.FileType(encoding='UTF-8'),
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


def main():
    args = parse_args()

    config = load_toml_config(args.config_file.read())

    ps_script = generate_ps(_merge(config, 'ps'))

    # TODO Run script
    print(ps_script)


def generate_ps(config):
    script = str()
    for (key, value) in config.items():
        script += f'Set-Alias -Name {key} -Value {value}\n'
    return script


if __name__ == '__main__':
    main()
