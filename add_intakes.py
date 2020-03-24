#!/usr/bin/env python

import fetch_all as fa
import json
import sys
import os

def usage(prog):
    fa.printf("%s <inmates9_json_file> <collection_json_file>\n", prog)

def main(*args):
    prog = os.path.basename(args[0])
    if len(args)<3:
        usage(prog)
        sys.exit()
    arrests_file = os.path.expanduser(args[1])
    collected_arrests_file = os.path.expanduser(args[2])
    if not os.path.isfile(os.path.expanduser(collected_arrests_file)):
        fa.save_json(collected_arrests_file, {})
    collected_arrests = fa.load_json(collected_arrests_file)
    curr_arrests = fa.load_json(arrests_file)['arrests']
    collected_ids = set(collected_arrests.keys())
    for arrest in curr_arrests:
        if arrest['intake_num'] in collected_ids:
            fa.printf("UPDATE inmate %s intake %s found\n", arrest['name'],
                      arrest['intake_num'])
        else:
            fa.printf("NEW inmate %s intake %s found\n", arrest['name'],
                      arrest['intake_num'])
        collected_arrests[arrest['intake_num']] = arrest
    fa.save_json(collected_arrests_file, collected_arrests)

if __name__ == "__main__":
    main(*sys.argv)
