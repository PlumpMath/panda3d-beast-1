#! /usr/bin/python
#---------------------------------------------------------------------------#
#- Beast - An Panda3d user interface library - See included "License.txt" - #
#---------------------------------------------------------------------------#
#- Beast, beastSpriteOptions.py manages all options for visual effects of a beastSprite
from panda3d.core import MouseWatcherRegion

class beastSpriteOptions:
	def __init__(self):
		self.__text = str()
		self.__size = (0, 0, 0, 0)
		self.__color = (0, 0, 0, 1)
		self.__border = 0
		self.__borderColor = (0, 0, 0, 1)
		self.__stretchingCorners = 0
		self.__backgroundColor = (0, 0, 0, 0)
		self.__backgroundImage = ''
		self.__backgroundTexture = None
		self.__font = ''
		self.__fontSize = 12
		self.__fontStyle = ()
		self.__suppressMouse = True
		self.__suppressKeys = False
		self.__margin = [0, 0, 0, 0]
		self.__padding = [0, 0, 0, 0]

	def getSuppressFlags(self):
		suppressFlags = 0
		if self.__suppressMouse:
			suppressFlags |= MouseWatcherRegion.SFMouseButton
			suppressFlags |= MouseWatcherRegion.SFMousePosition
		if self.__suppressKeys:
			suppressFlags |= MouseWatcherRegion.SFOtherButton
		return suppressFlags

	def copyOptionsFrom(self, src):
		b = beastSpriteOptions
		self.setText(b.getText(src))
		self.setSize(*b.getSize(src))
		self.setColor(b.getColor(src))
		self.setBorder(b.getBorder(src))
		self.setBorderColor(b.getBorderColor(src))
		self.setStretchingCorners(b.getStretchingCorners(src))
		self.setBackgroundColor(b.getBackgroundColor(src))
		self.setBackgroundImage(b.getBackgroundImage(src))
		self.setBackgroundTexture(b.getBackgroundTexture(src))
		self.setFont(b.getFont(src))
		self.setFontSize(b.getFontSize(src))
		self.setFontStyle(b.getFontStyle(src))
		self.setMargin(*b.getMargin(src))
		self.setPadding(*b.getPadding(src))

	#- You should inherit and define _update yourself if you need to apply changes
	def _update(self):
		pass

	def hasSize(self):
		s = self.__size
		if s[0] == 0 and s[1] == 0 and s[2] == 0 and s[3] == 0:
			return False
		else:
			return True

	'''
		Set options
	'''
	def setSuppressMouse(self, value):
		a = self.__suppressMouse
		self.__suppressMouse = value
		if a != value:
			self._update()

	def setSuppressKeys(self, value):
		a = self.__suppressKeys
		self.__suppressKeys = value
		if a != value:
			self._update()

	def setText(self, text):
		a = self.__text
		self.__text = text
		if a != text:
			self._update()

	def setSize(self, left, right, bottom, top):
		a = self.__size
		self.__size = left, right, bottom, top
		if a != (left, right, bottom, top):
			self._update()

	def setBorder(self, border):
		a = self.__border
		self.__border = border
		if a != border:
			self._update()

	def setBorderColor(self, color):
		a = self.__borderColor
		self.__borderColor = color
		if a != color:
			self._update()

	def setStretchingCorners(self, size):
		a = self.__stretchingCorners
		self.__stretchingCorners = size
		if a != size:
			self._update()

	def setBackgroundColor(self, color):
		a = self.__backgroundColor
		self.__backgroundColor = color
		if a != color:
			self._update()

	def setBackgroundImage(self, path):
		a = self.__backgroundImage
		self.__backgroundImage = path
		if a != path:
			self._update()

	def setBackgroundTexture(self, texture):
		a = self.__backgroundTexture
		self.__backgroundTexture = texture
		if a != texture:
			self._update()

	def setFont(self, font):
		a = self.__font
		self.__font = font
		if a != font:
			self._update()

	def setFontSize(self, size):
		a = self.__fontSize
		self.__fontSize = size
		if a != size:
			self._update()

	def setFontStyle(self, *style):
		a = self.__fontStyle
		self.__fontStyle = style
		if a != style:
			self._update()

	def setMargin(self, left, right, bottom, top):
		a = self.__margin
		self.__margin = left, right, bottom, top
		if a != (left, right, bottom, top):
			self._update()

	def setMarginLeft(self, left):
		a = self.__margin[0]
		self.__margin[0] = left
		if a != left:
			self._update()

	def setMarginRight(self, right):
		a = self.__margin[1]
		self.__margin[1] = right
		if a != right:
			self._update()

	def setMarginBottom(self, bottom):
		a = self.__margin[2]
		self.__margin[2] = bottom
		if a != bottom:
			self._update()

	def setMarginTop(self, top):
		a = self.__margin[3]
		self.__margin[3] = top
		if a != top:
			self._update()

	def setPadding(self, left, right, bottom, top):
		a = self.__padding
		self.__padding = left, right, bottom, top
		if a != (left, right, bottom, top):
			self._update()

	def setPaddingLeft(self, left):
		a = self.__padding[0]
		self.__padding[0] = left
		if a != left:
			self._update()

	def setPaddingRight(self, right):
		a = self.__padding[1]
		self.__padding[1] = right
		if a != right:
			self._update()

	def setPaddingBottom(self, bottom):
		a = self.__padding[2]
		self.__padding[2] = bottom
		if a != bottom:
			self._update()

	def setPaddingTop(self, top):
		a = self.__padding[3]
		self.__padding[3] = top
		if a != top:
			self._update()

	'''
		Get options
	'''
	def getSuppressMouse(self):
		return self.__suppressMouse

	def getSuppressKeys(self):
		return self.__suppressKeys

	def getText(self):
		return self.__text

	def getSize(self):
		return self.__size

	def getColor(self):
		return self.__color

	def getBorder(self):
		return self.__border

	def getBorderColor(self):
		return self.__borderColor

	def getStretchingCorners(self):
		return self.__stretchingCorners

	def getBackgroundColor(self):
		return self.__backgroundColor

	def getBackgroundImage(self):
		return self.__backgroundImage

	def getBackgroundTexture(self):
		return self.__backgroundTexture

	def getFont(self):
		return self.__font

	def getFontSize(self):
		return self.__fontSize

	def getFontStyle(self):
		return self.__fontStyle

	def getMargin(self):
		return self.__margin

	def getMarginLeft(self):
		return self.__margin[0]

	def getMarginRight(self):
		return self.__margin[1]

	def getMarginBottom(self):
		return self.__margin[2]

	def getMarginTop(self):
		return self.__margin[3]

	def getPadding(self):
		return self.__padding

	def getPaddingLeft(self):
		return self.__padding[0]

	def getPaddingRight(self):
		return self.__padding[1]

	def getPaddingBottom(self):
		return self.__padding[2]

	def getPaddingTop(self):
		return self.__padding[3]

