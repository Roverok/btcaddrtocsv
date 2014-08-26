#! /usr/bin/python3.2

# Grab Address and Info and convert to CSV File for given dates

from api import BLKAPI
import argparse

# Grab Values from CLI
parser = argparse.ArgumentParser()

# -h Help
# -a BTCAddress
# -o CSV Output File
# -x Existing CSV File
parser.add_argument("-a", "--btcaddress", help="Bitcoin Address", required=True)
parser.add_argument("-o", "--outputfile", help="CSV Formatted Output File", default="out.csv")
parser.add_argument("-x", "--existing", help="CSV Formatted Existing File")

args = parser.parse_args()

# Place Values for Output File and Address in their constants
outputfilename = args.outputfile
btcaddr = args.btcaddress

# Create new BLKAPI Object (See api.py)
test = BLKAPI()
# Run BLKAPI.initiallogic(btcaddr)
test.initiallogic(btcaddr)

# If they gave an existing address Use it
if args.existing :
	# Use the BLKAPI().convert..trans() function to parse the initial file
	# Parsing the initial file will allow us to match comments on
	# transactions via txid
	test.convertoldcsvtrans(args.existing)

# Removing Printing
# print (test.blktrans)
# Writeout the file via BLKAPI.writetocsv
test.writetocsv(outputfilename)
