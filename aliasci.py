import argparse
import sys
import toml

from enum import Enum

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

def checkTomlContent(toml):
    pass

def main():
    args = parse_args()

    parsed_toml = toml.loads(args.config_file.read())

    # TODO Run script
    print(parsed_toml)


if __name__ == '__main__':
    main()
