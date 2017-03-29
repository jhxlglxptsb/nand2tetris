import re

A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2

class parser(object):
    def __init__(self, myfile):
    	self.file = re.open(myfile)
    	self.rawcommands = file.readlines()
    	self.commands = []
   		self.mydeal()
    	self.start = 0
    	self.curcmd = ''
    	self.symbol = ''

    def run(self):
    	if hasMoreCommands():
    		self.curcmd = self.advance()

    def hasMoreCommands(self):
    	return self.start<len(self.commands)

    def advance(self):
    	return self.commands[self.start++]

    def commandType(self):
    	if self.curcmd.find('@'):
    		return A_COMMAND
    	elif self.curcmd.find('('):
    		return L_COMMAND
    	else:
    		return C_COMMAND

    def symbol(self):
    	return re.sub(r'\(|\)|@', '', self.curcmd)

    def dest(self):
    	if '=' in self.curcmd:
    		pattern = re.compile("(.*)\=")
    		res = pattern.search(self.curcmd).groups()
    		return res[0]
    	else:
    		return 'null'

    def comp(self):
    	if '=' in self.curcmd and ';' in self.curcmd:
    		pattern = re.compile("\=(.*);")
    		res = pattern.search(self.curcmd).groups()
    		return res[0]
    	elif '=' in self.curcmd:
    		pattern = re.compile("\=(.*)$")
    		res = pattern.search(self.curcmd).groups()
    		return res[0]
    	elif ';' in self.curcmd:
    		pattern = re.compile("(.*);")
    		res = pattern.search(self.curcmd).groups()
    		return res[0]
    	else
    		return self.curcmd

    def jump(self):
    	if ';' in self.curcmd:
    		pattern = re.compile(";(.*)$")
    		res = pattern.search(self.curcmd).groups()
    		return res[0]
    	else:
    		return 'null'


    def mydeal(self):
    	for bar in self.rawcommands:
    		bar = bar.strip('\n')
    		bar = bar.replace(' ', '')
    		bar = re.sub(r'//.*$', '', bar)
    		if bar != '':
    			self.commands.append(bar)