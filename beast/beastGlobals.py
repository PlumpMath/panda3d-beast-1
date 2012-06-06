'''
    This file is part of Beast, a Panda3D user interface library.
    See included "License.txt"
'''
from direct.showbase.DirectObject import DirectObject
from panda3d.core import ConfigVariableDouble, ConfigVariableBool, PGTop, PGButton, MouseButton, CardMaker, TransparencyAttrib
from beastNodePath import *
import __builtin__

class _beastGlobals(DirectObject):
	enter = PGButton.getEnterPrefix()
	exit = PGButton.getExitPrefix()
	within = PGButton.getWithinPrefix()
	without = PGButton.getWithoutPrefix()
	leftPress = PGButton.getPressPrefix() + MouseButton.one().getName() + '-'  
	centerPress = PGButton.getPressPrefix() + MouseButton.two().getName() + '-'
	rightPress = PGButton.getPressPrefix() + MouseButton.three().getName() + '-'
	leftClick = PGButton.getClickPrefix() + MouseButton.one().getName() + '-'
	centerClick = PGButton.getClickPrefix() + MouseButton.two().getName() + '-'
	rightClick = PGButton.getClickPrefix() + MouseButton.three().getName() + '-'
	leftRelease = PGButton.getReleasePrefix() + MouseButton.one().getName() + '-'
	centerRelease = PGButton.getReleasePrefix() + MouseButton.two().getName() + '-'
	rightRelease = PGButton.getReleasePrefix() + MouseButton.three().getName() + '-'
	wheelUp = PGButton.getPressPrefix() + MouseButton.wheelUp().getName() + '-'
	wheelDown = PGButton.getPressPrefix() + MouseButton.wheelDown().getName() + '-'
	def __init__(self, taskMgr, base):
		DirectObject.__init__(self)
		self.taskMgr = taskMgr
		self.base = base
		self.setupPoint2d()

		self.beastPointSize = ConfigVariableDouble('beast-point-size', 1.0).getValue()
		self.beastPointSizeAuto = ConfigVariableBool('beast-point-size-auto', False).getValue()
		self.beastRenderBruteForce = ConfigVariableBool('beast-render-brute-force', False).getValue()
		self.beastRenderDebug = ConfigVariableBool('beast-render-debug', False).getValue()

		self.setPointSize(self.beastPointSize, update = False)
		self.setPointSizeAuto(self.beastPointSizeAuto, update = False)
		self.accept('window-event', self.windowEvent)
		self.originalResolution = (float(self.base.win.getXSize()), float(self.base.win.getYSize()))

		self.buffer = None
		#- If bruteForce == False then we will setup beast frame rendering system
		if self.beastRenderBruteForce == False:
			self._setupTextureBuffer()
			taskMgr.add(self.renderTask, 'beastRender', sort = -100000000)

		self.windowEvent()

	def _setupTextureBuffer(self):
		if self.buffer:
			self.card.remove()
			self.camera2d.remove()
			self.base.graphicsEngine.removeWindow(self.buffer)

		self.buffer = self.base.win.makeTextureBuffer("beastBuffer", self.base.win.getXSize(), self.base.win.getYSize())
		self.buffer.setActive(True)
		self.buffer.getTexture().setOrigFileSize(self.base.win.getXSize(), self.base.win.getYSize())

		self.camera2d = self.base.makeCamera2d(self.buffer)
		self.camera2d.reparentTo(self.point2d.getParent())

		cm = CardMaker('beastDisplay')
		cm.setFrame(-1, 1, -1, 1)
		cm.setUvRange(self.buffer.getTexture())
		self.card = self.base.render2d.attachNewNode(cm.generate())
		self.card.setTransparency(TransparencyAttrib.MAlpha)
		self.card.setTexture(self.buffer.getTexture())

	def renderTask(self, task):
		if self.point2d.getRequiresUpdate():
			debug = self.beastRenderBruteForce == False and self.beastRenderDebug == True
			if debug:
				print ':beast::render'
			self.buffer.setActive(True)
			self.point2d.setRequiresUpdate(False)
		else:
			self.buffer.setActive(False)
		return task.cont

	def setupPoint2d(self):
		fakeRender2d = NodePath('render2d')
		fakeRender2d.setDepthTest(False)
		fakeRender2d.setDepthWrite(False)
		fakeRender2d.setMaterialOff(True)
		fakeRender2d.setTwoSided(True)

		self.point2d = beastNodePath(PGTop('point2d'))
		self.point2d.reparentTo(fakeRender2d)
		self.point2d.node().setMouseWatcher(self.base.mouseWatcherNode)

		self.p2dTopLeft = self.point2d.attachNewNode('p2dTopLeft')
		self.p2dTopRight = self.point2d.attachNewNode('p2dTopRight')
		self.p2dTopCenter = self.point2d.attachNewNode('p2dTopCenter')

		self.p2dCenterLeft = self.point2d.attachNewNode('p2dCenterLeft')
		self.p2dCenterRight = self.point2d.attachNewNode('p2dCenterRight')

		self.p2dBottomLeft = self.point2d.attachNewNode('p2dBottomLeft')
		self.p2dBottomRight = self.point2d.attachNewNode('p2dBottomRight')
		self.p2dBottomCenter = self.point2d.attachNewNode('p2dBottomCenter')

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

	''' Data folder '''
	def getDataFolder(self):
		if sys.platform.startswith('win'):
			slash = '\\'
		else:
			slash = '/'
		point = __file__.rindex(slash)
		f = __file__[:point] + slash + 'data' + slash
		return Filename().fromOsSpecific(f).getFullpath()

	''' Destroy beast now '''
	def destroy(self):
		self.ignoreAll()


