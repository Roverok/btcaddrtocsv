#! /usr/bin/python3.2

# Grab Address and Info and convert to CSV File for given dates

from api import BLKAPI
import argparse

parser = argparse.ArgumentParser()

# -h Help
# -a BTCAddress
# -o CSV Output File
# -x Existing CSV File
parser.add_argument("-a", "--btcaddress", help="Bitcoin Address", required=True)
parser.add_argument("-o", "--outputfile", help="CSV Formatted Output File", default="out.csv")
parser.add_argument("-x", "--existing", help="CSV Formatted Existing File")

args = parser.parse_args()

outputfilename = args.outputfile
btcaddr = args.btcaddress


test = BLKAPI()
test.initiallogic(btcaddr)

if args.existing :
	test.convertoldcsvtrans(args.existing)

print (test.blktrans)

test.writetocsv(outputfilename)
