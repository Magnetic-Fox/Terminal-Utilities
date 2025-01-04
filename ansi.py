#!/usr/bin/env python3

# Very simple (most used) ANSI escape codes implementation
# by Magnetic-Fox, 28.04-20.07.2024, 04.01.2025
#
# (C)2024-2025 Bartłomiej "Magnetic-Fox" Węgrzyn!

import sys

# Global variable for using HyperTerminal convention of interpreting colors
hyperColors=False

# State variables
fgColor=None
bgColor=None
fgColorT=True
bgColorT=True
lockFgColorT=False
bold=None
underline=None
reverse=None
blinking=None

# Helper function - simple none relay to shorten code
def noneStringRelay(input):
	return input if input!=None else ""

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
def setFgColor(input, ret=False, noSet=False):
	global fgColor, fgColorT
	if not noSet:
		fgColor=input
		fgColorT=False
	return output(CSI()+str(30+input)+"m",ret)

# Simplest version of setting background color (0-7, 60-67)
def setBgColor(input, ret=False, noSet=False):
	global bgColor, bgColorT
	if not noSet:
		bgColor=input
		bgColorT=False
	return setFgColor(10+input,ret,True)

# Set foreground color with translation (color codes 0-15)
def setFgColorT(color, ret=False):
	global hyperColors, fgColor, fgColorT, lockFgColorT
	fgColor=color
	fgColorT=True
	part=None
	if(color>7):
		if(hyperColors):
			color-=8
			part=setBold(ret)	# This does the trick
		else:
			color+=52		# + 60 - 8
	elif(hyperColors):
		if not lockFgColorT:
			lockFgColorT=True
			part=setNoBold(ret)
			lockFgColorT=False
	if part==None:
		return setFgColor(color,ret,True)
	else:
		return part+setFgColor(color,ret,True)

# Set background color with translation (color codes 0-15)
def setBgColorT(color, ret=False):
	global hyperColors, bgColor, bgColorT
	bgColor=color
	bgColorT=True
	if(color>7):
		if(hyperColors):
			color-=8	# There aren't any trick for that, unfortunatelly
		else:
			color+=52	# + 60 - 8
	return setBgColor(color,ret,True)

# Set cursor position
def setCurPos(x, y, ret=False):
	return output(CSI()+str(y)+";"+str(x)+"H",ret)

# Reset terminal font's settings
def reset(ret=False, resetStates=True):
	global fgColor, bgColor, fgColorT, bgColorT, bold, underline, reverse, blinking
	if resetStates:
		fgColor=None
		bgColor=None
		fgColorT=True
		bgColorT=True
		bold=None
		underline=None
		reverse=None
		blinking=None
	return output(CSI()+"0m",ret)

# Restore saved font states
def restoreStates(ret=False):
	global fgColor, bgColor, fgColorT, bgColorT, bold, underline, reverse, blinking
	tempOutput=""
	if fgColor!=None:
		if fgColorT:
			tempOutput+=noneStringRelay(setFgColorT(fgColor,ret))
		else:
			tempOutput+=noneStringRelay(setFgColor(fgColor,ret))
	if bgColor!=None:
		if bgColorT:
			tempOutput+=noneStringRelay(setBgColorT(bgColor,ret))
		else:
			tempOutput+=noneStringRelay(setBgColor(bgColor,ret))
	if bold!=None and bold:
		tempOutput+=noneStringRelay(setBold(ret))
	if underline!=None and underline:
		tempOutput+=noneStringRelay(setUnderline(ret))
	if reverse!=None and reverse:
		tempOutput+=noneStringRelay(setReverse(ret))
	if blinking!=None and blinking:
		tempOutput+=noneStringRelay(setBlinking(ret))
	return output(tempOutput,ret)

# Clear terminal's screen
def clear(ret=False):
	out=output(CSI()+"2J",ret)
	out2=setCurPos(1,1,ret)
	if(ret):
		return out+out2
	return

# Reset and restore states
def resetAndRestoreStates(ret=False):
	out=reset(ret,False)
	out2=restoreStates(ret)
	if(ret):
		return out+out2
	return

# Set bold text
def setBold(ret=False):
	global bold
	bold=True
	return output(CSI()+"1m",ret)

# Set no bold text (classic way)
def setNoBold(ret=False):
	global bold
	bold=False
	return resetAndRestoreStates(ret)

# Set no bold text (modern way)
def setNoBold_modern(ret=False):
	global bold
	bold=False
	return output(CSI()+"22m",ret)

# Set underlined text
def setUnderline(ret=False):
	global underline
	underline=True
	return output(CSI()+"4m",ret)

# Set no underlined text (classic way)
def setNoUnderline(ret=False):
	global underline
	underline=False
	return resetAndRestoreStates(ret)

# Set no underlined text (modern way)
def setNoUnderline_modern(ret=False):
	global underline
	underline=False
	return output(CSI()+"24m",ret)

# Set reverse video
def setReverse(ret=False):
	global reverse
	reverse=True
	return output(CSI()+"7m",ret)

# Set no reverse video (classic way)
def setNoReverse(ret=False):
	global reverse
	reverse=False
	return resetAndRestoreStates(ret)

# Set no reverse video (modern way)
def setNoReverse_modern(ret=False):
	global reverse
	reverse=False
	return output(CSI()+"27m",ret)

# Set blinking text
def setBlinking(ret=False):
	global blinking
	blinking=True
	return output(CSI()+"5m",ret)

# Set no blinking text (classic way)
def setNoBlinking(ret=False):
	global blinking
	blinking=False
	return resetAndRestoreStates(ret)

# Set no blinking text (modern way)
def setNoBlinking_modern(ret=False):
	global blinking
	blinking=False
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
