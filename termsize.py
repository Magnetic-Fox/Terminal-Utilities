#!/usr/bin/env python3

# Procedure for gathering terminal screen size
#
# Magnetic-Fox, 30.06.2024, 05.07.2024
#
# (C)2024 Bartłomiej "Magnetic-Fox" Węgrzyn

import ansi
import readchar

# Procedure for gathering terminal's screen size
def getTermSize():
	input=""

	# Do the algorithm - set cursor position to 999x999 and then ask terminal for its position (which will automatically be changed to the possible maximum)
	ansi.saveCurPos()
	ansi.setCurPos(999,999)
	ansi.askCurPos()	# Terminal will answer automatically, regardless of what comes next
	ansi.restoreCurPos()
	ansi.reverseLineFeed()	# I put reverse line feed here, because, for some strange reason,
	print("")		# the whole code works only when the next line is passed

	while True:
		input2=readchar.readkey()
		input+=input2
		# You'll be able to interrupt this code if terminal haven't responded - just press ENTER
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
