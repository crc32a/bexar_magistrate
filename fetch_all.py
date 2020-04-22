#!/usr/bin/env python

from lxml import etree
import traceback
import requests
import json
import time
import sys
import os

def printf(format,*args): sys.stdout.write(format%args)

intake_cols = ["name", "sid", "dob", "race", "sex", "arrest_time",
               "intake_time","magistration_time", "disposition",
               "magistration_release_time", "comments" ]

charge_cols = [ "mag_num", "offense_desc", "offense_type", "boond_amount" ]

recoveryParser = etree.XMLParser(recover=True)


def usage(prog):
    printf("usage is %s <arrests_file.json>\n", prog)
    printf("\n")
    printf("Fetch all recent arrests\n")

def load_json(file_name):
    fp = open(os.path.expanduser(file_name),"r")
    data = fp.read()
    fp.close()
    return json.loads(data)


def save_json(file_name, obj):
    fp = open(os.path.expanduser(file_name), "w")
    fp.write(json.dumps(obj, indent=4))
    fp.close()
    

def main(args):
    if len(args)<2:
        usage(args[0])
        sys.exit()
    json_file = args[1]
    arrests = get_arrests_main()
    save_json(json_file, arrests)

def get_arrests_main():
    obj = {"arrests":[],"failed":[]}
    arrests = get_recent_arrests()
    n = len(arrests)
    for(i,  arrest) in enumerate(arrests):
        name = arrest["name"]
        dob = arrest["dob"]
        sid = arrest["sid"]
        printf("loading %i of %i name=%s", i, n, name)
        printf(" dob=%s sid=%s\n", dob, sid)
        intake_num = arrest["intakeNum"]
        try:
            html = get_intake_html(intake_num)
            root = parse_html(html)
            intake = parse_intake(root)
            charges = parse_charges(root)
            intake["intake_num"] = intake_num
            intake["charges"] = charges
            for charge in intake["charges"]:
                printf("  %s:", charge["offense_desc"])
                printf("%s\n", charge["offense_type"])
            printf("\n")
            sys.stdout.flush()
            obj["arrests"].append(intake)
        except:
            traceback.print_exc()
            obj["failed"].append(intake_num)
            continue
    return obj

def get_recent_arrests():
    url = "https://centralmagistrate.bexar.org/Home/GetRecentArrests"
    headers = {"accept":"application/json"}
    r = requests.get(url,headers=headers)
    return json.loads(r.text)['data']


def get_intake_html(intake_num):
    url = "https://centralmagistrate.bexar.org/Home/Details/%s"
    headers = {"accept":"text/html"}
    r = requests.get(url%intake_num,headers=headers)
    return r.text


def parse_html(html):
    root = etree.fromstring(html, parser=recoveryParser)
    return root

def parse_intake(root):
    p_elements = root.xpath(".//div[@class='column2']/p")
    n = len(p_elements)
    out = {}
    if n != 11:
        printf("intake has %s p elements\n", n)
        return None
    for (i, col) in enumerate(intake_cols):
        out[col] = p_elements[i].text.strip()
    return out

def parse_charges(root):
    offence_tr = root.xpath(".//table[@id='bcitDataTable']/tbody/tr")
    charges = []
    for offense in offence_tr:
        tds = offense.xpath(".//td")
        n = len(tds)
        if n != 4:
            printf("charge has %d colums\n", n)
            continue
        charge = {}
        for (i, col) in enumerate(charge_cols):
            charge[col] = tds[i].text
        charges.append(charge)
    return charges
    

if __name__ == "__main__":
    main(sys.argv)
