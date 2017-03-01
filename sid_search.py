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
    wanted_sid = args[2]
    all = sm.load_json("all.json")
    displayed_name = False
    all_sorted = sorted([(int(k), v) for (k,v) in all.items()])
    for (intake_num, inmate) in all_sorted:
        sid = inmate['SID']
        if sid != wanted_sid:
            continue
        if not displayed_name:
            displayed_name = True
            name = inmate['Name']
            age = sm.inmate_age(inmate)
            sex = inmate['Sex']
            race = inmate['Race']
            sm.printf("name = %s age = %s sex= %s race = %s\n", 
                      name, age, sex, race)
        release = inmate['CMAG Release Date/Time']
        arrest = inmate['Arrest Date/Time']
        charges = inmate['charges']
        sm.printf("    Arrest = %s Release = %s intake = %s\n", arrest, 
                  release, intake_num)
        sm.printf("    charges\n")
        for charge in charges:
            offense = charge['offense']
            otype = charge['type']
            bond = charge['bond']
            sm.printf("        %s %s %s\n", offense, otype, bond)

if __name__ == "__main__":
    main(*sys.argv)
