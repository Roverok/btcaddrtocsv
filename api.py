#! /usr/bin/env python3

import json
import urllib.request
import csv

class BLKAPI(object):
	
	api_url = "http://blockchain.info/address/"
	api_address = "1KMLjhgjGLxZTJT5TSWxV2HCZHBqpDEpa1"
    # Temporary Hardcode
	api_format = "?format=json"
    # Transactions
	blktrans = { }

	def initiallogic(self) :
		numtrans = 0
		initialcall = self.call(0)
		numberOfTransactions = initialcall["n_tx"]
		for txs in initialcall["txs"]:
			inout = self.getdiff(txs)
			self.blktrans[numtrans] = []
			self.blktrans[numtrans].append( self.api_address)
			self.blktrans[numtrans].append(txs["hash"])
			self.blktrans[numtrans].append(inout["in"])
			self.blktrans[numtrans].append(inout["out"])
			numtrans = numtrans + 1
			
	def call(self, offset):
		if offset == 0 :
			# No need of Offset api
			api_call = self.api_url + self.api_address + self.api_format
		else:
			api_call = self.api_url + self.api_address + self.api_format + "&offset=" + offset
		# print("Trying API Call:\n " + api_call)
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
		wr.writerow(["Account","Description", "Money In", "Money Out"])
		for item in self.blktrans :
			print (self.blktrans[item])
			wr.writerow(self.blktrans[item])
