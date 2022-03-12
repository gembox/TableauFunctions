# -*- coding: utf-8 -*-
"""
author:rhelenius
"""

from lxml import etree
from spellchecker import SpellChecker
import re

def spellcheck_workbook(wbname):
    '''
    This will take in a workbook and check titles and text box objects for spelling errors. If errors are found
    it will tell you the text string, which word was flagged and where it was located. It is currently avoiding
    processing tooltips because of their messy representation in the XML, but may be implemented later.
    '''
    #Read workbook xml and instatiate spellchecker
    tree = etree.parse(wbname)
    root = tree.getroot()
    spell = SpellChecker()

    def find_errors(objecttype):
        '''
        This will take in a object type to find the element, parent path to get attributes from, and checks their 
        spelling for errors. Right now it supports dashboards or worksheets. In the future this could be expanded 
        to include additional types of objects/paths.
        '''
        elempath = './/dashboard/zones//formatted-text/run' if objecttype == 'textbox' else './/worksheet//title/formatted-text/run'
        elemparent = 'ancestor::dashboard' if objecttype == 'textbox' else 'ancestor::worksheet'
        for w in root.findall(elempath):
            elemtype = 'dashboard' if objecttype == 'dashboard' else 'worksheet'
            words = re.sub(r'[^\w\s]','',w.text)
            misspelled_ws = spell.unknown(words.split())
            if len(misspelled_ws) > 0:
                print('{} text: '.format(objecttype) + w.text)
                for word in misspelled_ws:
                    print('Flagged word: ' + word)
                    print('Suggested replacement: ' + spell.correction(word))
                for parent in w.xpath(elemparent):
                    print('Found in {}: '.format(elemtype) + parent.attrib['name'])
                print('\n')

    #let's call find_errors for worksheets and dashboards
    find_errors('title')
    find_errors('textbox')