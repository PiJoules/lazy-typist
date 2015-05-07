#!/usr/bin/python

import sys


class Coord:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def distance(self, coord):
		dx = abs(self.x - coord.x)
		dy = abs(self.y - coord.y)
		return dx + dy

class Keyboard:
	keyrows = ["qwertyuiop", "asdfghjkl ", "^zxcvbnm ^", "   #####  "]

	def __init__(self):
		self.kb = {}
		for y, row in enumerate(self.keyrows):
			for x, char in enumerate(row):
				self.kb[char] = Coord(x, y)

	def getClosestCoord(self, hand, char):
		dx = 0
		char = char.lower()
		charCoord = self.kb[char]
		if char == " ":
			char = "#"
			distances = [0]*4
			charCoord = self.kb[char]
			for i in range(len(distances)):
				tempCoord = Coord(charCoord.x - i, charCoord.y)
				distances[i] = hand.coord.distance(tempCoord)
				if i != 0 and distances[i] < distances[i-1]:
					dx = i
		elif char == "^":
			distances = [0]*10
			for i in range(len(distances)):
				tempCoord = Coord(charCoord.x - i, charCoord.y)
				distances[i] = hand.coord.distance(tempCoord)
				if i != 0 and distances[i] < distances[i-9]:
					dx = i

		return Coord(charCoord.x - dx, charCoord.y)

	def getEffort(self, hand, char):
		char = char.lower()
		if char == " ":
			char = "#"
		charCoord = self.kb[char]
		distance = 1000000 # some arbitary high value greater than largest distance on keyboard
		if char == "#":
			for i in range(4):
				tempCoord = Coord(charCoord.x - i, charCoord.y)
				distance = min(distance, hand.coord.distance(tempCoord))
		elif char == "^":
			distance = min(hand.coord.distance(charCoord), hand.coord.distance( Coord(charCoord.x - 9, charCoord.y) ))
		else:
			distance = hand.coord.distance(charCoord)
		return distance

class Hand:
	def __init__(self, x, y, name):
		self.coord = Coord(x, y)
		self.name = name

	def moveTo(self, x, y):
		self.coord.x = x
		self.coord.y = y

	def moveTo(self, coord):
		self.coord = coord

	def __str__(self):
		return self.name + " hand"

def printMovement(c, hand, effort):
	print c, ": Use ", hand, " (Effort: ", effort, ")"

def findPathToEnd(string, kb):
	startIndex = 0
	nextChar = string[startIndex]
	leftHand, rightHand = None, None
	if nextChar.isupper():
		nextChar = nextChar.lower()
		leftHand = Hand(0,2,"left")
		rightHand = Hand(kb.kb[nextChar].x, kb.kb[nextChar].y, "right")
		startIndex += 1
	else:
		leftHand = Hand(kb.kb[nextChar].x, kb.kb[nextChar].y, "left")
		startIndex += 1
		nextChar = string[startIndex]
		rightHand = Hand(kb.kb[nextChar].x, kb.kb[nextChar].y, "right")
		startIndex += 1

	totalEffort = 0

	for nextChar in string:
		leftHandEffort = kb.getEffort(leftHand, nextChar)
		rightHandEffort = kb.getEffort(rightHand, nextChar)

		if nextChar.isupper():
			leftHandToShift = kb.getEffort(leftHand, "^")
			rightHandToShift = kb.getEffort(rightHand, "^")
			if leftHandToShift+rightHandEffort < rightHandToShift+leftHandEffort:
				leftHand.moveTo(kb.getClosestCoord(leftHand, "^"))
				rightHand.moveTo(kb.getClosestCoord(rightHand, nextChar))
				printMovement("^", leftHand, leftHandToShift)
				printMovement(nextChar, rightHand, rightHandEffort)
				totalEffort += leftHandToShift + rightHandEffort
			else:
				rightHand.moveTo(kb.getClosestCoord(rightHand, "^"))
				leftHand.moveTo(kb.getClosestCoord(leftHand, nextChar))
				printMovement("^", rightHand, rightHandToShift)
				printMovement(nextChar, leftHand, leftHandEffort)
				totalEffort += rightHandToShift + leftHandEffort
		else:
			if leftHandEffort < rightHandEffort:
				leftHand.moveTo(kb.getClosestCoord(leftHand, nextChar))
				printMovement(nextChar, leftHand, leftHandEffort)
				totalEffort += leftHandEffort
			else:
				rightHand.moveTo(kb.getClosestCoord(rightHand, nextChar))
				printMovement(nextChar, rightHand, rightHandEffort)
				totalEffort += rightHandEffort

	print "Total effort: ", totalEffort

if __name__ == "__main__":
	kb = Keyboard()
	for i in range(1,len(sys.argv)):
		arg = sys.argv[i]
		print arg
		findPathToEnd(arg, kb)
		print ""