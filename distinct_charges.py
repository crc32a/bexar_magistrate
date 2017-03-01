#!/usr/bin/env 

import json
import sys
import os

def printf(format,*args): sys.stdout.write(format%args)

def load_json(pathIn):
    return json.loads(open(os.path.expanduser(pathIn),"r").read())

intakes = load_json("all.json")

charges = set([])
for (intake_num,intake) in intakes.items():
    for charge in intake['charges']:
        charges.add(charge['offense'])

distinct_charges = sorted(list(charges))

