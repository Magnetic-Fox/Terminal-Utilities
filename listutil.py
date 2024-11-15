#!/usr/bin/env python3

# Simple terminal list selector utility
#
# by Magnetic-Fox, 03-05.07.2024, 18-21.07.2024, 12-15.11.2024
#
# (C)2024 Bartłomiej "Magnetic-Fox" Węgrzyn!

# Imports...
import readchar
import ansi
import sys

# LIST SELECTOR UTILITY
#
# ARGUMENTS ARE AS FOLLOWS: list variable (list), x position of list on screen (pos_x),
# y position of list on screen (pos_y), screen width (s_width), screen height (s_height),
# set adding margins (addMargins), margin size (marginSize), function to invoke on selection change (onSelection),
# set passing and/or returning coordinates of left side of the selection (leftSideCoordinates),
# set placing cursor at the left side of selection (placeCursorAtStart), cursor setting correction (cursorCorrection),
# selected element index (startIndex), set returning coordinates too (returnCoordinatesToo).
#
# IMPORTANT: Variables for position on screen starts from 1 (not 0!)
def choice(list, pos_x, pos_y, s_width, s_height, addMargins=True, marginSize=1, onSelection=None, leftSideCoordinates=True, placeCursorAtStart=False, cursorCorrection=0, startIndex=0, returnCoordinatesToo=False):
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
	list=list[:]

	# Set the real start index on list if selection points to the None
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

	# Run the list selector utility only on existing list that has at least one element
	if(list!=None) and (len(list)>0):
		# Test and prepare list elements
		listSize=len(list)
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

		# Set to terminate selector and return error (None-only list)
		if allNone:
			selection=-1

		# Set how much to add to the output coordinates in "on selection" event
		if not leftSideCoordinates:
			adds=maxStrWidth-1

		# Main list selector part
		while not allNone:
			# Full list redraw event
			if redrawAll:
				# Set initial position
				ansi.setCurPos(pos_x,pos_y)
				# Draw elements up to the maximum height
				for x in range(s_height):
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
						if x==s_height-1:
							print(list[displayPos+x]+" "*(maxStrWidth-len(list[displayPos+x])),end="")
						else:
							print(list[displayPos+x]+" "*(maxStrWidth-len(list[displayPos+x])))
						if displayPos+x==selection:
							ansi.setNoReverse()
							# Invoke "on selection" event
							if(onSelection!=None):
								onSelection(selection,pos_x+adds,pos_y+x)
								ansi.setCurPos(pos_x,pos_y+x+1)
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

				# Additional test if selection actually not changed
				if oldSelection==selection:
					continue

				# Calculate coordinates of the previous screen and let it be fully redrawn
				if selection<displayPos:
					while selection<displayPos:
						displayPos-=s_height
					if displayPos<0:
						displayPos=0
					redrawAll=True

				# Unselect previously selected element and select currently selected
				else:
					if(oldSelection<listSize) and (s_height>1):
						ansi.setNoReverse()
						ansi.setCurPos(pos_x,pos_y+(oldSelection-displayPos))
						print(list[oldSelection]+" "*(maxStrWidth-len(list[oldSelection])),end="")
					if(selection-displayPos>=0):
						ansi.setCurPos(pos_x,pos_y+(selection-displayPos))
						ansi.setReverse()
						print(list[selection]+" "*(maxStrWidth-len(list[selection])),end="")
						ansi.setNoReverse()
						if(onSelection!=None):
							onSelection(selection,pos_x+adds,pos_y+(selection-displayPos))
							ansi.setCurPos(pos_x+(maxStrWidth if not placeCursorAtStart else 0)+cursorCorrection,pos_y+(selection-displayPos))

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

				# Additional test if selection actually not changed
				if oldSelection==selection:
					continue

				# Calculate coordinates of the previous screen and let it be fully redrawn
				if selection>=displayPos+s_height:
					while selection>=displayPos+s_height:
						displayPos+=s_height
					if(displayPos+s_height-1>=listSize):
						displayPos=listSize-s_height
					redrawAll=True

				# Unselect previously selected element and select currently selected
				else:
					if(oldSelection>=0) and (pos_y+(oldSelection-displayPos)>=pos_y):
						ansi.setNoReverse()
						ansi.setCurPos(pos_x,pos_y+(oldSelection-displayPos))
						print(list[oldSelection]+" "*(maxStrWidth-len(list[oldSelection])),end="")
					if(selection-displayPos<s_height):
						ansi.setCurPos(pos_x,pos_y+(selection-displayPos))
						ansi.setReverse()
						print(list[selection]+" "*(maxStrWidth-len(list[selection])),end="")
						ansi.setNoReverse()
						if(onSelection!=None):
							onSelection(selection,pos_x+adds,pos_y+(selection-displayPos))
							ansi.setCurPos(pos_x+(maxStrWidth if not placeCursorAtStart else 0)+cursorCorrection,pos_y+(selection-displayPos))

			# Break list selector (selection index is already set)
			elif(inp==readchar.key.ENTER):
				break

	# Set error if list has no elements or does not exist (got None)
	else:
		selection=-1

	# Return selection or error (and coordinates, if chosen to)
	if returnCoordinatesToo:
		if selection<0:
			# Return 0, 0 coordinates (wrong, in fact) on error
			return selection, 0, 0
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
	chosen,rx,ry=choice(list,1,1,width,height,onSelection=test,returnCoordinatesToo=True)

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
