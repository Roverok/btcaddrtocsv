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

	def initiallogic(self) :
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
		fmt = '%Y-%m-%d %H:%M:%S'
		for txs in alltrans:
			inout = self.getdiff(txs)
			txtime = datetime.datetime.fromtimestamp(int(txs["time"]))
			self.blktrans.append([ txtime.strftime(fmt), self.api_address , txs["hash"] , inout["in"] , inout["out"] ])

	
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
		

		
	def getdiff(self, datx):
		# Find the change
		satoshisin = 0
		satoshisout = 0
		for inputaddr in datx["inputs"]:
			if "prev_out" in inputaddr :
				if inputaddr["prev_out"]["addr"] == self.api_address :
					# Correct Address
					satoshisout = satoshisout + inputaddr["prev_out"]["value"]
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
					satoshisin = satoshisin + outputaddr["value"]
			else:
				# Object totally Doesn't. Fuck that bitch!
				continue;
		inout = { "in" : satoshisin , "out" : satoshisout }
		return inout
		
	def writetocsv(self, filename):
		output = open(filename, 'w', newline='', encoding='utf8')
		wr = csv.writer(output, quotechar=None)
		
		# Write Headers
		wr.writerow(["Date","Account","Description", "Money In", "Money Out"])
		for item in self.blktrans :
			print (item)
			wr.writerow(item)
