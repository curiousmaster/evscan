#! /usr/bin/python
# ======================================================================
# NAME
#   evscan - evasive scan
#
# SYNTAX
#   evscan.py [-h] [-f FILE] [-c COMMAND] [-m MAX] [-d DELAY]
#
# DESCRIPTION
#   Generate batch file with randomized order of ip addresses defined in FILE
#
#     -h, --help            show this help message and exit
#     -f FILE, --file FILE  Specify input file
#     -c COMMAND, --command COMMAND
#                           Specify command
#     -m MAX, --max MAX     Specify max number of IPs in batch
#     -d DELAY, --delay DELAY
#                           Specify delay between batches
#     -r, --random          Randomize ip list
#     -p, --parallell       scan in parallell
#
# SEE ALSE
#   nmap(1)
#
# AUTHOR
#   Sep 28, 2022 / Stefan Benediktsson
#
# VERSION
#   v1.0    - Initial Version
# 
# ======================================================================

import sys
import csv
import sqlite3
import random
import argparse
import ipaddress
import operator
import itertools
import collections


from os.path import expanduser

# ======================================================================
# Setup Initial Variables
# ======================================================================
COMMAND = "nmap"
FILE = ""
ARGS = ""
MAX = 10
DELAY=5


# ======================================================================
# Initiate the SQLITE3 database
# ======================================================================
con = sqlite3.connect(":memory:")
cur = con.cursor()



def parseArgs():
    # =================================================
    # NAME
    #   parseArgs()
    #
    # DESCRIPTION
    #   Parse command line options
    # =================================================
    global COMMAND
    global FILE
    global ARGS
    global MAX
    global DELAY

    ap = argparse.ArgumentParser(description="evscan")
    ap.add_argument("-f", "--file", required=True, help="Specify input file")
    ap.add_argument("-c", "--command", required=False, help="Specify command")
    ap.add_argument("-m", "--max", required=False, help="Specify max number of IPs in batch")
    ap.add_argument("-d", "--delay", required=False, help="Specify delay between batches")
    ap.add_argument("-r", "--random", required=False, action="store_true",  help="Randomize ip list")
    ap.add_argument("-p", "--parallell", required=False, action="store_true", help="scan in parallell")

    ARGS = vars(ap.parse_args())

    if ARGS['file']:
        FILE = ARGS['file']

    if ARGS['command']:
        COMMAND = ARGS['command']

    if ARGS['max']:
        MAX = int(ARGS['max'])

    if ARGS['delay']:
        DELAY = ARGS['delay']

    return ARGS


def readList(file):
# --------------------------------------------------
# readList()
#   Read a list of IP addresses
# --------------------------------------------------
    with open(file) as fp:
        data = fp.read().splitlines()

    return data


def randomizeList(list):
# --------------------------------------------------
# randomizeList()()
#   Randomize order of list objects
# --------------------------------------------------
    random.shuffle(list)
    return list


def main():
# --------------------------------------------------
# main()
# --------------------------------------------------
    global COMMAND
    global DELAY
    global MAX

    parseArgs();

    #IPADDRESSES = loadFile(FILE,",")
    IPADDRESSES = readList(FILE)

    if ARGS['random']:
        IPADDRESSES = randomizeList(IPADDRESSES)


    i = 0
    command = COMMAND

    for ip in IPADDRESSES:

        if ARGS['parallell']:
            command = command + " " + ip
        else:
            command = COMMAND + " " + ip
            print(command)


        if i%MAX == 1:
            if ARGS['parallell']:
                print(command)

            command = COMMAND
            print("sleep {}".format(DELAY))
        i = i+1



# --------------------------------------------------
# Run main()
# --------------------------------------------------
if __name__ == "__main__":
    main()
