#! /usr/bin/python3.2

# Grab Address and Info and convert to CSV File for given dates

from api import BLKAPI
import argparse

parser = argparse.ArgumentParser()

# -h Help
# -a BTCAddress
# -o CSV Output File
parser.add_argument("-a", "--btcaddress", help="Bitcoin Address", required=True)
parser.add_argument("-o", "--outputfile", help="CSV Formatted Output File", default="out.csv")

args = parser.parse_args()

outputfilename = args.outputfile
btcaddr = args.btcaddress


test = BLKAPI()
test.initiallogic(btcaddr)
test.convertoldcsvtrans("test2.csv")
print (test.blktrans)

test.writetocsv(outputfilename)
