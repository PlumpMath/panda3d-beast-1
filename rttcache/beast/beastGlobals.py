#!/usr/bin/python
#encoding: utf-8
'''
    This file is part of the Panda3D user interface library, Beast.
    See included "License.txt"
'''
from direct.showbase.DirectObject import DirectObject
from panda3d.core import ConfigVariableDouble, ConfigVariableBool, PGTop, PGButton, MouseButton, CardMaker, TransparencyAttrib
import __builtin__


class beastGlobals(DirectObject):
	def __init__(self, base):
		DirectObject.__init__(self)
		self.base = base

        '''
            Setup point2d NodePath
        '''
		self.point2d = NodePath(PGTop('point2d'))
		self.point2d.node().setMouseWatcher(self.base.mouseWatcherNode)
		self.point2d.setDepthTest(False)
		self.point2d.setDepthWrite(False)
		self.point2d.setMaterialOff(True)
		self.point2d.setTwoSided(True)

		self.p2dTopLeft = self.point2d.attachNewNode('p2dTopLeft')
		self.p2dTopRight = self.point2d.attachNewNode('p2dTopRight')
		self.p2dTopCenter = self.point2d.attachNewNode('p2dTopCenter')

		self.p2dCenterLeft = self.point2d.attachNewNode('p2dCenterLeft')
		self.p2dCenterRight = self.point2d.attachNewNode('p2dCenterRight')

		self.p2dBottomLeft = self.point2d.attachNewNode('p2dBottomLeft')
		self.p2dBottomRight = self.point2d.attachNewNode('p2dBottomRight')
		self.p2dBottomCenter = self.point2d.attachNewNode('p2dBottomCenter')

		self.beastPointSize = ConfigVariableDouble('beast-point-size', 1.0).getValue()
		self.beastPointSizeAuto = ConfigVariableBool('beast-point-size-auto', False).getValue()
		self.beastRenderCache = ConfigVariableBool('beast-render-cache', True).getValue()
		self.beastRenderDebug = ConfigVariableBool('beast-render-debug', False).getValue()

		self.setPointSize(self.beastPointSize, update = False)
		self.setPointSizeAuto(self.beastPointSizeAuto, update = False)
		self.accept('window-event', self.windowEvent)
		self.originalResolution = (float(self.base.win.getXSize()), float(self.base.win.getYSize()))

	def getMousePos(self):
		md = self.win.getPointer(0)
		x = md.getX()
		y = md.getY()
		p = self.point2d.getRelativePoint(self.pixel2d, (x, 0, -y))
		return p.getX(), p.getZ() 

	def hasMouse(self):
		return self.mouseWatcherNode.hasMouse()

	def getAbsolutePointSize(self):
		fakePointSize = None
		if self.getPointSizeAuto():
			oldX, oldY = self.originalResolution
			newX, newY = float(self.win.getXSize()), float(self.win.getYSize())
			ratio = newY / oldY
			fakePointSize = ratio

		if self.getPointSizeAuto():
			ps = fakePointSize
		else:
			ps = self.getPointSize()
		return ps

	def windowEvent(self, win = None):
		ps = self.getAbsolutePointSize()
		x = self.base.win.getXSize()
		y = self.base.win.getYSize()

		xActual = (x / ps)
		yActual = (y / ps)
		self.point2d.setScale(2.0 / xActual, 1.0, 2.0 / yActual)

		#- Finish actuals
		self.p2dTopLeft.setPos(-xActual / 2.0, 1.0, yActual / 2.0)
		self.p2dTopRight.setPos(xActual / 2.0, 1.0, yActual / 2.0)
		self.p2dTopCenter.setPos(0, 1.0, yActual / 2.0)

		self.p2dCenterLeft.setPos(-xActual / 2.0, 1.0, 0.0)
		self.p2dCenterRight.setPos(xActual / 2.0, 1.0, 0.0)

		self.p2dBottomLeft.setPos(-xActual / 2.0, 1.0, -yActual / 2.0)
		self.p2dBottomRight.setPos(xActual / 2.0, 1.0, -yActual / 2.0)
		self.p2dBottomCenter.setPos(0, 1.0, -yActual / 2.0)

		if self.beastRenderBruteForce == False:
			debug = self.beastRenderBruteForce == False and self.beastRenderDebug == True
			bx = self.buffer.getTexture().getOrigFileXSize()
			by = self.buffer.getTexture().getOrigFileYSize()
			cx = self.base.win.getXSize()
			cy = self.base.win.getYSize()
			if bx != cx or by != by:
				if debug:
					print ':beast::render::resolutionChanged from(%s, %s) to(%s, %s)' % (bx, by, cx, cy)
				self._setupTextureBuffer()
		messenger.send('beast.windowEvent')

	''' Point size '''
	def getPointSize(self):
		return self.pointSize

	def setPointSize(self, value, update = True):
		self.pointSize = float(value)
		if update:
			self.update()

	''' Point size auto resolution '''
	def setPSAutoResolution(self, x, y):
		self.originalResolution = (float(base.win.getXSize()), float(base.win.getYSize()))

	def getPSAutoResolution(self):
		return self.originalResolution

	''' Point size auto '''
	def setPointSizeAuto(self, value, update = True):
		self.pointSizeAuto = bool(value)
		if update:
			self.update()

	def getPointSizeAuto(self):
		return self.pointSizeAuto

	def togglePointSizeAuto(self):
		if self.getPointSizeAuto():
			self.setPointSizeAuto(False)
		else:
			self.setPointSizeAuto(True)

