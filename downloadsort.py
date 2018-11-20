#!/usr/bin/env python3

import glob
from shutil import move
import os
import sys
import argparse

if __name__ == "__main__":
        # Arg Parsing
        parser = argparse.ArgumentParser(description="Description: Move files in a given folder to folders matching their extension")

        # Required arguments
        required = parser.add_argument_group("Required Arguments")
        required.add_argument("-p", "--path", help="Path to folder", nargs='?', required=True)
        args = parser.parse_known_args()[0] # Parse known args

        path = args.path.rstrip(os.sep) # Strip last / (if there is one)
        for file in glob.glob("%s/%s" % (path, "*.*")):
            if "." in file: # Does file have an extension?
                ext = file.split(".")[-1].lower()
                filename = file.split(os.sep)[-1]
                try:
                    # Move files to given folder if it exists
                    move(file, "%s/%s/%s" % (path, ext, filename))
                except Exception as e:
                    # Folder doesn't exist, so create it then move files
                    os.mkdir(os.path.dirname("%s/%s/" % (path, ext)))
                    move(file, "%s/%s/%s" % (path, ext, filename))
