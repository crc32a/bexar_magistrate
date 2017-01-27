#!/usr/bin/env python

import scrape_magistrate as sm
import sys
import os

def usage(prog):
    sm.printf("%s <inmates_json_file> <collection_json_file>\n", prog)

def main(*args):
    prog = os.path.basename(args[0])
    if len(args)<3:
        usage(prog)
        sys.exit()
    inmate_file = os.path.expanduser(args[1])
    collected_inmate_file = os.path.expanduser(args[2])
    if not os.path.isfile(os.path.expanduser(collected_inmate_file)):
        sm.save_json(collected_inmate_file, {})
    collected_inmates = sm.load_json(collected_inmate_file)
    curr_inmates = sm.load_json(inmate_file)['inmates']
    collected_ids = set(collected_inmates.keys())
    for inmate in curr_inmates:
        if inmate['intake_num'] in collected_ids:
            continue
        sm.printf("New inmate %s intake %s found\n", inmate['Name'],
                  inmate['intake_num'])
        collected_inmates[inmate['intake_num']] = inmate
    sm.save_json(collected_inmate_file, collected_inmates)

if __name__ == "__main__":
    main(*sys.argv)
