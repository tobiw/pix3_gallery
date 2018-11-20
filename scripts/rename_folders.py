import os
import os.path
import sys


def rename(basedir, folder_name):
    abs_from = os.path.join(basedir, folder_name)
    abs_to = os.path.join(basedir, folder_name.replace(' ', '_'))
    os.rename(abs_from, abs_to)


def rename_subfolders(basedir, recurse=True):
    for d in os.listdir(basedir):
        if os.path.isdir(os.path.join(basedir, d)):
            rename_subfolders(os.path.join(basedir, d))
            rename(basedir, d)


def main(arg):
    rename_subfolders(arg)


if __name__ == '__main__':
    main(sys.argv[1])
