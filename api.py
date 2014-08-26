#! /usr/bin/env python3

# JSON Library neccessary to convert Blockchain.info API Information
import json

# urllib.request used to grab the json info from Blockchain.info
import urllib.request

# Standard CSV library from Python3 used to convert the array of objects
# to a csv file
import csv

# Grab the standard python Date Libraries for time converstion
import datetime
# Specifically grab the tzinfo. I'm not sure if I'm still using it anywhere.
from datetime import tzinfo

class BLKAPI(object):
	
	# API URL
	api_url = "http://blockchain.info/address/"
	# No Longer Used. But Old main RSM Mining Address
	api_address = "1KMLjhgjGLxZTJT5TSWxV2HCZHBqpDEpa1"
	# Tail to go after the url
	# Triggers a JSON response by blockchain.info
	api_format = "?format=json"
	# Transactions Array
	blktrans = []
	# Array of Transaction IDs
	prevtranstxids = []
	# Array of Previous Transaction
	prevtransactions = []
	
	# Pars the Give CSV file for old Transaction Comments
	# At this point I've already Grabbed the newest list of transactions
	# From Blockchain.info
	def convertoldcsvtrans(self, oldfilename):
		# Open the Old file
		oldfile = open(oldfilename, 'r')
		# Create  Object that now has the old CSV file's data
		csvoldfile = csv.reader(oldfile)
		print (csvoldfile)
		# Iterate through the old transaction rows
		for row in csvoldfile:
			# Iterate through the grabbed transactions rows
			for i in self.blktrans:
				# Search Through Transactions compare the txids
				# To see if old transactions have comments
				# That match the new transactions
				# Remember i is the BLKTRANS()'s Transaction
				# Table that was just updated by the 
				# initiallogic("ADDRESS") call
				if row[3] == i[3]:
					# Add Commnets to New One
					i[6] = row[6]

	# Initial Logic Call. Populates BLKTRANS() with transaction data
	# via BLKTRANS.populatetrans()
	def initiallogic(self, address) :

		# Note: priming the loop cuts down on an extra API call. I'm 
		# Sure I could change how the loop is handled if I had the time
		# However I do not atm have the time.

		# Set Initials
		# Bitcoin address as a strin
		self.api_address = address
		# Initial Transaction (right now 0)
		numtrans = 0
		# Call BLKTRANS.call() Which grabs Transactions 0-50 
		# (if they exist). Also returns various stats on the address
		# in question
		initialcall = self.call(0)
		# Grabs the number of transactions from the initialcall
		self.numberOfTransactions = initialcall["n_tx"]
		# Populates the internal data via the 
		# BLKTRANS.populatetrans(trans[...]) function
		self.populatetrans(initialcall["txs"])
		# Increment the Transaction number to +50
		numtrans += 50

		# Begin to loop through 50 transactions at a time
		# (blockchain.info rate Limiting)
		while self.numberOfTransactions > numtrans :
			# Calls Call to get the Latest JSON info
			subsequentcalls = self.call(numtrans)
			# Calls populate transactions and sends 
			# this 50 transactions to the transaction array
			self.populatetrans(subsequentcalls["txs"])
			# Increments the transaction counter by 50
			numtrans += 50
			
			
		# Now Commented Out
		'''
		for txs in initialcall["txs"]:
			inout = self.getdiff(txs)
			txtime = datetime.datetime.fromtimestamp(int(txs["time"]))
			self.blktrans.append([ txtime.strftime(fmt), self.api_address , txs["hash"] , inout["in"] , inout["out"] ])
		'''
	# Add the transactions in alltrans to the BLK transaction array
	def populatetrans(self, alltrans):
		# Date Format YYYY-MM-DD HH:MM:SS TZ
		fmt = '%y-%m-%d'
		# Format time HH:MM:SS in 24 hour time
		fmttime = '%H:%M:%S'
		# Iterate through the transactions in alltrans
		for txs in alltrans:
			# Grab the change via the BLKTRANS.getdiff() function.
			# Send the transaction in question
			inout = self.getdiff(txs)
			# Convert the Timestamp to A pythonic Time
			txtime = datetime.datetime.fromtimestamp(int(txs["time"]))
			# Onto the end of the transaction array add this tx
			self.blktrans.append([ txtime.strftime(fmt), txtime.strftime(fmttime), self.api_address , txs["hash"] , inout["in"] , inout["out"], "" ])

	
	def call(self, offset):
		if offset == 0 :
			# No need of Offset api
			api_call = self.api_url + self.api_address + self.api_format
		else:
			# Add offset
			api_call = self.api_url + self.api_address + self.api_format + "&offset=" + str(offset)
		# print("Trying API Call:\n " + api_call)
		# Request & Response Dance to grab the data
		# Need to add error checking and retrying at some point
		request = urllib.request.Request(api_call)
		response = urllib.request.urlopen(request)
		# Convert the response to json
		xjson = json.loads((response.read().decode('utf-8')))
		# Send the json back to the initial function
		return xjson
	
	def normalize(self):
		# Instead of giving total inputs and outputs. Only display the net change
		for item in self.blktrans:
			if item[4] == 0 or item[5] == 0 :
				## No real Normalization here. One of these is already 0
				continue;
			elif item[4] > item[5] :
				## Net Positive Transaction
				tempfour = item[4] - item[5]
				## Positive Transaction Zero Leaving in the End
				item[5] = 0
				## Set Adjusted Postive Amount
				item[4] = tempfour
			elif item[5] > item[4] :
				## Net Negative Transaction
				tempfive = item[5] - item[4]
				## Negative Transaction Zero Incoming in the End
				item[4] = 0
				## Set Adjusted Negative Amount
				item[5] = tempfive
		return
		
	# Converts transactions in transaction array from satoshis to BTC.
	# When adding uBTC or mBTC this is where you'd change the value
	def bitcoinit(self):
		for item in self.blktrans:
			# Convert to BTC
			item[4] = float(item[4])/100000000
			item[5] = float(item[5])/100000000
		
		return
		
	# Gets the changes for a particular transaction
	def getdiff(self, datx):
		# Find the change
		# Initials
		satoshisin = 0
		satoshisout = 0
		# Loop through Inputs
		for inputaddr in datx["inputs"]:
			# Loops through addresses in inputs
			if "prev_out" in inputaddr :
				# If the inputs here are the same as the main address we're querying a change
				# has occurred
				if inputaddr["prev_out"]["addr"] == self.api_address :
					# Correct Address
					satoshisout += inputaddr["prev_out"]["value"]
			else :
				# No Input Transaction; Do Nothing
				continue;
		#print(datx["out"])
		# Now do the same thing for output addresses
		for outputaddr in datx["out"]:
			# Check through actual addresses
			if "addr" in outputaddr:
				# Object Exists Keep Going
				if outputaddr["addr"] == self.api_address :
					# Correct Address
					# print("Amount Value Up:\n " + str(outputaddr["value"]))
					satoshisin += outputaddr["value"]
			else:
				# Object totally Doesn't. Fuck that bitch!
				# | Classic me. I had a really stupid error witht this 
				# for like three days. It was related to this section. 
				# Forgive the foul language.
				continue;
		# Return dictionary with the different satoshis
		inout = { "in" : satoshisin , "out" : satoshisout }
		return inout
		
	# Function to write the final transaction array to a scv file
	def writetocsv(self, filename):
		
		## Normalize First
		self.normalize()
		## Convert Satoshi to BTC
		self.bitcoinit()
		
		## Create Output File
		output = open(filename, 'w', newline='', encoding='utf8')
		## Create CSV Writer
		wr = csv.writer(output, quotechar=None)
		
		# Write Headers
		wr.writerow(["Date","Time","Account","Description", "Money In", "Money Out", "Notes"])
		
		## Write Transactions
		for item in self.blktrans :
			# Print the Transaction CSV Style to File
			wr.writerow(item)

