import os
import shutil
import sys
from pathlib import Path


def browse_tree(path, home_directory):
    for root, directories, filenames in os.walk(path):
        for filename in filenames:
            src = os.path.abspath(os.path.join(root, filename))
            software_name = path + os.path.join(root, filename)
            dst = os.path.join(home_directory, src.removeprefix(os.path.abspath(path) + "/"))

            yield {"src": src, "software_name": software_name, "dst": dst}


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

        print("   ", msg, filename["software_name"], "->", filename["dst"])


def main():
    CURRENT_FOLDER = os.getcwd()
    softwares = [x for x in os.listdir(CURRENT_FOLDER) if os.path.isdir(os.path.join(CURRENT_FOLDER, x))]

    folder = sys.argv[1].removesuffix("/")
    dry_run = False

    if folder in softwares and os.path.isdir(folder):
        print(folder)
        files = browse_tree(folder, Path().home())
        create_symlinks(files, dry_run)


if __name__ == "__main__":
    main()
