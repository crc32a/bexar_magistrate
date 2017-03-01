#!/usr/bin/env python

import scrape_magistrate as sm
import operator
import sys
import re



def main(*args):
    if len(args)<2:
        sm.printf("usage is %s <collection_jsonfile>\n",args[0])
        sm.printf("\n")
        sm.printf("count inmate charges and list rankings\n")
        sm.printf("\n")
        sys.exit()

    collections_file = args[1]
    all = sm.load_json("all.json")
    info = {}
    for (intake_num, inmate) in all.items():
        sid = inmate['SID']
        name = inmate['Name']
        age = sm.inmate_age(inmate)
        sex = inmate['Sex']
        race = inmate['Race']
        arrest = inmate['Arrest Date/Time']
        release = inmate['CMAG Release Date/Time']
        if sid not in info:
            info[sid] = {"name": name, "age": age, "race": race, "sid": sid,
                         "charges": 0, "sex": sex}
        info[sid]['charges'] += len(inmate['charges'])
    counts = [(val) for (val) in info.values()]
    counts.sort(key=operator.itemgetter("charges"))
    for info  in counts:
        sm.printf("charges %3d sid=%s name=%s age=%s sex=%s race=%s\n",
        info['charges'], info['sid'], info['name'], info['age'], info['sex'],
        info['race'])

if __name__ == "__main__":
    main(*sys.argv)
