import Parser, Code, SymbolTable, sys

class assembler(object):
	def __init__(self):
		self.count = 0
		self.sy = 16
		self.symbol = SymbolTable.symboltable()

	def firstpass(self, myfile):
		parse = Parser.parser(myfile)
		while parse.hasMoreCommands():
			parse.advance()
			cmdtype = parse.commandType()
			if cmdtype == Parser.A_COMMAND or cmdtype == Parser.C_COMMAND:
				self.count+=1
			else:
				self.symbol.addEntry(parse.symbols(), self.count)

	def secondpass(self, myfile, outfile):
		parse = Parser.parser(myfile)
		out = open(outfile,'w')
		mycode = Code.code()
		while parse.hasMoreCommands():
			parse.advance()
			cmdtype = parse.commandType()
			if cmdtype == Parser.A_COMMAND:
				symb = parse.symbols()
				if symb.isdigit():
					out.write('0' + bin(int(symb))[2:].zfill(15) + '\n')
				else:
					if not self.symbol.contains(symb):
						self.symbol.addEntry(symb, self.sy)
						self.sy+=1
					symnum = self.symbol.GetAddress(symb)
					if symb == 'ponggame.0':
						print symnum
					out.write('0' + bin(int(symnum))[2:].zfill(15) + '\n')
			elif cmdtype == Parser.C_COMMAND:
				dest = mycode.dest(parse.dest())
				comp = mycode.comp(parse.comp())
				jump = mycode.jump(parse.jump())
				out.write('111' + comp + dest + jump + '\n')
			else:
				pass
		out.close()

	def run(self, myfile):
		outfile = myfile.replace('.asm', '.hack')
		self.firstpass(myfile)
		self.secondpass(myfile, outfile)

if __name__ == "__main__": 
	myfile = sys.argv[1]
	ass = assembler()
	ass.run(myfile)  