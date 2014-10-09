#!/usr/bin/env python3

# Use Grab a useful ods document from a series of BTC addresses

# Small hack to allow using the odslib library without having the
# client add it to their system manually
import sys
sys.path.insert(0, './ezodf')

from ezodf import newdoc, Sheet

def test():
    ods = newdoc(doctype='ods', filname='test.ods')
    sheet1 = Sheet('sheet1')
    ods.sheets += sheet1
    sheet['A1'].set_value("Test")
    ods.save()


test()
