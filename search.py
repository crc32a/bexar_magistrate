#!/usr/bin/env python

import scrape_magistrate as sm
import sys
import re



def main(*args):
    if len(args)<3:
        sm.printf("usage is %s collection_jsonfile charge\n",args[0])
        sm.printf("\n")
        sm.printf("search the inmates for the given charge\n")
        sm.printf("\n")
        sys.exit()

    collections_file = args[1]
    charge_str = args[2]

    charge_re = re.compile(".*" + charge_str + ".*", re.IGNORECASE)
    all = sm.load_json("all.json")

    for (intake_num, inmate) in all.items():
        name = inmate['Name']
        age = sm.inmate_age(inmate)
        sex = inmate['Sex']
        race = inmate['Race']
        arrest = inmate['Arrest Date/Time']
        release = inmate['CMAG Release Date/Time']

        hit = False
        for charge in inmate['charges']:
            m = charge_re.match(charge['offense'])
            if m:
                hit = True
                break
        if hit:
            sm.printf("%s %s %s %s %s arrest=\"%s\" release=\"%s\"\n", 
                      intake_num, name, age, race, sex, arrest, release)
            sm.printf("==================================\n")
            for charge in inmate['charges']:
                sm.printf("%s %s %s\n", charge['offense'], charge['type'],
                          charge['bond'])
            sm.printf("\n")

if __name__ == "__main__":
    main(*sys.argv)
