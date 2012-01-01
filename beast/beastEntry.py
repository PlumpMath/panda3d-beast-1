#! /usr/bin/python
#---------------------------------------------------------------------------#
#- Beast - An Panda3d user interface library - See included "License.txt" - #
#---------------------------------------------------------------------------#
#- Beast, beastEntry.py manages several beastSprite's to create an user-input area
from panda3d.core import PGButton
from direct.showbase.DirectObject import DirectObject
from beastSpriteOptions import *
from beastNodePath import *
from beastSprite import *

class beastEntry(beastNodePath, beastSpriteOptions, DirectObject):
	def __init__(self, name):
		beastNodePath.__init__(self, PGButton(name))
		beastSpriteOptions.__init__(self)
		DirectObject.__init__(self)
		self.setPythonTag('beastEntry', self)
		self.states = {}
		self.__focus = False
		self.getState('default') #- Install a default sprite
		self.__lastState = 'default'
		b = beast
		for ev in (b.enter, b.exit, b.within, b.without, b.leftPress, b.centerPress, b.rightPress, b.leftClick, b.centerClick, b.rightClick, b.leftRelease, b.centerRelease, b.rightRelease, b.wheelUp, b.wheelDown):
			self.bind(ev, self.__foo)
		self.setSuppressKeys(True)
		self.getCurrentState().getTextNode().setMaxRows(9)
		self.accept('keystroke-'+self.node().getId(), self.__keystroke)

	def _update(self):
		self.node().setSuppressFlags(self.getSuppressFlags())
		self.setRequiresUpdate(True)

	def __keystroke(self, mwp):
		if self.getFocus() == False or mwp.hasKeycode() == False:
			return
		code = mwp.getKeycode()
		if code == 8: #- backspace
			self.setText(self.getText()[:-1])
		elif code == 13: #- enteer
			self.setText(self.getText() + '\n')
		else:
			if self.getCurrentState().getTextNode().hasCharacter(code) == False:
				print ':beastEntry: TextNode.hasCharacter(%s) != True' % code
				return
			key = chr(code)
			print repr(key), code
			self.setText(self.getText() + key)

	def __foo(self):
		pass

	def __checkState(self):
		state = self.getCurrentStateName()
		if self.__lastState == state:
			pass
		else:
			self.setRequiresUpdate(True) #- It changed, so we need a new render
			self.__lastState = state

	def bind(self, eventType, command, extraArgs = [], mwParam = False):
		self.accept(eventType + self.node().getId(), self._fakeBind, extraArgs = [eventType, command, extraArgs, mwParam])

	def unbind(self, eventType):
		self.ignore(eventType + self.node().getId())
		self.bind(eventType, self.__foo)

	def _fakeBind(self, eventType, command, extraArgs, mwParam, mwp):
		if mwParam:
			extraArgs.append(mwp)
		#- Generally speaking, this only occurs on enter/exit lclick, rclick, cclick, 
		command(*extraArgs)
		if eventType == beast.leftClick:
			self.setFocus(True)
		if eventType == beast.exit:
			self.accept('mouse1-up', self.setFocus, [False])
		if eventType == beast.enter:
			self.ignore('mouse1-up')
		self.__checkState()

	def __getattribute__(self, name):
		if (name.startswith('set') or name.startswith('get')) and name in dir(beastSpriteOptions):
			def callme(*args, **kwargs):
				func = getattr(beastSpriteOptions, name)
				ret = func(self, *args, **kwargs)
				if name.startswith('get'):
					return ret #- No need to go to children
				for key, value in self.states.items():
					func = getattr(value, name)
					func(*args, **kwargs)
			return callme
		elif name in ['getHeight', 'getWidth', 'getSize']:
			func = getattr(self.getCurrentState(), name)
			return func
		else:
			return object.__getattribute__(self, name)

	def align(self, mode, otherNode, inner = False, relative = beast.point2d):
		pos = self.getCurrentState().align(mode, otherNode.getCurrentState(), inner, relative, returnPosition = True)
		if pos.getX() != 0:
			self.setX(relative, pos.getX() + otherNode.getX(relative))
		else:
			self.setZ(relative, pos.getZ() + otherNode.getZ(relative))

	def getCurrentStateName(self):
		state = self.node().getState()
		states = {0: 'default', 1: 'click', 2: 'hover', 3: 'disabled'}
		return states[state]

	def getCurrentState(self):
		return self.getState(self.getCurrentStateName())

	def getState(self, state):
		assert state == 'default' or state == 'hover' or state == 'active' or state == 'disabled'
		if state in self.states:
			pass
		else:
			sprite = beastSprite(self.getName() + '-' + state)
			sprite.copyOptionsFrom(self)
			self.states[state] = sprite
		self._updateForFocus()
		return self.states[state] #- Finally actually give them the sprite..

	def setDisabled(self, value):
		if value:
			self.node().setActive(False)
		else:
			self.node().setActive(True)
		self.__checkState()

	def getDisabled(self):
		if self.getCurrentStateName() == 'disabled':
			return True
		else:
			return False

	def _updateForFocus(self):
		sprites = {}
		for key, value in self.states.items():
			if value:
				sprites[key] = value
		#- Sprites has no None values now
		default = sprites.get('default')
		hover = sprites.get('hover')
		active = sprites.get('active')
		disabled = sprites.get('disabled')

		ar = [default, active, hover, disabled]
		if ar[1] == None:
			ar[1] = default
		if ar[2] == None:
			ar[2] = default
		if ar[3] == None:
			ar[3] = default
		if self.__focus:
			self.node().setup(ar[1], ar[1], ar[1], ar[3])
			self.node().setFocus(True)
		#	for bt in base.buttonThrowers:
		#		bt = bt.node()
		#		bt.setPrefix(str(self.node().getId())+'-')
		else:
			self.node().setup(ar[0], ar[1], ar[2], ar[3])
			self.node().setFocus(False)
		#	for bt in base.buttonThrowers:
		#		bt = bt.node()
		#		bt.setPrefix('')

	def setFocus(self, value):
		if value != self.__focus:
			self.__focus = value
			self._updateForFocus()
			self.setRequiresUpdate(True)

	def getFocus(self):
		return self.__focus

	def remove(self):
		self.ignoreAll()
		NodePath.remove(self)


