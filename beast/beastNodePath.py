#! /usr/bin/python
#---------------------------------------------------------------------------#
#- Beast - An Panda3d user interface library - See included "License.txt" - #
#---------------------------------------------------------------------------#
#- Beast, beastNodePath.py inherits from NodePath and is functionally the same, only these changes:
#- attachNewNode returns a beastNodePath in place of a reguler NodePath instance
#- beastNodePath has setRequiresUpdate and getRequiresUpdate, that contain the state of weather
#- this node should require a new frame to be rendered by beast
#- calling any setEtc on this beastNodePath also update setRequiresUpdate() to be True
from panda3d.core import NodePath

class beastNodePath(NodePath):
	def __init__(self, *args, **kwargs):
		NodePath.__init__(self, *args, **kwargs)
		self.setPythonTag('beast', self)
		self.setTag('beastRequiresUpdate', '1')
	#	self.__requiresUpdate = True

	def attachNewNode(self, *args):
		if type(args[0]) == str or type(args[0]) == unicode:
			tmp = beastNodePath(args[0])
			tmp.reparentTo(self)
			return tmp
		else:
			return NodePath.attachNewNode(self, *args)

	def setX(self, *args, **kwargs):
		old = self.getX()
		NodePath.setX(self, *args, **kwargs)
		new = self.getX()
		if old != new:
			self.setRequiresUpdate(True)

	def setY(self, *args, **kwargs):
		old = self.getY()
		NodePath.setY(self, *args, **kwargs)
		new = self.getY()
		if old != new:
			self.setRequiresUpdate(True)

	def setZ(self, *args, **kwargs):
		old = self.getZ()
		NodePath.setZ(self, *args, **kwargs)
		new = self.getZ()
		if old != new:
			self.setRequiresUpdate(True)

	def setPos(self, *args, **kwargs):
		old = self.getPos()
		NodePath.setPos(self, *args, **kwargs)
		new = self.getPos()
		if old != new:
			self.setRequiresUpdate(True)

	def setHpr(self, *args, **kwargs):
		old = self.getHpr()
		NodePath.setHpr(self, *args, **kwargs)
		new = self.getHpr()
		if old != new:
			self.setRequiresUpdate(True)

	def setScale(self, *args, **kwargs):
		old = self.getScale()
		NodePath.setScale(self, *args, **kwargs)
		new = self.getScale()
		if old != new:
			self.setRequiresUpdate(True)

	def reparentTo(self, *args, **kwargs):
		old = self.getParent()
		NodePath.reparentTo(self, *args, **kwargs)
		new = self.getParent()
		if old != new:
			self.setRequiresUpdate(True)

	def setRequiresUpdate(self, value):
		if value:
			self.setTag('beastRequiresUpdate', '1')
		else:
			self.setTag('beastRequiresUpdate', '0')
			for np in self.findAllMatches('**/=beastRequiresUpdate=1'):
				np.setTag('beastRequiresUpdate', '0')

	def getRequiresUpdate(self):
		if self.getTag('beastRequiresUpdate') == '1':
			return True
	#	print self.find('**/=beastRequiresUpdate=1')
		if self.find('**/=beastRequiresUpdate=1'):
			return True
		return False

