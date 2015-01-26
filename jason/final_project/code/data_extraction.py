# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 12:24:37 2015

@author: Jason
"""

import os
import csv
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

xml_source_path = "../data/USPTO_zipfiles/"
xml_destination_path = "/Users/Jason/Documents/DataScience/DAT4-students/jason/final_project/data/formatted_xmls/"
csv_destination_path = "/Users/Jason/Documents/DataScience/DAT4-students/jason/final_project/data/csvs/"

xml_source_list = [xml_source_path + x for x in os.listdir(xml_source_path)[1:]]
csv_source_list = [xml_destination_path + x for x in os.listdir(xml_destination_path)[1:]]

xmltest = "/Users/Jason/Documents/DataScience/DAT4-students/jason/final_project/data/xmltest.xml"
root = ET.parse(xmltest).getroot()

# reformat xmls to work with ElementTree
for xml in xml_source_list:
    text = '<patents>\n'
    with open(xml,'rU') as f:
       for line in f.readlines():
           if '<?xml' not in line and '<!DOCTYPE' not in line: 
               text += line
    text += '</patents>\n'
    with open(xml_destination_path + xml[-13:], 'wb') as g:
        g.write(text)

# assembles all applicants' names in one list
def applicantNames(patent):
    return_names = []
    return_name = ''
    for applicants in root[patent].findall('.//applicants'):
        apps = applicants.findall('.//applicant')
        for applicant in apps:
            lastname = applicant.findtext('.//addressbook/last-name') 
            firstname = applicant.findtext('.//addressbook/first-name')
            return_name = lastname + ", " + firstname
            return_names.append(return_name)
    return return_names
 
# bundles the patent assignee's organization name and address into a list
def assigneeNameAddress(patent):
    return_assignee = []
    if not len(root[patent].findall('.//assignee')):
        return ['None','None']
    for assignee in root[patent].findall('.//assignee'):
        name = assignee.findtext('.//orgname')
        if assignee.findtext('.//state') != None:
            address = assignee.findtext('.//address').replace('\n', '') + ", " \
            + assignee.findtext('.//city') + ", " + \
            assignee.findtext('.//state').replace('\n', '') + ", " + \
            assignee.findtext('.//country')
        else:
            address = assignee.findtext('.//address').replace('\n', '') + ", " \
            + assignee.findtext('.//city') + ", , " + assignee.findtext('.//country')
        return_assignee.append(name)
        return_assignee.append(address)
    return return_assignee
   

# joins all of a patent's claim text into a single string
def claimCollect(patent):
    return_claims = ''
    for claim in root[patent].findall('.//claims'):
        return_claims += ''.join(claim.itertext()).replace('\n', ' ') + ' '
    return return_claims

def csvExtract(patent):
    table_row = [root[patent].findtext('.//document-id/doc-number'), \
                 root[patent].findtext('.//invention-title'), \
                 root[patent].findtext('.//document-id/kind'), \
                 root[patent].findtext('.//document-id/date'), \
                 root[patent].find('.//application-reference').get('appl-type'), \
                 root[patent].findtext('.//application-reference//date'), \
                 root[patent].findtext('.//classification-national/main-classification'),\
                 len(root[patent].findall('.//references-cited/citation')), \
                 assigneeNameAddress(patent)[0], \
                 assigneeNameAddress(patent)[1], \
                 applicantNames(patent), \
                 len(root[patent].findall('.//applicants/applicant')), \
                 root[patent].findtext('.//abstract/*'), \
                 claimCollect(patent)]
    return table_row
csvExtract(2340)
claimCollect(4604)
assigneeNameAddress(4604)
applicantNames(4605)

headers = ['grant_doc_num', # assigned patent number
'invention_title', 
'grant_kind', # type of patent granted
'grant_date', # when patent was granted
'appl_type', # type of patent applied for
'appl_date', # date of patent application
'main_class', # main US government classification of patent
'num_refs', # number of references cited by the patent applicant and examiners
'assignee_org', # holder of patent
'assignee_address',
'applicant_name', # name of inventor(s)
'num_applicants', # number of applicants
'abstract', # synopsis of patent claims
'claims'] # explanation of patent   

# Extract desired data from formatted xmls and write to individual csvs
for xml in csv_source_list[:1]:
    root = ET.parse(xml).getroot()
    patent_list = root.findall('us-patent-grant')
    patents_table = []
    for index, patent in enumerate(patent_list):
        try:
            patents_table.append(csvExtract(index))
        except:
            continue
    with open(csv_destination_path + xml[-13:-4] +'.csv', 'wb') as g:
        writer = csv.writer(g)
        writer.writerow(headers)
        writer.writerows(patents_table)
    root.clear()  



'''
for xml in csv_source_list[:5]:
    root = ET.parse(xml).getroot()
    patent_list = root.findall('us-patent-grant')
    patents_table = []
    patent_index = len(patent_list) - 1
    for patent in patent_list:
        patent = 0
        while patent < patent_index:
            patents_table.append(csvExtract(patent))
        patent += 1
    with open(csv_destination_path + xml[-13:], 'wb') as g:
        writer = csv.writer(g)
        writer.writerow(headers)
        writer.writerows(patents_table)
    root.clear() 

for xml in csv_source_list[:5]:
    root = ET.parse(xml).getroot()
    patent_list = root.findall('us-patent-grant')
    patents_table = []
    for patent in patent_list:
            table_row = [root[patent].findtext('.//document-id/doc-number'), \
                 root[patent].findtext('.//invention-title'), \
                 root[patent].findtext('.//document-id/kind'), \
                 root[patent].findtext('.//document-id/date'), \
                 root[patent].find('.//application-reference').get('appl-type'), \
                 root[patent].findtext('.//application-reference//date'), \
                 root[patent].findtext('.//classification-national/main-classification'),\
                 len(root[patent].findall('.//references-cited/citation')), \
                 assigneeNameAddress(patent)[0], \
                 assigneeNameAddress(patent)[1], \
                 applicantNames(patent), \
                 root[patent].findtext('.//abstract/*'), \
                 claimCollect(patent)]
        table.append(table_row)
    with open(csv_destination_path + xml[-13:], 'wb') as g:
        writer = csv.writer(g)
        writer.writerow(headers)
        writer.writerows(patents_table)
    root.clear() 
  
root[patent].get('.//application-reference')  
root[patent].find('.//application-reference[@appl-type=]')
parent_map = dict((c, p) for p in tree.getiterator() for c in p)


for grant in root.iterfind('../us-bibliograhpic-data-grant/publication-reference/document-id/doc-number'):
    print grant.tag, grant.text

for text in x.itertext():
            yield text
        for tail in x.itertext():
            yield tail

root[2250].findall('.//claims')

for x in root[patent].findall('.//claims'):
        i = x.findall('.//')
    for text in i:
        return ''.join(text.itertext()).replace('\n', '') 
          
def clCollect(patent):
    for x in root[patent].findall('.//claim'):
        return/yield ''.join(x.itertext()).replace('\n', '')
        
def clCollect(patent):
    for x in root[patent].findall('.//claim/claim-text*'):
        i = x.findall('[claim-text]*')
        for j in i:
            j = i.itertext()
            return ''.join(j)

This one works, but doubles the text of each claim for some reason.
def claimCollect(patent):
    return_claims = ''
    for claim in root[patent].findall('.//claims'):
        i = claim.findall('.//')
        for text in i:
            return_claims += ''.join(text.itertext()).replace('\n', '') + ' '
    return return_claims

[x.findall('.//claim') for x in root[2250].findall('.//claims')]
'''