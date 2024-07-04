#!/usr/bin/env python3

# Procedure for gathering terminal screen size
#
# Magnetic-Fox, 30.06.2024

import readchar

def getTermSize():
	input=""
	print("\x1b7\x1b[999;999H\x1b[6n\x1b8\x1bM")
	while True:
		input2=readchar.readkey()
		input+=input2
		if(input2[-1]=='R') or (input2[-1]==readchar.key.ENTER):
			break

	if(input.find(readchar.key.ESC)>0):
		input=input[input.find(readchar.key.ESC):]

	if (len(input)>2) and (input[0]==readchar.key.ESC and input[1]=="[" and input[-1]=='R'):
		try:
			rows=input[2:input.index(';')]
			cols=input[input.index(';')+1:input.index('R')]
			output=(int(cols),int(rows))
		except:
			output=None
	else:
		output=None

	return output
