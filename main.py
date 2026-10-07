import argparse
import logging
import shutil
import subprocess
import sys

import requests
from rich.console import Console
from rich.markdown import Markdown

logging.basicConfig(filemode="a", filename="log.log", level=logging.DEBUG)
logger = logging.getLogger("main")
logger.debug('And... ACTION!')

def get_linux_package_manager():
    # Ordered dictionary of package managers and their corresponding major distributions
    package_managers = {
        'apt': 'Debian/Ubuntu/Mint',
        'dnf': 'Fedora/RHEL/CentOS',
        'pacman': 'Arch Linux/Manjaro',
        'zypper': 'openSUSE',
        'yum': 'Older RHEL/CentOS',
        'apk': 'Alpine'
    }
    
    # Check the system PATH for the package manager executable
    for binary, distro in package_managers.items():
        if shutil.which(binary) is not None:
            return {
                "binary": binary,
                "distribution_family": distro
            }
            
    return None

console = Console()

def printmd(md):
    mdobj = Markdown(md)
    console.print(mdobj)

printmd("**Stuff Package Manager**\n*Where you get your packages*")
print()

parser = argparse.ArgumentParser(description="Stuff Package Manager", epilog="Or, you could just google it and also like all the greats we have Super Ultra Amazing Cow Powers")
subparsers = parser.add_subparsers(dest="command", required=True)

parser_install = subparsers.add_parser("install", help="Install packages. Its in the name.")
parser_install.add_argument('package', help="The package you want to install")
parser_install.add_argument('--pm', help="Custom package manager; not reccomended to set!")

moo = subparsers.add_parser('moo', help="Super Cow Powers!")
moo.add_argument("--farts", help="Oops", action='store_true')
args = parser.parse_args()

if args.command == "install":
    print("So you have chosen an install\n")
    print("Downloading... ", end="")
    scr = requests.get(f'https://raw.githubusercontent.com/Archie-Aird/install-scripts/refs/heads/main/{args.package}/install.sh')
    if scr.status_code != 200:
        if scr.status_code == 404:
            print("FAIL: no such package")
        else:
            print("FAIL: status code " + str(scr.status_code))
        sys.exit(1)
    print("PASS")
    if args.pm:
        print("Package manager manually set.")
        distro = {"binary": args.pm, "distribution_family": "Customized"}
    else:
        print("Finding package manager.... ", end="")
        distro = get_linux_package_manager()
        print(distro['binary'] + " (" + distro["distribution_family"] + ")")
    print("Writing to file... ", end="")
    torun = scr.text
    torun = torun.replace("SPECIALPM", f'"{distro['binary']}"')
    torun = torun.replace("SPECIALDS", f'"{distro['distribution_family']}"')
    logger.debug(torun)
    try:
        with open("tempscr.sh", "w") as f:
            f.write(torun)
    except Exception:  # noqa: BLE001
        print("FAIL")
        sys.exit(1)
    print("PASS")
    print("Executing script... ", end="")
    try:
        res = subprocess.run(["bash", "./tempscr.sh"], check=True)
    except subprocess.CalledProcessError:
        print("FAIL: Error")
        sys.exit(1)
    print()
    printmd("---\n# Success!")
elif args.command == "moo":
    print("Mooooo")
    if args.farts:
        print(r'''                      ,     ,
                ___('-&&&-')__
                '.__./     \__.'
    _     _     _ .-'  6  6 \
/` `--'( ('--` `\         |
/        ) )      \ \ _   _|
|        ( (        | (0_._0)
|         ) )       |/ '---'
|        ( (        |\_
|         ) )       |( \,
\       ((`       / )__/
|     /:))\     |   d
|    /:((::\    |
|   |:::):::|   |
/   \::&&:::/   \
\   /;U&::U;\   /
    | | | u:u | | |
    | | \     / | |
jgs | | _|   | _| |
    / \""`   `""/ \
| __|       | __|
`"""`       `"""`
        ''')
    else:
        # A
        print(r''' _______________________
< Have you mooed today? >
 -----------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
        ''')