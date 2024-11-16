#!/usr/bin/env python3

# Simple terminal list selector utility
#
# by Magnetic-Fox, 03-05.07.2024, 18-21.07.2024, 12-16.11.2024
#
# (C)2024 Bartłomiej "Magnetic-Fox" Węgrzyn!

# Imports...
import readchar
import ansi
import sys

# Helper function to shorten the list selector utility's code
def printOut(lcm, rcm, leftCharMod, rightCharMod, maxStrWidth, list, selection):
	# Load element to the temporary variable
	tempString=list[selection]
	# If modifying element's first character
	if lcm:
		# Print element's new first character
		print(leftCharMod,end="")
		# And cut element's first character
		tempString=tempString[1:]
	# If modifying element's last character and its width is at the maximum level
	if rcm and maxStrWidth==len(list[selection]):
		# Then cut element's last character
		tempString=tempString[:-1]
	# Print what's needed
	print(tempString,end="")
	# Fill element's empty part with spaces
	print(" "*(maxStrWidth-len(list[selection])-(1 if rcm else 0)),end="")
	# If modifying element's last character
	if rcm:
		# Print element's new last character
		print(rightCharMod,end="")
	return

# Helper function for unselecting elements
def unSelect(pos_x, pos_y, selection, displayPos, lcm, rcm, leftCharMod, rightCharMod, maxStrWidth, list):
	# Unselect element
	ansi.setNoReverse()
	ansi.setCurPos(pos_x,pos_y+selection-displayPos)
	printOut(lcm,rcm,leftCharMod,rightCharMod,maxStrWidth,list,selection)
	return

# Helper function for selecting elements and executing onSelection function
def selectAndExecute(pos_x, pos_y, selection, displayPos, lcm, rcm, leftCharMod, rightCharMod, maxStrWidth, list, onSelection, adds, placeCursorAtStart, cursorCorrection):
	# Select element
	ansi.setCurPos(pos_x,pos_y+selection-displayPos)
	ansi.setReverse()
	printOut(lcm,rcm,leftCharMod,rightCharMod,maxStrWidth,list,selection)
	ansi.setNoReverse()
	# Execute onSelection function if needed
	if(onSelection!=None):
		onSelection(selection,pos_x+adds,pos_y+selection-displayPos)
		ansi.setCurPos(pos_x+(maxStrWidth if not placeCursorAtStart else 0)+cursorCorrection,pos_y+selection-displayPos)
	return

# Helper function to calculate proper display position
def calculateDisplayPosition(selection, displayPos, s_height, listSize, up=True):
	# Calculate while going up
	if up:
		while selection<displayPos:
			displayPos-=s_height
		if displayPos<0:
			displayPos=0
	# Calculate while going down
	else:
		while selection>=displayPos+s_height:
			displayPos+=s_height
		if(displayPos+s_height-1>=listSize):
			displayPos=listSize-s_height
	# Return calculated display position
	return displayPos

# Helper function to reset/calculate proper selection index
def resetSelectionIndex(selection, list, listSize, up=True):
	# Reset while going up
	if up:
		while list[selection]==None:
			selection-=1
			# Go down if beginning reached
			if selection<0:
				selection=0
				while list[selection]==None:
					selection+=1
					# Stop if end reached
					if selection>=listSize:
						selection=listSize-1
						break
				# And then break
				break
	# Reset while going down
	else:
		while list[selection]==None:
			selection+=1
			# Go up if end reached
			if selection>=listSize:
				selection=listSize-1
				while list[selection]==None:
					selection-=1
					# Stop if beginning reached
					if selection<0:
						selection=0
						break
				# And then break
				break
	# Return reset selection index
	return selection

