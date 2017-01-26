#!/usr/bin/env python

import scrape_magistrate
import time
import sys
import os

def retry_failed(inmates):
    failed_fetches = inmates['failed_fetch'][:]
    inmates['failed_fetch'] = []
    for(url, name) in failed_fetches:
        try:
            inmate_text = scrape_magistrate.get_inmate(url)
            inmate = scrape_magistrate.parse_inmate(inmate_text)
            time.sleep(1.0)
            inmates['inmates'].append(inmate)
        except:
            printf("Failed to fetch data for %s %s\n", name, sys.exc_info())
            inmates['failed_fetch'].append([url,name])
    return inmates

if __name__ == "__main__":
    #inmate_json_file = sys.argv[1]
    inmate_json_file = "/home/crc/workspace/curr/lab/cmag/inmates_20160125.json"
    inmates = scrape_magistrate.load_json(os.path.expanduser(inmate_json_file))
    inmates = retry_failed(inmates)
    scrape_magistrate.save_json(os.path.expanduser(inmate_json_file), inmates)
