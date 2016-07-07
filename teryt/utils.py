#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as et
from django.utils.encoding import smart_text
import re

class HttpError(Exception):
    pass
    
class ParsingError(Exception):
    pass

def xstr(s):
    return '' if s is None else smart_text(s)


def parse(stream):
    for event, element in et.iterparse(stream):
        if element.tag != 'row':
            continue
        yield {
            x.get('name'): x.text.strip() if x.text else None for x in element
        }

def get_xml_id_dictionary(url='http://www.stat.gov.pl/broker/access/prefile/'\
            'listPreFiles.jspa'):
    from bs4 import BeautifulSoup
    import requests
    
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        msg = 'An error occured while connecting to {},'\
        'status code: {}'.format(url,response.status_code)
        raise HttpError(msg)
    soup = BeautifulSoup(response.content,'html.parser')
    
    try:
        files = {}
        table = soup.find(name='table', id='row')
        tbody = table.find(name='tbody')

        for tr in tbody.find_all(name='tr'):
            fname = tr.find(name='td')
            fname = fname.string
            fname = fname+'.xml'
            id = tr.find(name='a',href=re.compile('downloadPreFile'))
            files[ fname ] = int((id['href']).rpartition('id=')[2])
    except AttributeError:
        raise ParsingError("Cannot parse tree, possibly incorrect url or obsolete code.")
        
    return files
            
