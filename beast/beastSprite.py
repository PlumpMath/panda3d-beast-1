#! /usr/bin/python
#---------------------------------------------------------------------------#
#- Beast - An Panda3d user interface library - See included "License.txt" - #
#---------------------------------------------------------------------------#
#- Beast, beastSprite.py creates a beastSprite NodePath that can be resized dynamically
from panda3d.core import TextNode, Point3, TransparencyAttrib
from beastSpriteOptions import *
from beastNodePath import *

class beastSprite(beastSpriteOptions, beastNodePath):
	def __init__(self, name):
		beastSpriteOptions.__init__(self)
		beastNodePath.__init__(self, TextNode(name))
		self.setPythonTag('beastSprite', self)
		self.setTransparency(TransparencyAttrib.MAlpha)
		self._update()

	#- Align this node to (otherNode)'s (mode), and optionally to (otherNode)'s (inner) (mode)
	#- This respects this sprite's Margin, which spaces this sprite away from the other sprite
	#- in all cases
	#- This respects the other nodes Padding, which spaces this sprite away from the inside of
	#- the other node
	def align(self, mode, otherNode, inner = False, relative = beast.point2d, returnPosition = False):
		self.setRequiresUpdate(True)
		assert otherNode.hasPythonTag('beastSprite'), 'otherNode must be a valid sprite! got %s instead' % otherNode
		otherNode = otherNode.getPythonTag('beastSprite')
		assert otherNode != self, 'otherNode must be a valid sprite! got self instance instead' % otherNode
		leftOne, rightOne, bottomOne, topOne = self.getSize()
		mLeftOne, mRightOne, mBottomOne, mTopOne = self.getMargin()
		pLeftOne, pRightOne, pBottomOne, pTopOne = self.getPadding()
		leftTwo, rightTwo, bottomTwo, topTwo = otherNode.getSize()
		mLeftTwo, mRightTwo, mBottomTwo, mTopTwo = otherNode.getMargin()
		pLeftTwo, pRightTwo, pBottomTwo, pTopTwo = otherNode.getPadding()
		x = 0
		z = 0
		if mode == 'left':
			if inner:
				x = leftTwo - leftOne + mLeftOne + pLeftTwo
			else:
				x = leftTwo - rightOne - mRightOne
		if mode == 'right':
			if inner:
				x = rightTwo - rightOne - mRightOne - pRightTwo
			else:
				x = rightTwo - leftOne + mLeftOne
		if mode == 'bottom':
			if inner:
				z = bottomTwo - bottomOne + mBottomOne + pBottomTwo
			else:
				z = bottomTwo - topOne - mBottomOne
		if mode == 'top':
			if inner:
				z = topTwo - topOne - mTopOne - pTopTwo
			else:
				z = topTwo - bottomOne + mTopOne
		if returnPosition:
			if x != 0:
				return Point3(x, 0, 0)
			else:
				return Point3(0, 0, z)
		if x:
			self.setX(relative, otherNode.getX(relative) + x)
		if z:
			self.setZ(relative, otherNode.getZ(relative) + z)

	def _update(self):
		self.setRequiresUpdate(True)
		tn = self.getTextNode()

		if self.getBackgroundImage():
			self.setTexture(loader.loadTexture(self.getBackgroundImage()))

		if self.getStretchingCorners() and self.getBackgroundImage():
			ts = float(self.getTexture().getXSize()) #- How do we assume X size?
			sc = float(self.getStretchingCorners())
			s = self.getScale()[0]
			tn.setCardBorder(sc / s, sc / ts)

		tn.setText(self.getText())
		if tn.getText() == '':
			tn.setText(' ')

		''' Font section '''
		if self.getFont():
			tn.setFont(loader.loadFont(self.getFont()))

		fontStyle = self.getFontStyle()
		if 'italic' in fontStyle:
			tn.setSlant(0.3)
		else:
			tn.setSlant(0.0)

		if 'smallcaps' in fontStyle:
			tn.setSmallCaps(True)
		else:
			tn.setSmallCaps(False)

		if 'shadow' in fontStyle:
			tn.setShadow(0.05, 0.05)
			tn.setShadowColor(0, 0, 0, 1)
		else:
			tn.setShadow(0, 0)

		tn.setTextColor(*self.getColor())

		''' Background section '''
		tn.setCardColor(*self.getBackgroundColor())
		if tn.getText() != ' ':
			self.setScale(self.getFontSize())
			p = self.getStretchingCorners() / self.getScale()[0]
			#- This is a fix for whitespace bug in TextNode
			#- See this forum post for more information:
			#- http://www.panda3d.org/forums/viewtopic.php?p=80596#80596
			#- Oddly enough, TextNode.calcWidth() calculates the width properly
			#- tn.setCardAsMargin(p, p, p, p) <- Should have worked
			#- Instead we built it our self
			spaces = 0
			if tn.getText().endswith(' ') or tn.getText().endswith('\t'):
				txt = tn.getText().replace('\t', ' ' * int(tn.getTabWidth()))
				spaces = float(len(txt) - len(txt.rstrip(' ')))
				spaces = tn.calcWidth(' ') * spaces
			tn.setCardAsMargin(p, p + spaces, p, p)

		if self.hasSize():
			tn.setCardActual(*beastSpriteOptions.getSize(self))

		''' Border section '''
		if self.getBorder() > 0:
			if self.hasSize():
				tn.setFrameActual(*beastSpriteOptions.getSize(self))
			tn.setFrameLineWidth(self.getBorder())
			tn.setFrameColor(self.getBorderColor())

	def getHeight(self, scaled = True):
		size = self.getSize(scaled)
		return size[3] - size[2]

	def getWidth(self, scaled = True):
		size = self.getSize(scaled)
		return size[1] - size[0]

	def getSize(self, scaled = True):
		s = self.getScale()[0]
		l, r, b, t = self.getTextNode().getCardActual()
		if scaled:
			l, r, b, t = l*s, r*s, b*s, t*s
		return l, r, b, t

	def getTextNode(self):
		return self.node()

if __name__ == '__main__':
	s = beastSprite('name')
