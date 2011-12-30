#! /usr/bin/python
#---------------------------------------------------------------------------#
#- Beast - An Panda3d user interface library - See included "License.txt" - #
#---------------------------------------------------------------------------#
#- Beast, beastButton.py manages several beastSprite's and creates a user-interaction able area
from panda3d.core import PGButton
from direct.showbase.DirectObject import DirectObject
from beastSpriteOptions import *
from beastNodePath import *
from beastSprite import *

#- A Button by default has one state, named 'default'
#- You can change visual options for all states of the button by using button.setEtc
#- You can change visual options for one specific state by calling button.getState(name).setEtc
#- There can be up to four states, 'default', 'hover', 'click', and 'disabled'
#- By default all of the states have the same visual look
#- Only after changing one of the state's specific looks will you see a change
#- Thus, you can apply a size to all states by calling button.setSize(l, r, b, t)
#- Or you can apply a size to just one state ('click') by doing the following:
#- calling button.getState('click').setSize(l, r, b, t)

class beastButton(beastNodePath, beastSpriteOptions, DirectObject):
	def __init__(self, name):
		beastNodePath.__init__(self, PGButton(name))
		beastSpriteOptions.__init__(self)
		DirectObject.__init__(self)
		self.setPythonTag('beastButton', self)
		self.states = {}
		self.getState('default') #- Install a default sprite
		self.__lastState = 'default'
	#	taskMgr.add(self.__checkStateTask, '%s-checkStateTask' % hex(id(self)))

		b = beast
		for ev in (b.enter, b.exit, b.within, b.without, b.leftPress, b.centerPress, b.rightPress, b.leftClick, b.centerClick, b.rightClick, b.leftRelease, b.centerRelease, b.rightRelease, b.wheelUp, b.wheelDown):
			self.bind(ev, self.__foo)

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
		self.accept(eventType + self.node().getId(), self._fakeBind, extraArgs = [command, extraArgs, mwParam])

	def unbind(self, eventType):
		self.ignore(eventType + self.node().getId())

	def _fakeBind(self, command, extraArgs, mwParam, mwp):
		if mwParam:
			extraArgs.append(mwp)
		#- Generally speaking, this only occurs on enter/exit lclick, rclick, cclick, 
		command(*extraArgs)
		self.__checkState()

	def __getattribute__(self, name):
		if (name.startswith('set') or name.startswith('get')) and name in dir(beastSpriteOptions):
			def callme(*args, **kwargs):
				func = getattr(beastSpriteOptions, name)
				func(self, *args, **kwargs)
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
		assert state == 'default' or state == 'hover' or state == 'click' or state == 'disabled'
		if state in self.states:
			pass
		else:
			#- name = mybutton-click, mybutton-hover, mybutton-etc
			sprite = beastSprite(self.getName() + '-' + state)
			sprite.copyOptionsFrom(self)
			self.states[state] = sprite
		sprites = {}
		for key, value in self.states.items():
			if value:
				sprites[key] = value
		#- Sprites has no None values now
		default = sprites.get('default')
		hover = sprites.get('hover')
		click = sprites.get('click')
		disabled = sprites.get('disabled')
		#- Buttons can have any number of states, only if called for though
		if default and hover and click and disabled:
			self.node().setup(default, click, hover, disabled)
		elif default and hover and click:
			self.node().setup(default, click, hover)
		elif default and hover:
			self.node().setup(default, default, hover)
		else:
			self.node().setup(default)
		return self.states[state] #- Finally actually give them the sprite..

	def setDisabled(self, value):
		if value:
			self.node().setActive(False)
		else:
			self.node().setActive(True)

	def getDisabled(self):
		if self.getCurrentStateName() == 'disabled':
			return True
		else:
			return False

	def remove(self):
		self.ignoreAll()
		NodePath.remove(self)
