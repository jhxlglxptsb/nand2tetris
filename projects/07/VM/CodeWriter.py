#CodeWriter.py

import Parser,sys

class CodeWriter(object):
	def __init__(self, myfile):
		outfile = myfile.replace('.vm', '.asm')
		self.filename = myfile.replace('.vm', '')
		self.out = open(outfile,'w')
		self.count = 0
		
	def setFileName(self, myfile):
		self.parse = Parser.Parser(myfile)

	def writeArithmetic(self):
		com = self.parse.arg1(Parser.C_ARITHMETIC)
		getin = ''
		if com == 'add':
			getin = "@SP" + '\n' + "AM=M-1" + '\n' +  "D=M" + '\n' + "A=A-1" + '\n' + "M=D+M" + '\n'
		elif com == 'sub':
			getin =  "@SP" + '\n' + "AM=M-1" + '\n' +  "D=M" + '\n' +  "A=A-1" + '\n' + "M=M-D" + '\n'
		elif com == 'neg':
			getin = "@SP" + '\n' + "A=M-1" + '\n' + "M=-M" + '\n'
		elif com == 'eq':
			s = str(self.count)
			self.count+=1
			getin = "@SP" + '\n' + "AM=M-1" + '\n' + "D=M" + '\n' + "A=A-1" + '\n' + "D=M-D" + '\n' + "@EQ.TRUE" + s + '\n' + "D;JEQ" + '\n' + "@SP" + '\n' + "A=M-1" + '\n' + "M=0" + '\n' + "@EQ.AFTER" + s + '\n' + "0;JMP" +'\n' + "(EQ.TRUE" + s + ")" + '\n' +  "@SP" + '\n' + "A=M-1" + '\n' + "M=-1" + '\n' + "(EQ.AFTER" + s + ")" + '\n'
		elif com == 'gt':
			s = str(self.count)
			self.count+=1
			getin = "@SP" + '\n' + "AM=M-1" + '\n' + "D=M" + '\n' + "A=A-1" + '\n' + "D=M-D" + '\n' + "@GT.TRUE" + s + '\n' + "D;JGT" + '\n' + "@SP" + '\n' + "A=M-1" + '\n' + "M=0" + '\n' + "@GT.AFTER" + s + '\n' + "0;JMP" +'\n' + "(GT.TRUE" + s + ")" + '\n' + "@SP" + '\n' + "A=M-1" + '\n' + "M=-1" + '\n' + "(GT.AFTER" + s + ")" + '\n'
		elif com == 'lt':
			s = str(self.count)
			self.count+=1
			getin = "@SP" + '\n' + "AM=M-1" + '\n' + "D=M" + '\n' + "A=A-1" + '\n' + "D=M-D" + '\n' + "@LT.TRUE" + s + '\n' + "D;JLT" + '\n' + "@SP" + '\n' + "A=M-1" + '\n' + "M=0" + '\n' + "@LT.AFTER" + s + '\n' + "0;JMP" +'\n' + "(LT.TRUE" + s + ")" + '\n' + "@SP" + '\n' + "A=M-1" + '\n' + "M=-1" + '\n' + "(LT.AFTER" + s + ")" + '\n'
		elif com == 'and':
			getin = "@SP" + '\n' + "AM=M-1" + '\n' + "D=M" + '\n' + "A=A-1" + '\n' + "M=D&M" + '\n'
		elif com == 'or':
			getin = "@SP" + '\n' + "AM=M-1" + '\n' + "D=M" + '\n' + "A=A-1" + '\n' + "M=D|M" + '\n'
		elif com == 'not':
			getin = "@SP" + '\n' + "A=M-1" + '\n' + "M=!M" + '\n'
		self.out.write(getin)

	def WritePushPop(self):
		if self.parse.commandType() == Parser.C_PUSH:
			self.WritePush()
		else:
			self.WritePop()

	def WritePush(self):
		mypush = "@SP\nA=M\nM=D\n@SP\nM=M+1\n"
		com = self.parse.arg1(Parser.C_PUSH)
		num = self.parse.arg2()
		getin = ''
		if com == 'argument':
			getin = "@ARG\nD=M\n@" + num + "\nA=D+A\nD=M\n" + mypush
		elif com == 'local':
			getin = "@LCL\nD=M\n@" + num + "\nA=D+A\nD=M\n" + mypush
		elif com == 'static':
			getin = "@"+self.filename + num + "\nD=M\n" + mypush
		elif com == 'constant':
			getin = "@" + num + "\nD=A\n" + mypush
		elif com == 'this':
			getin = "@THIS\nD=M\n@" + num + "\nA=D+A\nD=M\n" + mypush
		elif com == 'that':
			getin = "@THAT\nD=M\n@" + num + "\nA=D+A\nD=M\n" + mypush
		elif com == 'pointer':
			if num == '0':
				getin = "@THIS\nD=M\n" + mypush
			else:
				getin = "@THAT\nD=M\n" + mypush
		elif com == 'temp':
			getin = "@R5\nD=A\n@" + num + "\nA=D+A\nD=M\n" + mypush
		self.out.write(getin)

	def WritePop(self):
		mypop = "@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n" 
		com = self.parse.arg1(Parser.C_POP)
		num = self.parse.arg2()
		getin = ''
		if com == 'argument':
			getin = "@ARG\nD=M\n@" + num + "\nD=D+A\n" + mypop
		elif com == 'local':
			getin = "@LCL\nD=M\n@" + num + "\nD=D+A\n" + mypop
		elif com == 'static':
			getin = "@"+self.filename + num + "\nD=A\n" + mypop
		elif com == 'this':
			getin = "@THIS\nD=M\n@" + num + "\nD=D+A\n" + mypop
		elif com == 'that':
			getin = "@THAT\nD=M\n@" + num + "\nD=D+A\n" + mypop
		elif com == 'pointer':
			if num == '0':
				getin = "@THIS\nD=A\n" + mypop
			else:
				getin = "@THAT\nD=A\n" + mypop
		elif com == 'temp':
			getin = "@R5\nD=A\n@" + num + "\nD=D+A\n" + mypop
		self.out.write(getin)

	def Close(self):
		self.out.close()

	def run(self, myfile):
		self.setFileName(myfile)
		while self.parse.hasMoreCommands():
			self.parse.advance()
			mytype = self.parse.commandType()
			if mytype == Parser.C_ARITHMETIC:
				self.writeArithmetic()
			elif mytype == Parser.C_PUSH or mytype == Parser.C_POP:
				self.WritePushPop()
		self.Close()

if __name__ == "__main__": 
	myfile = sys.argv[1]
	ass = CodeWriter(myfile)
	ass.run(myfile)
