"""
test_django-teryt
------------

Tests for `django-teryt` modules utils.
"""

from django.utils import six
from django.test import TestCase
from unittest.mock import patch
import requests
import requests_mock
from bs4 import BeautifulSoup

from ..utils import get_xml_id_dictionary, HttpError, ParsingError

class TestUtils(TestCase):
    def setUp(self):
        self.correct_dict = {'SIMC.xml': 1360, 'TERC.xml': 1358,
        'ULIC.xml': 1493, 'WMRODZ.xml': 941}
        
        self.correct_html = """<html><body>
            <table class="list" id="row"><tbody>

            <tr><td>ULIC</td>
            <td><a href="downloadPreFile.jspa?id=1493"/>
            </td></tr>

            <tr><td>TERC</td>
            <td><a href="downloadPreFile.jspa?id=1358"/>
            </td></tr>

            <tr><td>SIMC</td>
            <td><a href="downloadPreFile.jspa?id=1360"/>
            </td></tr>

            <tr><td>WMRODZ</td>
            <td><a href="downloadPreFile.jspa?id=941"/>
            </td></tr>

            </tbody></table></body></html>
            """
            
        self.gus_url = 'http://www.stat.gov.pl/broker/access/prefile/'\
            'listPreFiles.jspa'
    
    def test_parse_correct(self):
        with requests_mock.mock() as m:
            m.get(self.gus_url, text=self.correct_html)
            dictionary = get_xml_id_dictionary(self.gus_url)
            self.assertEqual(dictionary,self.correct_dict)
            
    def test_http_connection_error(self):
        with requests_mock.mock() as m:
            m.get(self.gus_url, text='Not found', status_code=404)           
            self.assertRaises(HttpError,get_xml_id_dictionary)
    
    def test_incorrect_parse_wrong_url(self):
        self.assertRaises(ParsingError,get_xml_id_dictionary,'http://www.wp.pl')
        
    def test_incorrect_parse_initialize_parse_tree_fail(self):
        with patch.object(BeautifulSoup, 'find', return_value=None) as mock_method:
            self.assertRaises(ParsingError, get_xml_id_dictionary)
            self.assertTrue(mock_method.called)
            
            
        