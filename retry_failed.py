#!/usr/bin/env python2

import scrape_magistrate as sm
import time
import sys
import os

if __name__ == "__main__":
    inmate_json_file = sys.argv[1]
    inmates = sm.load_json(os.path.expanduser(inmate_json_file))
    inmates = sm.retry_failed(inmates)
    sm.save_json(inmate_json_file, inmates)
