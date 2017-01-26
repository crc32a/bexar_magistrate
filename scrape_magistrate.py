#!/usr/bin/env python

import xml.etree.ElementTree as ET
import traceback
import requests
import time
import json
import sys
import os
import re

mag_url = "http://apps.bexar.org/CMAGSearchList/"
start_table_re = re.compile(".*<table.*")
stop_table_re = re.compile(".*</table>.*")

def printf(format,*args): sys.stdout.write(format%args)

def fprintf(fp,format,*args): fp.write(format%args)

def load_json(pathIn):
    return json.loads(open(os.path.expanduser(pathIn),"r").read())

def save_json(pathOut,obj):
    open(os.path.expanduser(pathOut),"w").write(json.dumps(obj, indent=2))


def get_inmates():
    req = requests.get(mag_url)
    lines = req.text.split("\n")
    inmates = []
    for line in lines:
        (link, name, intake_num) = find_link_and_name(line)
        if link and name:
            inmates.append([link.strip(), name.strip(),intake_num.strip()])
    return inmates


def find_link_and_name(line):
    search_str = "ListDetails.aspx?detail="
    search_len = len(search_str)
    n = line.find(search_str)
    if n < 0:
        return (None, None, None)
    link = [mag_url]
    link.append(search_str)
    i = n + search_len
    digit_list = []
    while line[i].isdigit():
        digit = line[i]
        link.append(digit)
        digit_list.append(digit)
        i += 1
    intake_num = "".join(digit_list)
    url = "".join(link)
    i += 2
    letters = []
    while line[i] != "<":
        letters.append(line[i])
        i += 1
    name = "".join(letters)
    return (url, name, intake_num)

def test_re(re_str,line):
    date_re = re.compile(re_str)
    m = date_re.match(line)
    if m:
        printf("\n")
        i = 1
        for g in m.groups():
            printf("group(%i)=%s\n",i,g)
            i += 1
        return m
    return False

def get_inmate(url):
    req = requests.get(url)
    inmate_text = req.text
    return inmate_text

def get_all_inmate_data():
    failed = []
    inmates = []
    inmate_headers= get_inmates()
    n_inmates = len(inmate_headers)
    printf("%d inmates in magistrate\n", n_inmates)
    i = 0
    for (url, name, intake_num) in inmate_headers:
        if url is None or name is None:
            continue
        printf("Fetching inmate %s %d of %d\n", name, i, n_inmates)
        i += 1
        try:
            inmate_text = get_inmate(url)
            inmate = parse_inmate(inmate_text)
            inmate['intake_num'] = intake_num
            inmates.append(inmate)
            time.sleep(1.0)
        except:
            printf("Failed to fetch data for %s %s\n", name, sys.exc_info())
            failed.append([url,name, intake_num])
    return {"inmates": inmates,"failed_fetch": failed}

def parse_inmate(inmate_text):
    tables = find_tables(inmate_text)
    inmate = parse_inmate_data(tables[0])
    charges = parse_inmate_charges(tables[1])
    inmate['charges'] = charges
    return inmate

def retry_failed(inmates):
    failed_fetches = inmates['failed_fetch'][:]
    inmates['failed_fetch'] = []
    n_failures = len(failed_fetches)
    printf("fetching %d inmates\n", n_failures)
    i = 0
    for(url, name, intake_num) in failed_fetches:
        try:
            printf("Fetching inmate %s intake %s %d of %d\n", name,
                   intake_num, i, n_failures)
            i += 1
            inmate_text = get_inmate(url)
            inmate = parse_inmate(inmate_text)
            inmate['intake_num'] = intake_num
            time.sleep(2.0)
            inmates['inmates'].append(inmate)
        except:
            printf("Failed to fetch data for %s %s\n", name, sys.exc_info())
            inmates['failed_fetch'].append([url,name])
    return inmates



def parse_inmate_data(inmate_table):
    inmate_data = {}
    table = ET.fromstring(inmate_table)
    trs = table.findall(".//tr")
    for tr in trs:
        tds = tr.findall(".//td")
        if len(tds) >=2:
            col = tds[0].text.strip().replace(":","")
            val = tds[1].getchildren()[0].text
            if val is not None:
                inmate_data[col] = val.strip()
            else:
                inmate_data[col] = ""
    return inmate_data

def parse_inmate_charges(charges_table):
    charges = []
    table = ET.fromstring(charges_table)
    trs = table.findall(".//tr")
    for tr in trs[1:]:
        tds = tr.findall(".//td//font")
        charge = {"magnum": tds[0].text.strip(),
                  "offense": tds[1].text.strip(),
                  "type": tds[2].text.strip(),
                  "bond": tds[3].text.strip()}
        charges.append(charge)
    return charges

def find_tables(text):
    in_table = False
    tables = []
    curr_table = []
    for line in text.split("\n"):
        if in_table:
            curr_table.append(line)
            m = stop_table_re.match(line)
            if m:
                in_table = False
                tables.append("".join(curr_table))
                curr_table = []
        else:
            m = start_table_re.match(line)
            if m:
                in_table = True
                curr_table.append(line)
    return tables



if __name__ == "__main__":
    inmate_json_file = sys.argv[1]
    inmates = get_all_inmate_data()
    save_json(os.path.expanduser(inmate_json_file), inmates)