# LIST SELECTOR UTILITY
#
# ARGUMENTS ARE AS FOLLOWS: list variable (list), x position of list on screen (pos_x),
# y position of list on screen (pos_y), screen width (s_width), screen height (s_height),
# set adding margins (addMargins), margin size (marginSize), character to change on the left side of the element (leftCharMod),
# character to change on the right side of the element (rightCharMod), function to invoke on selection change (onSelection),
# set passing and/or returning coordinates of left side of the selection (leftSideCoordinates),
# set placing cursor at the left side of selection (placeCursorAtStart), cursor setting correction (cursorCorrection),
# selected element index (startIndex), set returning coordinates too (returnCoordinatesToo).
# ONLY FIRST FIVE PARAMETERS ARE REQUIRED (list, pos_x, pos_y, s_width and s_height), OTHERS ARE OPTIONAL.
#
# IMPORTANT: Variables for position on screen starts from 1 (not 0!)
def choice(list, pos_x, pos_y, s_width, s_height, addMargins=True, marginSize=1, leftCharMod='', rightCharMod='', onSelection=None, leftSideCoordinates=True, placeCursorAtStart=False, cursorCorrection=0, startIndex=0, returnCoordinatesToo=False, firstRedrawStartIndexOnly=False):
	# Let's thrown an exception yet at the beginning (if needed)
	if list==None:
		raise TypeError("list is None")
	# Define temporary variables and initialize them
	s_width-=pos_x-1
	s_height-=pos_y-1
	maxStrWidth=0
	selection=startIndex
	displayPos=0
	adds=0
	redrawAll=True
	reset=False
	allNone=True
	once=firstRedrawStartIndexOnly
	list=list[:]
	# Test if leftCharMod is one character long
	if leftCharMod!=None and len(leftCharMod)>1:
		# Throw exception
		raise ValueError("leftCharMod has to be one-character string")
	# Test if rightCharMod is one character long
	elif rightCharMod!=None and len(rightCharMod)>1:
		# Throw exception
		raise ValueError("rightCharMod has to be one-character string")
	else:
		# Let's shorten it
		lcm=(leftCharMod!=None) and (len(leftCharMod)==1)
		rcm=(rightCharMod!=None) and (len(rightCharMod)==1)
	# Store list size in variable
	listSize=len(list)
	# Set the real start index on existing list if selection points to the None
	if selection<len(list) and selection>=0:
		selection=resetSelectionIndex(selection,list,listSize,up=False)
	else:
		selection=0
	# Check if screen position is good
	if selection>=displayPos+s_height:
		displayPos=calculateDisplayPosition(selection,displayPos,s_height,listSize,up=False)
	# Run the list selector utility only on existing list that has at least one element
	if len(list)>0:
		# Test and prepare list elements
		for x in range(len(list)):
			# Check if list is None-only and if it is necessary to reset the selector utility
			if list[x]==None:
				if x==0:
					reset=True
				continue
			else:
				allNone=False
				if reset:
					selection=x
					if selection>s_height-1:
						displayPos=selection
						if displayPos+s_height>len(list):
							displayPos=len(list)-s_height
					reset=False
			# Add margins to the list elements
			if addMargins:
				list[x]=" "*marginSize+list[x]+" "*marginSize
			# Update maximum string width (length)
			if len(list[x])>maxStrWidth:
				maxStrWidth=len(list[x])
			# Truncate too long elements
			if maxStrWidth>s_width:
				maxStrWidth=s_width
				subt=3
				if addMargins:
					subt+=marginSize
				list[x]=list[x][0:s_width-subt]
				list[x]+="..."+" "*marginSize
		# Throw exception (None-only list)
		if allNone:
			raise ValueError("list contains None elements only")
		# Set how much to add to the output coordinates in "on selection" event
		if not leftSideCoordinates:
			adds=maxStrWidth-1
		# Main list selector part
		while not allNone:
			# Full list redraw event
			if redrawAll:
				if not once:
					# Set initial position
					ansi.setCurPos(pos_x,pos_y)
				# Draw elements up to the maximum height
				for x in range(s_height):
					if once:
						if displayPos+x<startIndex:
							continue
						else:
							ansi.setCurPos(pos_x,pos_y+x)
					if x==listSize:
						break
					else:
						if list[displayPos+x]==None:
							if(pos_x>1):
								ansi.setCurPos(pos_x,pos_y+x)
							if x==s_height-1:
								print(" "*maxStrWidth,end="")
							else:
								print(" "*maxStrWidth)
							continue
						if displayPos+x==selection:
							ansi.setReverse()
						if(pos_x>1):
							ansi.setCurPos(pos_x,pos_y+x)
						printOut(lcm,rcm,leftCharMod,rightCharMod,maxStrWidth,list,displayPos+x)
						if x!=s_height-1:
							# Go to the next line
							print("")
						if displayPos+x==selection:
							ansi.setNoReverse()
							# Invoke "on selection" event
							if(onSelection!=None):
								onSelection(selection,pos_x+adds,pos_y+x)
								ansi.setCurPos(pos_x,pos_y+x+1)
							if once:
								once=False
								break
				# Set redraw all task as done
				redrawAll=False
				# Set cursor position after drawing the list
				ansi.setCurPos(pos_x+(maxStrWidth if not placeCursorAtStart else 0)+cursorCorrection,pos_y+selection-displayPos)
			# Flush standard output (which is VERY IMPORTANT!)
			sys.stdout.flush()
			# Read character from the standard input
			inp=readchar.readkey()
			# Go up on the list (one element, 16 elements, get first element of the list)
			if(inp==readchar.key.UP) or (inp==readchar.key.PAGE_UP) or (inp==readchar.key.HOME):
				# Store old selection index
				oldSelection=selection
				# Go up one element
				if inp==readchar.key.UP:
					selection-=1
				# Go up 16 elements
				elif inp==readchar.key.PAGE_UP:
					selection-=16
				# Go up to the first element
				elif inp==readchar.key.HOME:
					selection=0
				# Reset selection to 0 if selection is lower
				if selection<0:
					selection=0
					# If list selection hasn't changed - do nothing
					if oldSelection==selection:
						continue
				# Reset position while on None elements
				selection=resetSelectionIndex(selection,list,listSize)
				# Continue on None
				if list[selection]==None:
					continue
				# Additional test if selection actually not changed
				if oldSelection==selection:
					continue
				# Calculate coordinates of the previous screen and let it be fully redrawn
				if selection<displayPos:
					displayPos=calculateDisplayPosition(selection,displayPos,s_height,listSize)
					redrawAll=True
				# Unselect previously selected element and select currently selected
				else:
					if(oldSelection<listSize) and (s_height>1):
						unSelect(pos_x,pos_y,oldSelection,displayPos,lcm,rcm,leftCharMod,rightCharMod,maxStrWidth,list)
					if(selection-displayPos>=0):
						selectAndExecute(pos_x,pos_y,selection,displayPos,lcm,rcm,leftCharMod,rightCharMod,maxStrWidth,list,onSelection,adds,placeCursorAtStart,cursorCorrection)
			# Go down on the list (one element, 16 elements, get end of the list)
			elif(inp==readchar.key.DOWN) or (inp==readchar.key.PAGE_DOWN) or (inp==readchar.key.END):
				# Store old selection index
				oldSelection=selection
				# Go down one element
				if inp==readchar.key.DOWN:
					selection+=1
				# Go down 16 elements
				elif inp==readchar.key.PAGE_DOWN:
					selection+=16
				# Go down to the last element
				elif inp==readchar.key.END:
					selection=listSize-1
				# Reset selection to the last element if greater or equal
				if selection>=listSize:
					selection=listSize-1
					# If list selection hasn't changed - do nothing
					if oldSelection==selection:
						continue
				# Reset position while on None elements
				selection=resetSelectionIndex(selection,list,listSize,up=False)
				# Continue on None
				if list[selection]==None:
					continue
				# Additional test if selection actually not changed
				if oldSelection==selection:
					continue
				# Calculate coordinates of the previous screen and let it be fully redrawn
				if selection>=displayPos+s_height:
					displayPos=calculateDisplayPosition(selection,displayPos,s_height,listSize,up=False)
					redrawAll=True
				# Unselect previously selected element and select currently selected
				else:
					if(oldSelection>=0) and (pos_y+(oldSelection-displayPos)>=pos_y):
						unSelect(pos_x,pos_y,oldSelection,displayPos,lcm,rcm,leftCharMod,rightCharMod,maxStrWidth,list)
					if(selection-displayPos<s_height):
						selectAndExecute(pos_x,pos_y,selection,displayPos,lcm,rcm,leftCharMod,rightCharMod,maxStrWidth,list,onSelection,adds,placeCursorAtStart,cursorCorrection)
			# Break list selector (selection index is already set)
			elif(inp==readchar.key.ENTER):
				break
	# An error occurred - throw appropriate exception
	else:
		if list==None:
			raise TypeError("list is None")
		elif len(list)==0:
			raise ValueError("list is empty")
		else:
			raise RuntimeError("unknown error occurred")
	# Return selection or throw exception
	if returnCoordinatesToo:
		if selection<0:
			raise ValueError("selection error occurred")
		return selection, pos_x+adds, pos_y+selection-displayPos
	return selection



# EXAMPLE/TEST PART BELOW
# Below are example functions that shows typical usage of this list selector utility

# --------------------------------------------------------------------------------------------

# EXAMPLE ON-SELECTION EVENT FUNCTION
# Input variables as follows: chosen ID, X and Y coordinates of selection (left or right side)
def test(in1,in2,in3):
	ansi.setCurPos(30,2)
	print(str(in1)+","+str(in2)+","+str(in3)+" "*10)
	return

# EXAMPLE/TEST INVOKING FUNCTION
# Input variables can be used to override width and height to be used on terminal
def makeTest(width=80, height=24):
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
	chosen,rx,ry=choice(list,1,1,width,height,onSelection=test,returnCoordinatesToo=True,leftCharMod="[",rightCharMod="]",marginSize=2)
	# Display selection ID
	ansi.clear()
	ansi.setCurPos(1,1)
	print("ID:   "+str(chosen))
	print("X:    "+str(rx))
	print("Y:    "+str(ry))
	# Set wrap around, as probably was before running test
	ansi.setWrapAround()
	# Finish
	return

# AUTORUN PART / EXAMPLE MODE
if __name__ == "__main__":
	makeTest()
