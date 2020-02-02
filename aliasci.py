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
    possible_keys = [e.value for e in ConsoleType]
    possible_keys.append("all")
    for key in toml_json:
        if key not in possible_keys:
            eprint(f"Unknown key {key}")
            sys.exit(1)
    return toml_json


def main():
    args = parse_args()

    config = load_toml_config(args.config_file.read())

    # TODO Run script
    print(config)


if __name__ == '__main__':
    main()
