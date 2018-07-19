#!/usr/bin/env python2

import json
import sys
import os

def printf(format,*args): sys.stdout.write(format%args)

def load_json(pathIn):
    return json.loads(open(os.path.expanduser(pathIn),"r").read())

intakes = load_json("all.json")

l = 0
charges = set([])
for (intake_num,intake) in intakes.items():
    for charge in intake['charges']:
        charges.add((charge['type'], charge['offense']))
        charge_len  = len(charge['offense'])
        if charge_len > l:
            l = charge_len

distinct_charges = sorted(list(charges))
for (charge_type,offense) in distinct_charges:
    print charge_type, offense

