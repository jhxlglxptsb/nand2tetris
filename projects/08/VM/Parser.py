#Parser.py

import re

C_ARITHMETIC = 1
C_PUSH = 2
C_POP = 3
C_LABEL = 4
C_GOTO = 5
C_IF = 6
C_RETURN = 7
C_CALL = 8
C_FUNCTION = 9

class Parser(object):
	def __init__(self, myfile):
		tempfile = open(myfile, 'r')
		self.rawcommands = tempfile.readlines()
		self.commands = []
		self.mydeal()
		self.start = 0
		self.curcmd = ''
		self.func = ''

	def hasMoreCommands(self):
		return self.start<len(self.commands)

	def advance(self):
		self.curcmd = self.commands[self.start]
		self.start += 1

	def commandType(self):
		token = self.curcmd.split(' ')
		if token[0] == 'push':
			return C_PUSH
		elif token[0] == 'pop':
			return C_POP
		elif token[0] == 'label':
			return C_LABEL
		elif token[0] == 'goto':
			return C_GOTO
		elif token[0] == 'if-goto':
			return C_IF
		elif token[0] == 'return':
			return C_RETURN
		elif token[0] == 'call':
			return C_CALL
		elif token[0] == 'function':
			self.func = self.arg1(C_FUNCTION)
			return C_FUNCTION
		else:
			return C_ARITHMETIC

	def arg1(self,ty):
		token = self.curcmd.split(' ')
		if ty == C_ARITHMETIC:
			return token[0]
		else:
			return token[1]

	def arg2(self):
		token = self.curcmd.split(' ')
		return token[2]

	def mydeal(self):
		for bar in self.rawcommands:
			print bar
			bar = bar.strip('\n')
			bar = re.sub(r'//.*$', '', bar)
			bar = bar.strip()
			if bar != '':
				self.commands.append(bar)
