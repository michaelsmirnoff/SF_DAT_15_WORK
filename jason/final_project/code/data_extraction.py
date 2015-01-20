# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 12:24:37 2015

@author: Jason
"""

import os
import re
import datetime
from bs4 import BeautifulSoup  

source_path = "/Users/Jason/Documents/DataScience/DAT4-students/jason/final_project/data/USPTO_zipfiles/"
destination_path = "/Users/Jason/Documents/DataScience/DAT4-students/jason/final_project/data"

source = os.listdir(source_path)[1:]
source = [source_path + x for x in source]

test = source[0]

with open(source[0], 'rU') as g:
    btest = BeautifulSoup(g, 'xml')

btest.prettify

def _get_date(filename, dateformat='ipg%y%m%d.xml'):
    """
    Given a [filename], returns the expanded year.
    The optional [dateformat] argument allows for different file formats
    """
    filename = re.search(r'ip[ag]\d{6}', filename) or re.search(r'p[ag]\d{6}', filename)
    if not filename:
        return 'default'
    filename = filename.group() + '.xml'
    dateobj = datetime.datetime.strptime(filename.replace('ipa', 'ipg').replace('pa', 'ipg'), dateformat)
    return int(dateobj.strftime('%Y%m%d'))  # returns YYYYMMDD

endtag_regex = re.compile('^<!DOCTYPE (.*) SYSTEM')
endtag = ''
with open(test, 'r') as f:
    doc = ''  # (re)initialize current XML doc to empty string
    for line in f:
        doc += line
        endtag = endtag_regex.findall(line) if not endtag else endtag
        if not endtag:
            continue
        terminate = re.compile('^</{0}>'.format(endtag[0]))
        if terminate.findall(line):
            yield (_get_date(test), doc)
            endtag = ''
            doc = ''