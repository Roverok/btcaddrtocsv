#!/usr/bin/env python3

# Use Grab a useful ods document from a series of BTC addresses

# Small hack to allow using the odslib library without having the
# client add it to their system manually
import sys
sys.path.insert(0, './odslib')

from odslib import ODS

def test():
    print ("Test")
    # Create a New Sheet
    ods = ODS()

    # Creat Sheet Title
    sheet = ods.content.getSheet(0)
    sheet.setSheetName('Test')

    # Add some content
    sheet.getCell(0,0).stringValue("Some Cool Text")
    sheet.getCell(0,1).floatValue(2)

    # Add some more content
    sheet.getCell(1,0).stringValue("Some More Cooler Text")
    sheet.getCell(0,1).floatValue(3)

    # Add a Formula
    sheet.getCell(2,0).stringValue("Together Now")
    sheet.getCell(2,1).floatForumula(0, '=SUM(B2:B3)')


    return


test()
