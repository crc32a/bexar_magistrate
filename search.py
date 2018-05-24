#!/usr/bin/env python2

import scrape_magistrate as sm
import datetime
import sys
import re

months = {'January':1, 'February':2, 'March':3, 
           'April':4, 'May':5, 'June':6, 
           'July':7,  'August':8, 'September':9, 
           'October':10, 'November':11, 'December':12}

date_restr="(\S*)\s([0-9]{,2}),([0-9]{,4}) at ([0-9]{,2}):([0-9]{,2})"
date_re = re.compile(date_restr, re.IGNORECASE)

def getdate(date_str):
    default_dt = datetime.datetime(1970,1,1,0,0)
    m = date_re.match(date_str)
    if not m:
        return default_dr
    year = int(m.group(3))
    if m.group(1) not in months:
        return default_dt
    month = months[m.group(1)]
    day = int(m.group(2))
    hour = int(m.group(4))
    min = int(m.group(5))
    dt = datetime.datetime(year, month, day, hour)
    return dt

def main(*args):
    if len(args)<3:
        sm.printf("usage is %s <collection_jsonfile> <charge>\n",args[0])
        sm.printf("\n")
        sm.printf("search the inmates for the given charge\n")
        sm.printf("\n")
        sys.exit()

    collections_file = args[1]
    charge_str = args[2]

    charge_re = re.compile(".*" + charge_str + ".*", re.IGNORECASE)
    all = sm.load_json("all.json")

    arrest_order = []

    for(intake_num, inmate) in all.items():
        arrest = inmate['Arrest Date/Time']
        dt = getdate(arrest)
        arrest_order.append( (dt, intake_num, inmate))
    arrest_order.sort()

    for (dt, intake_num, inmate) in arrest_order:
        name = inmate['Name']
        age = sm.inmate_age(inmate)
        sex = inmate['Sex']
        race = inmate['Race']
        arrest = inmate['Arrest Date/Time']
        sid = inmate['SID']
        release = inmate['CMAG Release Date/Time']

        hit = False
        for charge in inmate['charges']:
            m = charge_re.match(charge['offense'])
            if m:
                hit = True
                break
        if hit:
            sm.printf("%s %s %s %s %s %s arrest=\"%s\" release=\"%s\"\n", 
                      intake_num, name, age, race, sex, sid, arrest, release)
            sm.printf("==================================\n")
            for charge in inmate['charges']:
                sm.printf("%s %s %s\n", charge['offense'], charge['type'],
                          charge['bond'])
            sm.printf("\n")

if __name__ == "__main__":
    main(*sys.argv)
