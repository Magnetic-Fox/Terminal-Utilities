#!/usr/bin/env python3

# Very simple (most used) ANSI escape codes implementation
# by Magnetic-Fox, 28.04.2024, 02.05.2024, 04.05.2024
#
# (C)2024 Bartłomiej "Magnetic-Fox" Węgrzyn!

def output(input, ret=False):
	if(ret):
		return input
	else:
		print(input,end="")
		return

def fullBlock():
	return "█"

def darkShade():
	return "▓"

def mediumShade():
	return "▒"

def lightShade():
	return "░"

def Bell():
	return "\x07"

def Enquiry():
	return "\x05"

def MakeBell(ret=False):
	return output(Bell(),ret)

def MakeEnquiry(ret=False):
	return output(Enquiry(),ret)

def CSI():
	return "\x1b["

def setFgColor(input, ret=False):
	return output(CSI()+str(30+input)+"m",ret)

def setBgColor(input, ret=False):
	return setFgColor(10+input,ret)

def setCurPos(x, y, ret=False):
	return output(CSI()+str(y)+";"+str(x)+"H",ret)

def reset(ret=False):
	return output(CSI()+"0m",ret)

def clear(ret=False):
	out=output(CSI()+"2J",ret)
	out2=setCurPos(1,1,ret)
	if(ret):
		return out+out2
	return

def setBold(ret=False):
	return output(CSI()+"1m",ret)

def setNoBold(ret=False):
	return output(CSI()+"22m",ret)

def setUnderline(ret=False):
	return output(CSI()+"4m",ret)

def setNoUnderline(ret=False):
	return output(CSI()+"24m",ret)

def setReverse(ret=False):
	return output(CSI()+"7m",ret)

def setNoReverse(ret=False):
	return output(CSI()+"27m",ret)

def setBlinking(ret=False):
	return output(CSI()+"5m",ret)

def setNoBlinking(ret=False):
	return output(CSI()+"25m",ret)

def setWrapAround(ret=False):
	return output(CSI()+"?7h",ret)

def setNoWrapAround(ret=False):
	return output(CSI()+"?7l",ret)
