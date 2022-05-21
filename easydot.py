import os
import shutil
import sys
from pathlib import Path

class ErrorMessages:
    DST_FILE_NOT_EXISTS = "Destination inexistante"
    OK = "Ok"


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
            
            if not os.path.islink(dst):
                msg = ErrorMessages.DST_FILE_NOT_EXISTS
            else:
                msg = ErrorMessages.OK

            yield {"src": src, "dst": dst, "msg": msg, "software_name": None}


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
            msg = "[SYMBLINK EXISTS]"
            # Demander le remplacement ?

        else:
            msg = "[FILE EXISTS]"

        print("   ", msg, filename["src"], "->", filename["dst"])


def main():
    CURRENT_FOLDER = os.getcwd()
    softwares = get_softwares(CURRENT_FOLDER)

    folder = sys.argv[1].removesuffix("/")
    dry_run = False

    if folder in softwares and os.path.isdir(folder):
        print(folder)
        files = browse_tree(folder)
        create_symlinks(files, dry_run)


if __name__ == "__main__":
    main()
