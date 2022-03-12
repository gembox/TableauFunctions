# -*- coding: utf-8 -*-
"""
author:rhelenius
"""

import xml.etree.ElementTree as ET

def update_color_palette(wbname,palettename,oldColor,newColor):
    '''This will take in an existing color found in a palette and reaplce it with a new one. Should be specified by the hex code. It will update
    both the embedded color palette and also any references to the color used in the palette.
    Args: 
        wbname (string): Name of the Tableau .twb file
        palettename (string): Name of the custom color palette
        oldColor (string): Hex value of the color to be replaced
        newColor (string): Hex value of the new color
    Raises:
        Exception: Color palette not found in workbook
    
    Output:
        Overwrites the existing Tableau file with the new color values
    '''
    matched_flag = False
    #Register namespace
    ET.register_namespace('user', "http://www.tableausoftware.com/xml/user")
    #Read workbook xml
    tree = ET.parse(wbname)
    root = tree.getroot()
    #Update color code in color palette if found, raise an error if not
    for child in tree.findall("preferences/color-palette[@name='"+palettename+"']/color"):
        if child.text is not None and child.text == oldColor:
            child.text = newColor
            matched_flag = True
    else:
        if matched_flag == False:
            raise Exception('No color {} in palette named {}'.format(oldColor,palettename))
    #Update color code in column property
    for child in tree.findall("datasources/datasource/style/style-rule/encoding[@palette='"+palettename+"']/map[@to='"+oldColor+"']"):
        if child is not None:
            child.set("to",newColor)
    #Get the XML we read in above and write the new element
    tree = ET.ElementTree(root)
    tree.write(wbname, xml_declaration=True, encoding ='utf-8')