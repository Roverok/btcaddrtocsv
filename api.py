#! /usr/bin/env python3

import json
import urllib.request
import csv
import datetime
from datetime import tzinfo

class BLKAPI(object):
	
	api_url = "http://blockchain.info/address/"
	api_address = "1KMLjhgjGLxZTJT5TSWxV2HCZHBqpDEpa1"
	# Temporary Hardcode
	api_format = "?format=json"
	# Transactions
	blktrans = []
	prevtranstxids = []
	prevtransactions = []
	
	def convertoldcsvtrans(self, oldfilename):
		oldfile = open(oldfilename, 'r')
		csvoldfile = csv.reader(oldfile)
		print (csvoldfile.line_num)
		for row in csvoldfile:
			for i in self.blktrans:
				# Search Through Transactions
				if row[3] == i[3]:
					# Add Commnets to New One
					i[6] = row[6]

	def initiallogic(self, address) :
		self.api_address = address
		numtrans = 0
		initialcall = self.call(0)
		self.numberOfTransactions = initialcall["n_tx"]
		self.populatetrans(initialcall["txs"])
		numtrans += 50
		while self.numberOfTransactions > numtrans :
			subsequentcalls = self.call(numtrans)
			self.populatetrans(subsequentcalls["txs"])
			numtrans += 50
			
			
		'''
		for txs in initialcall["txs"]:
			inout = self.getdiff(txs)
			txtime = datetime.datetime.fromtimestamp(int(txs["time"]))
			self.blktrans.append([ txtime.strftime(fmt), self.api_address , txs["hash"] , inout["in"] , inout["out"] ])
		'''

	def populatetrans(self, alltrans):
		# Date Format YYYY-MM-DD HH:MM:SS TZ
		fmt = '%y-%m-%d'
		fmttime = '%H:%M:%S'
		for txs in alltrans:
			inout = self.getdiff(txs)
			txtime = datetime.datetime.fromtimestamp(int(txs["time"]))
			self.blktrans.append([ txtime.strftime(fmt), txtime.strftime(fmttime), self.api_address , txs["hash"] , inout["in"] , inout["out"], "" ])

	
	def call(self, offset):
		if offset == 0 :
			# No need of Offset api
			api_call = self.api_url + self.api_address + self.api_format
		else:
			api_call = self.api_url + self.api_address + self.api_format + "&offset=" + str(offset)
		print("Trying API Call:\n " + api_call)
		request = urllib.request.Request(api_call)
		response = urllib.request.urlopen(request)
		xjson = json.loads((response.read().decode('utf-8')))
		return xjson
	
	def normalize(self):
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
		
	def bitcoinit(self):
		for item in self.blktrans:
			# Convert to BTC
			item[4] = float(item[4])/100000000
			item[5] = float(item[5])/100000000
		
		return
		
	def getdiff(self, datx):
		# Find the change
		satoshisin = 0
		satoshisout = 0
		for inputaddr in datx["inputs"]:
			if "prev_out" in inputaddr :
				if inputaddr["prev_out"]["addr"] == self.api_address :
					# Correct Address
					satoshisout += inputaddr["prev_out"]["value"]
			else :
				# No Input Transaction; Do Nothing
				continue;
		#print(datx["out"])
		for outputaddr in datx["out"]:
			if "addr" in outputaddr:
				# Object Exists Keep Going
				if outputaddr["addr"] == self.api_address :
					# Correct Address
					# print("Amount Value Up:\n " + str(outputaddr["value"]))
					satoshisin += outputaddr["value"]
			else:
				# Object totally Doesn't. Fuck that bitch!
				continue;
		inout = { "in" : satoshisin , "out" : satoshisout }
		return inout
		
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
			# Print the Transaction Pythonically
			print (item)
			# Print the Transaction CSV Style to File
			wr.writerow(item)
