#!/usr/bin/env python3

# Simple terminal list utility
#
# by Magnetic-Fox, 03-05.07.2024, 18.07.2024
#
# (C)2024 Bartłomiej "Magnetic-Fox" Węgrzyn!

import readchar
import ansi

# List selector utility
# Arguments are as follows: list variable, x position of screen, y position of screen, screen width, screen height,
# set margins, margin size, function to invoke on selection change, set returning coordinates of left side of the selection,
# start index (selected element)

# IMPORTANT: Position variables starts from 1 (not 0!)
def choice(list, pos_x, pos_y, s_width, s_height, addMargins=True, marginSize=1, onSelection=None, leftSideCoords=True, startIndex=0):
	s_width-=pos_x-1
	s_height-=pos_y-1
	maxStrWidth=0
	selection=startIndex
	displayPos=0
	adds=0
	redrawAll=True
	reset=False
	allNone=True
	list=list[:]

	if (selection<len(list)) and (selection>=0):
		while list[selection]==None:
			selection+=1
			if selection>=len(list):
				selection=startIndex
				while list[selection]==None:
					selection-=1
					if selection<0:
						selection=0
						break
				break
	else:
		selection=0

	if(list!=None) and (len(list)>0):
		listSize=len(list)
		for x in range(len(list)):
			if list[x]==None:
				if x==0:
					reset=True
				continue
			else:
				allNone=False
				if reset:
					#displayPos=x
					selection=x
					if selection>s_height-1:
						displayPos=selection
						if displayPos+s_height>len(list):
							displayPos=len(list)-s_height
					reset=False
			if addMargins:
				list[x]=" "*marginSize+list[x]+" "*marginSize
			if len(list[x])>maxStrWidth:
				maxStrWidth=len(list[x])
			if maxStrWidth>s_width:
				maxStrWidth=s_width
				subt=3
				if addMargins:
					subt+=marginSize
				list[x]=list[x][0:s_width-subt]
				list[x]+="..."+" "*marginSize
		if allNone:
			return -1
		if not leftSideCoords:
			adds=maxStrWidth-1
		while True:
			if redrawAll:
				ansi.setCurPos(pos_x,pos_y)
				for x in range(s_height):
					if x==listSize:
						break
					else:
						if list[displayPos+x]==None:
							if(pos_x>1):
								ansi.setCurPos(pos_x,pos_y+x)
							if x==s_height-1:
								print(" "*maxStrWidth,end="")
								ansi.setCurPos(pos_x,pos_y+x-1)
								print("")
							else:
								print(" "*maxStrWidth)
							continue
						if displayPos+x==selection:
							ansi.setReverse()
						if(pos_x>1):
							ansi.setCurPos(pos_x,pos_y+x)
						if x==s_height-1:
							print(list[displayPos+x]+" "*(maxStrWidth-len(list[displayPos+x])),end="")
							ansi.setCurPos(pos_x,pos_y+x-1)
							print("")
						else:
							print(list[displayPos+x]+" "*(maxStrWidth-len(list[displayPos+x])))
						if displayPos+x==selection:
							ansi.setNoReverse()
							if(onSelection!=None):
								onSelection(selection,pos_x+adds,pos_y+x)
								ansi.setCurPos(pos_x,pos_y+x+1)
				redrawAll=False
			inp=readchar.readkey()
			if(inp==readchar.key.UP) or (inp==readchar.key.PAGE_UP) or (inp==readchar.key.HOME):
				oldSelection=selection
				if inp==readchar.key.UP:
					selection-=1
				elif inp==readchar.key.PAGE_UP:
					selection-=16
				elif inp==readchar.key.HOME:
					selection=0
				if selection<0:
					selection=0
				while list[selection]==None:
					selection-=1
					if selection<0:
						selection=0
						while list[selection]==None:
							selection+=1
							if selection>=listSize:
								selection=listSize-1
								break
						break
				if list[selection]==None:
					continue
				if selection<displayPos:
					while selection<displayPos:
						displayPos-=s_height
					if displayPos<0:
						displayPos=0
					redrawAll=True
				else:
					if(oldSelection<listSize) and (s_height>1):
						ansi.setNoReverse()
						ansi.setCurPos(pos_x,pos_y+(oldSelection-displayPos))
						if pos_y+(oldSelection-displayPos)>=s_height:
							print(list[oldSelection]+" "*(maxStrWidth-len(list[oldSelection])),end="")
							ansi.setCurPos(pos_x,s_height-2)
							print("")
						else:
							print(list[oldSelection]+" "*(maxStrWidth-len(list[oldSelection])))
					if(selection-displayPos>=0):
						ansi.setCurPos(pos_x,pos_y+(selection-displayPos))
						ansi.setReverse()
						if pos_y+(selection-displayPos)>=s_height:
							print(list[selection]+" "*(maxStrWidth-len(list[selection])),end="")
							ansi.setCurPos(pos_x,s_height-2)
							print("")
						else:
							print(list[selection]+" "*(maxStrWidth-len(list[selection])))
						ansi.setNoReverse()
						if(onSelection!=None):
							onSelection(selection,pos_x+adds,pos_y+(selection-displayPos))
							ansi.setCurPos(pos_x,pos_y+(selection-displayPos)+1)
			elif(inp==readchar.key.DOWN) or (inp==readchar.key.PAGE_DOWN) or (inp==readchar.key.END):
				oldSelection=selection
				if inp==readchar.key.DOWN:
					selection+=1
				elif inp==readchar.key.PAGE_DOWN:
					selection+=16
				elif inp==readchar.key.END:
					selection=listSize-1
				if selection>=listSize:
					selection=listSize-1
				while list[selection]==None:
					selection+=1
					if selection>=listSize:
						selection=listSize-1
						while list[selection]==None:
							selection-=1
							if selection<0:
								selection=0
								break
						break
				if list[selection]==None:
					continue
				if selection>=displayPos+s_height:
					while selection>=displayPos+s_height:
						displayPos+=s_height
					if(displayPos+s_height-1>=listSize):
						displayPos=listSize-s_height
					redrawAll=True
				else:
					if(oldSelection>=0) and (pos_y+(oldSelection-displayPos)>=pos_y):
						ansi.setNoReverse()
						ansi.setCurPos(pos_x,pos_y+(oldSelection-displayPos))
						if pos_y+(oldSelection-displayPos)==s_height:
							print(list[oldSelection]+" "*(maxStrWidth-len(list[oldSelection])),end="")
							ansi.setCurPos(pos_x,s_height-1)
							print("")
						else:
							print(list[oldSelection]+" "*(maxStrWidth-len(list[oldSelection])))
					if(selection-displayPos<s_height):
						ansi.setCurPos(pos_x,pos_y+(selection-displayPos))
						ansi.setReverse()
						if pos_y+(selection-displayPos):
							print(list[selection]+" "*(maxStrWidth-len(list[selection])),end="")
							ansi.setCurPos(pos_x,s_height-1)
							print("")
						else:
							print(list[selection]+" "*(maxStrWidth-len(list[selection])))
						ansi.setNoReverse()
						if(onSelection!=None):
							onSelection(selection,pos_x+adds,pos_y+(selection-displayPos))
							ansi.setCurPos(pos_x,pos_y+(selection-displayPos)+1)
			elif(inp==readchar.key.ENTER):
				break
	else:
		selection=-1
	return selection

# Input variables as follows: chosen ID, X and Y coordinates of selection (left or right side)
def test(in1,in2,in3):
	ansi.setCurPos(30,2)
	print(str(in1)+","+str(in2)+","+str(in3)+" "*10)
	return

# Test function
def makeTest():
	# Prepare test
	list=["1",None,None,"2"]

	# Insert some empty values at the beginning of the list
	for x in range(1,100):
		list+=[None]

	# Insert some strings and empty values
	for x in range(1,2001):
		list+=[str(x)]
		if x%6==0:
			list+=[None]

	# Insert some empty values at the end of the list
	for x in range(1,100):
		list+=[None]

	# Prepare output terminal
	ansi.clear()
	ansi.setNoWrapAround()
	ansi.setCurPos(30,1)

	# Make some header
	print("ID,X,Y")

	# Invoke list selector and store selection in "chosen" variable
	chosen=choice(list,1,1,80,24,onSelection=test)

	# Display selection ID
	ansi.clear()
	ansi.setCurPos(1,1)
	print("Chosen ID: "+str(chosen))

	# Set wrap around, as probably was before running test
	ansi.setWrapAround()

	return

# Autorun
if __name__ == "__main__":
	makeTest()
