import argparse

#!/bin/env python3
import os
import sys
from pathlib import Path


class Messages:
    OK = "Ok"
    DST_FILE_NOT_EXISTS = "Destination inexistante"
    DST_EXIST_BUT_NO_LINK = "Destination existe mais n'est pas un lien"


def get_softwares(path):
    return sorted([folder for folder in os.listdir(path) if
                   os.path.isdir(os.path.join(path, folder)) and not folder.startswith(".")])


def get_symbolics_links(path):
    ret = []

    softwares = get_softwares(path)
    for software in softwares:
        software_path = os.path.join(path, software)

        for link in browse_tree(software_path):
            ret.append(link)

    return ret


def browse_tree(path, home_directory=Path().home()):
    for root, directories, filenames in os.walk(path):
        for filename in filenames:
            src = os.path.abspath(os.path.join(root, filename))
            dst = os.path.join(home_directory, src.removeprefix(os.path.abspath(path) + "/"))

            src_short = src.removeprefix(os.path.abspath(path) + "/")
            dst_short = dst.removeprefix(os.path.abspath(home_directory) + "/")

            if os.path.isfile(dst) and not os.path.islink(dst):
                msg = Messages.DST_EXIST_BUT_NO_LINK

            elif not os.path.isfile(dst) and not os.path.islink(dst):
                msg = Messages.DST_FILE_NOT_EXISTS
            else:
                msg = Messages.OK

            yield {"src": src, "dst": dst, "src_short": src_short, "dst_short": dst_short, "msg": msg, "software_name": None}


def create_symlinks(files, dry_run):
    for filename in files:
        dst_folder = os.path.dirname(filename["dst"])
        if not os.path.isdir(dst_folder):
            if not dry_run:
                os.makedirs(dst_folder)

            print("    [CREATEFOLDER]", dst_folder)

        # Création du lien symbolique
        if not os.path.isfile(filename["dst"]):
            if not dry_run:
                os.symlink(filename["src"], filename["dst"])

            msg = "[+SYMBLINK]"

        elif os.path.islink(filename["dst"]):
            msg = "[ERROR: SYMBLINK EXISTS]"
            # Demander le remplacement ?

        else:
            msg = "[ERROR: FILE EXISTS]"

        print("   ", msg, filename["src"], "->", filename["dst"])


def main():
    current_folder = os.getcwd()
    current_folder = os.path.join(Path.home(), "Dotfiles")


    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--list", required=False)
    args = argument_parser.parse_args()

    softwares = get_softwares(current_folder)

    if args.list:
        for software in softwares:
            print("    - {}".format(software))


    # if len(sys.argv) == 2:
    #     folder = sys.argv[1].removesuffix("/")
    #     dry_run = False
    #
    #     if folder in softwares and os.path.isdir(folder):
    #         print(folder)
    #         files = browse_tree(folder)
    #         create_symlinks(files, dry_run)


if __name__ == "__main__":
    main()
