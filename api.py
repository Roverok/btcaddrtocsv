#! /usr/bin/env python3


class BLKAPI(object):
	
	api_url = "http://blockchain.info/address/"
	api_address = "1KMLjhgjGLxZTJT5TSWxV2HCZHBqpDEpa1"
    # Temporary Hardcode
	api_format = "format=json"
    # Transactions
	blktrans = { }

	def initiallogic(self) :
		initialcall = self.call(0)
		numberOfTransactions = initialcall["n_tx"]
		for txs in initialcall["txs"]:
			inout = self.getdiff(txs)
			blktrans["Account"] = self.apicall
			blktrans["Description"] = txs["hash"]
			blktrans["MONEYIN"] = inout["in"]
			blktrans["MONEYOUT"] = inout["out"]
			
	def call(self, offset):
		if offset == 0 :
			# No need of Offset api
			api_call = self.api_url + self.api_address + self.api_format
		else:
			api_call = self.api_url + self.api_address + self.api_format + "&offset=" + offset
		request = urllib.request.Request(api_call)
		response = urllib.request.urlopen(request)
		xjson = json.loads((response.read().decode('utf-8')))
		return xjson
		

		
	def getdiff(self, datx):
		# Find the change
		satoshisin = 0
		satoshisout = 0
		for input in datx["input"]:
			if input["prev_out"]["addr"] == self.api_address :
				# Correct Address
				satoshisout = satoshisout + input["prove_out"]["value"]
		for output in datx["out"]:
			if output["addr"] == self.api_address :
				# Correct Address
				satoshisin = satoshisin + output["addr"]["value"]
		
		inout = { "in" : satoshisin , "out" : satoshisout }
		return inout
