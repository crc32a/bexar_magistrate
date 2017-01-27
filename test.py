#!/usr/bin/env python

import scrape_magistrate as sm
import re

prost_re = re.compile(".*",re.IGNORECASE)

all = sm.load_json("all.json")



for (intake_num, inmate) in all.items():
    name = inmate['Name']
    age = sm.inmate_age(inmate)
    sex = inmate['Sex']
    race = inmate['Race']

    hit = False
    for charge in inmate['charges']:
        m = prost_re.match(charge['offense'])
        if m:
            hit = True
            break
    if hit:
        sm.printf("%s %s %s %s\n", name, age, race, sex)
        sm.printf("==================================\n")
        for charge in inmate['charges']:
            sm.printf("%s %s %s\n", charge['offense'], charge['type'],
                      charge['bond'])
        
