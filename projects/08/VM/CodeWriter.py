#CodeWriter.py

import Parser,sys
import os,glob

class CodeWriter(object):
	def __init__(self, myfile):
		outfile =  ''
		if '.vm' in myfile:
			outfile = myfile.replace('.vm', '.asm')
		else:
			outfile = myfile + '\\' + myfile + '.asm'
		self.out = open(outfile,'w')
		self.count = 0
		self.mypush = "@SP\nA=M\nM=D\n@SP\nM=M+1\n"
		self.mypop = "@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n" 
		
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
		com = self.parse.arg1(Parser.C_PUSH)
		num = self.parse.arg2()
		getin = ''
		if com == 'argument':
			getin = "@ARG\nD=M\n@" + num + "\nA=D+A\nD=M\n"
		elif com == 'local':
			getin = "@LCL\nD=M\n@" + num + "\nA=D+A\nD=M\n"
		elif com == 'static':
			getin = "@" + self.filename + num + "\nD=M\n"
		elif com == 'constant':
			getin = "@" + num + "\nD=A\n"
		elif com == 'this':
			getin = "@THIS\nD=M\n@" + num + "\nA=D+A\nD=M\n"
		elif com == 'that':
			getin = "@THAT\nD=M\n@" + num + "\nA=D+A\nD=M\n"
		elif com == 'pointer':
			if num == '0':
				getin = "@THIS\nD=M\n"
			else:
				getin = "@THAT\nD=M\n"
		elif com == 'temp':
			getin = "@R5\nD=A\n@" + num + "\nA=D+A\nD=M\n"
		self.out.write(getin)
		self.out.write(self.mypush)

	def WritePop(self):
		com = self.parse.arg1(Parser.C_POP)
		num = self.parse.arg2()
		getin = ''
		if com == 'argument':
			getin = "@ARG\nD=M\n@" + num + "\nD=D+A\n"
		elif com == 'local':
			getin = "@LCL\nD=M\n@" + num + "\nD=D+A\n"
		elif com == 'static':
			getin = "@"+self.filename + num + "\nD=A\n"
		elif com == 'this':
			getin = "@THIS\nD=M\n@" + num + "\nD=D+A\n"
		elif com == 'that':
			getin = "@THAT\nD=M\n@" + num + "\nD=D+A\n"
		elif com == 'pointer':
			if num == '0':
				getin = "@THIS\nD=A\n"
			else:
				getin = "@THAT\nD=A\n"
		elif com == 'temp':
			getin = "@R5\nD=A\n@" + num + "\nD=D+A\n"
		self.out.write(getin)
		self.out.write(self.mypop)

	def callFunction(self, ag1, ag2, s):
		ret = "@RET." + s + "\nD=A\n" + self.mypush
		lcl = "@LCL\nD=M\n" + self.mypush
		ag = "@ARG\nD=M\n" + self.mypush
		isat = "@THIS\nD=M\n" + self.mypush + "@THAT\nD=M\n" + self.mypush
		sp = "@SP\nD=M\n@" + ag2 + "\nD=D-A\n@5\nD=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n@" + ag1 + "\n0;JMP\n(RET." + s + ")\n"
		getin = ret + lcl + ag + isat +sp;
		self.out.write(getin)

	def writeInit(self):
		getin = "@256\nD=A\n@SP\nM=D\n"
		self.out.write(getin)
		s = str(self.count)
		self.count+=1
		if self.issys == 1:
			self.callFunction("Sys.init", "0", s)
		self.out.write("0;JMP\n")

	def writeLabel(self):
		com = self.parse.arg1(Parser.C_LABEL)
		getin = "(" + self.parse.func + "$" + com + ")\n"
		self.out.write(getin)

	def writeGoto(self):
		com = self.parse.arg1(Parser.C_GOTO)
		getin = "@" + self.parse.func + "$" + com +"\n0;JMP\n"
		self.out.write(getin)

	def writeIf(self):
		com = self.parse.arg1(Parser.C_IF)
		getin = "@SP\nAM=M-1\nD=M\n@" + self.parse.func + "$" + com + "\nD;JNE\n"
		self.out.write(getin)

	def writeCall(self):
		s = str(self.count)
		self.count+=1
		com = self.parse.arg1(Parser.C_CALL)
		num = self.parse.arg2()
		self.callFunction(com, num, s)

	def writeReturn(self):
		getin= "@LCL\nD=M\n@5\nD=D-A\nA=D\nD=M\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\nD=A+1\n@SP\nM=D\n@LCL\nAM=M-1\nD=M\n@THAT\nM=D\n@LCL\nAM=M-1\nD=M\n@THIS\nM=D\n@LCL\nAM=M-1\nD=M\n@ARG\nM=D\n@LCL\nAM=M-1\nD=M\n@LCL\nM=D\n@R13\nA=M\n0;JMP\n"
		self.out.write(getin)

	def writeFunction(self):
		com = self.parse.arg1(Parser.C_FUNCTION)
		getin = "(" + com + ")\n"
		self.out.write(getin)
		num = int(self.parse.arg2())	
		for i in range(0, num):
			self.out.write("@0\nD=A\n" + self.mypush)

	def Close(self):
		self.out.close()

	def run(self, myfile):
		self.issys = 0
		f = glob.glob(myfile + '\\*.vm')
		for file in f : 
			filen = os.path.basename(file)
			if filen == 'Sys.vm':
				self.issys = 1	
		self.writeInit();
		for file in f : 
			self.filename = os.path.basename(file)
			self.setFileName(file)
			while self.parse.hasMoreCommands():
				self.parse.advance()
				mytype = self.parse.commandType()
				if mytype == Parser.C_ARITHMETIC:
					self.writeArithmetic()
				elif mytype == Parser.C_PUSH or mytype == Parser.C_POP:
					self.WritePushPop()
				elif mytype == Parser.C_LABEL:
					self.writeLabel()
				elif mytype == Parser.C_GOTO:
					self.writeGoto()
				elif mytype == Parser.C_IF:
					self.writeIf()
				elif mytype == Parser.C_CALL:
					self.writeCall()
				elif mytype == Parser.C_RETURN:
					self.writeReturn()
				elif mytype == Parser.C_FUNCTION:
					self.writeFunction()
		self.Close()

if __name__ == "__main__": 
	myfile = sys.argv[1]
	ass = CodeWriter(myfile)
	ass.run(myfile)