class beastGlobals(_beastGlobals):
	''' Inherit from _beastGlobals if you hate '__builtins__' after calling beast.destroy() '''
	def __init__(self):
		_beastGlobals.__init__(self,
		taskMgr = taskMgr,
		base = base,
		)
		#- You must set the "keystroke" event
		base.buttonThrowers[0].node().setKeystrokeEvent('keystroke')
		__builtin__.point2d = self.point2d
		__builtin__.p2dTopLeft = self.p2dTopLeft
		__builtin__.p2dTopRight = self.p2dTopRight
		__builtin__.p2dTopCenter = self.p2dTopCenter
		__builtin__.p2dCenterLeft = self.p2dCenterLeft
		__builtin__.p2dCenterRight = self.p2dCenterRight
		__builtin__.p2dBottomLeft = self.p2dBottomLeft
		__builtin__.p2dBottomRight = self.p2dBottomRight
		__builtin__.p2dBottomCenter = self.p2dBottomCenter

	def destroy(self):
		_beastGlobals.destroy(self)
		__builtin__.beast = None
		__builtin__.point2d = None
		__builtin__.p2dTopLeft = None
		__builtin__.p2dTopRight = None
		__builtin__.p2dTopCenter = None
		__builtin__.p2dCenterLeft = None
		__builtin__.p2dCenterRight = None
		__builtin__.p2dBottomLeft = None
		__builtin__.p2dBottomRight = None
		__builtin__.p2dBottomCenter = None


if hasattr(__builtins__, 'beast') == False:
	if __name__ == '__main__':
		import direct.directbase.DirectStart
	__builtin__.beast = beastGlobals()


''' display smileys on each relative point '''
if __name__ == '__main__':
	''' middle '''
	smiley = loader.loadModel('smiley')
	smiley.reparentTo(point2d)
	smiley.setScale(50) #- 100 pixels

	''' top section '''
	smiley = loader.loadModel('smiley')
	smiley.reparentTo(p2dTopLeft)
	smiley.setScale(50) #- 100 pixels
	smiley.setX(50)
	smiley.setZ(-50)

	smiley = loader.loadModel('smiley')
	smiley.reparentTo(p2dTopRight)
	smiley.setScale(50) #- 100 pixels
	smiley.setX(-50)
	smiley.setZ(-50)

	smiley = loader.loadModel('smiley')
	smiley.reparentTo(p2dTopCenter)
	smiley.setScale(50) #- 100 pixels
	smiley.setZ(-50)

	''' middle '''
	smiley = loader.loadModel('smiley')
	smiley.reparentTo(p2dCenterLeft)
	smiley.setScale(50) #- 100 pixels
	smiley.setX(50)

	smiley = loader.loadModel('smiley')
	smiley.reparentTo(point2d)
	smiley.setScale(50) #- 100 pixels

	smiley = loader.loadModel('smiley')
	smiley.reparentTo(p2dCenterRight)
	smiley.setScale(50) #- 100 pixels
	smiley.setX(-50)

	''' bottom section '''
	smiley = loader.loadModel('smiley')
	smiley.reparentTo(p2dBottomLeft)
	smiley.setScale(50) #- 100 pixels
	smiley.setX(50)
	smiley.setZ(50)

	smiley = loader.loadModel('smiley')
	smiley.reparentTo(p2dBottomCenter)
	smiley.setScale(50) #- 100 pixels
	smiley.setZ(50)

	smiley = loader.loadModel('smiley')
	smiley.reparentTo(p2dBottomRight)
	smiley.setScale(50) #- 100 pixels
	smiley.setX(-50)
	smiley.setZ(50)

	base.accept('1', beast.setPointSize, [1.0])
	base.accept('2', beast.setPointSize, [1.5])
	base.accept('3', beast.setPointSize, [2.0])
	base.accept('enter', beast.togglePointSizeAuto)
	run()
