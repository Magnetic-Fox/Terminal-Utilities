#!/usr/bin/env python3

# Very simple (most used) ANSI escape codes implementation
# by Magnetic-Fox, 28.04.2024, 02-04.05.2024, 30.06.2024, 05.07.2024, 18.07.2024
#
# (C)2024 Bartłomiej "Magnetic-Fox" Węgrzyn!

import sys

# Global variable for using HyperTerminal convention of interpreting colors
hyperColors=False

# Encoding and decoding code pages configuration
def configureEncodings(inputEnc=None, outputEnc=None):
	inEnc=None
	outEnc=None
	if(inputEnc!=None):
		try:
			sys.stdin.reconfigure(encoding=inputEnc, errors="replace")
			inEnc=inputEnc
		except:
			pass
	if(outputEnc!=None):
		try:
			sys.stdout.reconfigure(encoding=outputEnc, errors="replace")
			outEnc=outputEnc
		except:
			pass
	return (inEnc, outEnc)

# Output ANSI controlling string (or print it, which is default)
def output(input, ret=False):
	if(ret):
		return input
	else:
		print(input,end="")
		return

# Full block (semi-graphic sign)
def fullBlock():
	return "█"

# Dark shade (semi-graphic sign)
def darkShade():
	return "▓"

# Medium shade (semi-graphic sign)
def mediumShade():
	return "▒"

# Light shade (semi-graphic sign)
def lightShade():
	return "░"

# Bell code
def Bell():
	return "\x07"

# Enquiry code
def Enquiry():
	return "\x05"

# Output bell
def MakeBell(ret=False):
	return output(Bell(),ret)

# Output enquiry
def MakeEnquiry(ret=False):
	return output(Enquiry(),ret)

# Control Sequence Introducer code
def CSI():
	return "\x1b["

# Escape code
def ESC():
	return "\x1b"

# Simplest version of setting foreground color (0-7, 60-67)
def setFgColor(input, ret=False):
	return output(CSI()+str(30+input)+"m",ret)

# Simplest version of setting background color (0-7, 60-67)
def setBgColor(input, ret=False):
	return setFgColor(10+input,ret)

# Set foreground color with translation (color codes 0-15)
def setFgColorT(color, ret=False):
	global hyperColors
	part=None
	if(color>7):
		if(hyperColors):
			color-=8
			part=setBold(ret) # This does the trick
		else:
			color+=52         # + 60 - 8
	elif(hyperColors):
		part=setNoBold()
	if part==None:
		return setFgColor(color,ret)
	else:
		return part+setFgColor(color,ret)

# Set background color with translation (color codes 0-15)
def setBgColorT(color, ret=False):
	global hyperColors
	if(color>7):
		if(hyperColors):
			color-=8    # There aren't any trick for that, unfortunatelly
		else:
			color+=52 # + 60 - 8
	return setBgColor(color,ret)

# Set cursor position
def setCurPos(x, y, ret=False):
	return output(CSI()+str(y)+";"+str(x)+"H",ret)

# Reset terminal
def reset(ret=False):
	return output(CSI()+"0m",ret)

# Clear terminal's screen
def clear(ret=False):
	out=output(CSI()+"2J",ret)
	out2=setCurPos(1,1,ret)
	if(ret):
		return out+out2
	return

# Set bold text
def setBold(ret=False):
	return output(CSI()+"1m",ret)

# Set no bold text
def setNoBold(ret=False):
	return output(CSI()+"22m",ret)

# Set underlined text
def setUnderline(ret=False):
	return output(CSI()+"4m",ret)

# Set no underlined text
def setNoUnderline(ret=False):
	return output(CSI()+"24m",ret)

# Set reverse video
def setReverse(ret=False):
	return output(CSI()+"7m",ret)

# Set no reverse video
def setNoReverse(ret=False):
	return output(CSI()+"27m",ret)

# Set blinking text
def setBlinking(ret=False):
	return output(CSI()+"5m",ret)

# Set no blinking text
def setNoBlinking(ret=False):
	return output(CSI()+"25m",ret)

# Set automatic line wrap after exceeding line
def setWrapAround(ret=False):
	return output(CSI()+"?7h",ret)

# Set no automatic line wrap after exceeding line
def setNoWrapAround(ret=False):
	return output(CSI()+"?7l",ret)

# Make terminal save its cursor's position
def saveCurPos(ret=False):
	return output(ESC()+"7",ret)

# Make terminal restore its cursor's position
def restoreCurPos(ret=False):
	return output(ESC()+"8",ret)

# Ask terminal for its cursor's position
def askCurPos(ret=False):
	return output(CSI()+"6n",ret)

# Make reverse line feed (shortly, caret one line up)
def reverseLineFeed(ret=False):
	return output(ESC()+"M",ret)

# Set hypercolors state
def setHyperColors(state):
	global hyperColors
	hyperColors=state
	return hyperColors

# Get hypercolors state
def getHyperColors():
	global hyperColors
	return hyperColors
