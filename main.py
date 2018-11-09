#!/bin/env python3

import argparse
import os
import shutil

from sys import argv
from random import choice

# Setup parser
parser = argparse.ArgumentParser(description="Let's play hide hide&seek.")
parser.add_argument('--hide', action="store_true", help="hide somewhere in the system")
parser.add_argument('--nohint', action="store_true", help="do not leave hint file behind, be aware that finding this thing without hint can be tricky")
parser.add_argument('--directory', help="i'll hide somewhere in this directory")
parser.add_argument('-v', '--verbose', action='count', default=0, help="tell me stuff")

args = parser.parse_args()

if not args.hide:
    print("You found me. Huray!")
else:
    filename = os.path.basename(argv[0])
    while True:
        if args.verbose >= 2:
            print("Hiding.")
        path = "."
        if argv.directory:
            path = argv.directory
        try:
            while True:
                options = list(filter(lambda x: os.path.isdir(os.path.join(path, x)), os.listdir(path))) + [None]

                if args.verbose >= 4:
                    print("Options, options. What to chose from %s?" % str(options))

                chosen = choice(options)

                if chosen is None:
                    print("'%s' looks good I'll stay here." % path)
                    while filename in os.listdir(path):
                        print("There alreasy is a weird file names named '%s' so I gotta name myself 'hideandseek_%s'" % (filename, filename))
                        filename  = "hideandseek_%s" % filename
                    shutil.move(argv[0], os.path.join(path, filename))
                    if not args.nohint:
                        with open(argv[0], "w") as file:
                            file.write("I've hiddden in '%s'\n" % path)
                    break

                else:
                    if args.verbose >= 3:
                        print("I chose " + chosen)
                    path = os.path.join(path, chosen)

            if args.verbose >= 1:
                print("I've hidden here: " + path)

            break
        except PermissionError:
            print("Ups I cannot hide in '%s' due to permission issues." % path)
            continue
                
