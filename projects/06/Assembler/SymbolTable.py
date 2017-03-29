class symboltable(object):
	def constructor(self):
		self.symbols = {}

	def addEntry(self, symbol, address):
		self.symbols[symbol] = address

	def contains(self, symbol):
		return symbol in self.symbols

	def GetAddress(self, symbol):
		return self.symbols[symbol]