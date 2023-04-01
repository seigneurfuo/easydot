#!/bin/env python3

import argparse
import os
import sys
from pathlib import Path


class Messages:
    OK = "Ok"
    DST_FILE_NOT_EXISTS = "Destination inexistante"
    DST_EXIST_BUT_NO_LINK = "Destination existe mais n'est pas un lien."
    SRC_FOLDER_NOT_FOUND = "Le dossier \"{}\" n'existe pas"

#https://stackoverflow.com/a/287944
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_softwares(path):
    ret_list = []
    excludes = ("__pycache__")
    for folder in os.listdir(path):
        if os.path.isdir(os.path.join(path, folder)) and not folder.startswith(".") and folder not in excludes:
            ret_list.append(folder)

    return sorted(ret_list)


def get_symbolics_links(path):
    ret = []

    softwares = get_softwares(path)
    for software in softwares:
        software_path = os.path.join(path, software)

        for link in browse_software_files(software_path):
            ret.append(link)

    return ret


def browse_software_files(path, home_directory=Path().home()):
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


def create_symlinks(files, args):
    for filename in files:
        dst_folder = os.path.dirname(filename["dst"])

        if args.force_delete and os.path.isfile(filename["dst"]):
            if not args.dry:
                os.remove(filename["dst"])

            msg = "{}[DELETE] {}{}".format(bcolors.WARNING, bcolors.ENDC, filename["dst"])
            print(msg)

        if not os.path.isdir(dst_folder):
            if not args.dry:
                os.makedirs(dst_folder)

            msg = "{}[CREATEFOLDER] {}{}".format(bcolors.OKGREEN, bcolors.ENDC, dst_folder)
            print(msg)

        # Création du lien symbolique
        if not os.path.isfile(filename["dst"]):
            if not args.dry:
                os.symlink(filename["src"], filename["dst"])

            msg = "{}[+SYMBLINK]{}".format(bcolors.OKGREEN, bcolors.ENDC)

        # elif os.path.islink(filename["dst"]):
        #     msg = "{}[ERROR: SYMBLINK EXISTS]{}".format(bcolors.FAIL, bcolors.ENDC)
        #     # Demander le remplacement ?
        else:
            msg = "{}[ERROR: FILE EXISTS]{}".format(bcolors.FAIL, bcolors.ENDC)

        print(msg, filename["src"], "->", filename["dst"], "\n")


def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--list", required=False, action="store_true")
    argument_parser.add_argument("--dry", required=False, action="store_true")
    argument_parser.add_argument("--name", type=str, help="Software name")
    argument_parser.add_argument("--force-delete", required=False, action="store_true")
    args = argument_parser.parse_args()

    #current_folder = os.getcwd()
    current_folder = os.path.join(Path.home(), "Dotfiles")

    softwares = get_softwares(current_folder)

    if args.list:
        for software in softwares:
            print("    - {}".format(software))

    if args.name:
        software_name = args.name.strip().removesuffix("/")
        folderpath = os.path.join(current_folder, software_name)

        if software_name in softwares and os.path.isdir(folderpath):
             files = browse_software_files(folderpath)
             create_symlinks(files, args)
        else:
            msg = Messages.SRC_FOLDER_NOT_FOUND.format(folderpath)
            print(msg)

if __name__ == "__main__":
    main()
