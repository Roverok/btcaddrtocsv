#! /usr/bin/python3.2

# Grab Address and Info and convert to CSV File for given dates

from api import BLKAPI
import argparse

parser = argparse.ArgumentParser()

# -h Help
# -a BTCAddress
# -o CSV Output File
parser.add_argument("-a", "--btcaddress", help="Bitcoin Address")
parser.add_argument("-o", "--outputfile", help="CSV Formatted Output File")

args = parser.parse_args()

outputfilename = args.outputfile
btcaddr = args.btcaddress


test = BLKAPI()
test.initiallogic(btcaddr)
# print (test.blktrans)

test.writetocsv(outputfilename)
