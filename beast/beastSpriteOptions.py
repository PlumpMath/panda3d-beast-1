#! /usr/bin/python
#---------------------------------------------------------------------------#
#- Beast - An Panda3d user interface library - See included "License.txt" - #
#---------------------------------------------------------------------------#
#- Beast, beastSpriteOptions.py manages all options for visual effects of a beastSprite

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
		self.__margin = [0, 0, 0, 0]
		self.__padding = [0, 0, 0, 0]

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
	def setText(self, text):
		self.__text = text
		self._update()

	def setSize(self, left, right, bottom, top):
		self.__size = left, right, bottom, top
		self._update()

	def setBorder(self, border):
		self.__border = border
		self._update()

	def setBorderColor(self, color):
		self.__color = color
		self._update()

	def setStretchingCorners(self, size):
		self.__stretchingCorners = size
		self._update()

	def setBackgroundColor(self, color):
		self.__backgroundColor = color
		self._update()

	def setBackgroundImage(self, path):
		self.__backgroundImage = path
		self._update()

	def setBackgroundTexture(self, texture):
		self.__backgroundTexture = texture
		self._update()

	def setFont(self, font):
		self.__font = font
		self._update()

	def setFontSize(self, size):
		self.__fontSize = size
		self._update()

	def setFontStyle(self, *style):
		self.__fontStyle = style
		self._update()

	def setMargin(self, left, right, bottom, top):
		self.__margin = left, right, bottom, top
		self._update()

	def setMarginLeft(self, left):
		self.__margin[0] = left
		self._update()

	def setMarginRight(self, right):
		self.__margin[1] = right
		self._update()

	def setMarginBottom(self, bottom):
		self.__margin[2] = bottom
		self._update()

	def setMarginTop(self, top):
		self.__margin[3] = top
		self._update()

	def setPadding(self, left, right, bottom, top):
		self.__padding = left, right, bottom, top
		self._update()

	def setPaddingLeft(self, left):
		self.__padding[0] = left
		self._update()

	def setPaddingRight(self, right):
		self.__padding[1] = right
		self._update()

	def setPaddingBottom(self, bottom):
		self.__padding[2] = bottom
		self._update()

	def setPaddingTop(self, top):
		self.__padding[3] = top
		self._update()

	'''
		Get options
	'''
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

