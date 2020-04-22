#!/usr/bin/env python

from fetch_all import load_json, printf
import sys
import os

def main(args):
    all = load_json("all.json")
    counts = {}
    for (intake_num, arrest) in all.items():
        printf("%s: %s\n", intake_num, arrest)

if __name__ == "__main__":
    main(sys.argv)
