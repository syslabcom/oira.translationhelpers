#!/usr/bin/env python

# Author: Wolfgang Thomas <thomas@syslab.com>

"""%(program)s: Escape HTML inside XML tags (in case the translators were
    too stupid to use an XML-capable editor).

usage:  %(program)s input.xml output.xml
input.xml    The filename of the exported survey
output.xml   The filename for the fixed survey
"""

import sys
import os
from bs4 import BeautifulSoup, Tag
from xml.sax.saxutils import escape

PLACEHOLDER = 'XXXXX'


def usage(stream, msg=None):
    if msg:
        print(msg, file=stream)
    program = os.path.basename(sys.argv[0])
    print (__doc__ % {"program": program}, file=stream)
    sys.exit(0)


if len(sys.argv) < 3:
    usage(sys.stderr, "\nNot enough arguments")
input = sys.argv[1]
output = sys.argv[2]

fh = open(input, 'r')
data = fh.read()
fh.close()

soup = BeautifulSoup(data, features="lxml")


tags = [
    'title', 'solution-direction', 'description', 'problem-description',
    'action-plan', 'legal-reference',
    'introduction']

bad_tags = [
    "existing_measures"
]

for tag in tags:
    entities = soup.find_all(tag)
    for entity in entities:
        if len(entity.contents) > 1:
            for line in entity.children:
                if isinstance(line, Tag):
                    txt = escape(line.prettify())
                else:
                    txt = line.string
                txt = txt.strip()
                line.replace_with(txt)


for tag in bad_tags:
    bad_ones = soup.findAll(tag)
    [bad.extract() for bad in bad_ones]

contents = soup.sector.encode(formatter=None).decode('utf-8')
xml = "<?xml version='1.0' encoding='utf-8'?>\n{0}".format(contents)
fh = open(output, 'w')
fh.write(xml)
fh.close()


sys.exit('ok')
