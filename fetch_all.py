#!/usr/bin/env python

from lxml import etree
import traceback
import requests
import json
import time
import sys

def printf(format,*args): sys.stdout.write(format%args)

intake_cols = ["name", "sid", "dob", "race", "sex", "arrest_time",
               "intake_time","magistration_time", "disposition",
               "magistration_release_time", "comments" ]

charge_cols = [ "mag_num", "offense_desc", "offense_type", "boond_amount" ]

recoveryParser = etree.XMLParser(recover=True)


def main(args):
    json_file = args[1]

def get_arrests_main():
    obj = {"arrests":[],"failed":[]}
    arrests = get_recent_arrests()
    n = len(arrests)
    for(i,  arrest) in enumerate(arrests):
        name = arrest['name']
        printf("loading %i of %i name=%s\n", i, n, name)
        intake_num = arrest["intakeNum"]
        try:
            html = get_intake_html(intake_num)
            root = parse_html(html)
            intake = parse_intake(root)
            charges = parse_charges(root)
            intake['intake_num'] = intake_num
            intake["charges"] = charges
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
