#!/usr/bin/python
#encoding: utf-8
'''
    This file is part of the Panda3D user interface library, Beast.
    See included "License.txt"
'''
from panda3d.core import NodePath, ConfigVariableBool, CardMaker, TransparencyAttrib, PGTop
from direct.showbase.DirectObject import DirectObject
from Sprite import *

SpriteCollectionCounter = 0

class SpriteCollection(NodePath, DirectObject):
    def __init__(self, name, dynamic = False):
        NodePath.__init__(self, PGTop(name))
        DirectObject.__init__(self)
        self.setPythonTag('SpriteCollection', self)

        global SpriteCollectionCounter
        SpriteCollectionCounter += 1
        self.__id = int(SpriteCollectionCounter)

        self.node().setMouseWatcher(base.mouseWatcherNode)
        self.setDepthTest(False)
        self.setDepthWrite(False)
        self.setMaterialOff(True)
        self.setTwoSided(True)

        self.__lastRender = globalClock.getFrameCount()
        self.buffer = None
        self.__dynamic = dynamic
        self.__beastRenderCache = ConfigVariableBool('beast-render-cache', True).getValue()
        self.__beastForceNewFrame = ConfigVariableBool('beast-force-new-frame', True).getValue()
        self.__beastDebug = ConfigVariableBool('beast-debug', False).getValue()
        if self.__dynamic == False and self.__beastRenderCache == True:
            self.fakeRender2d = NodePath('fakeRender2d-%s-%s' % (self.__id, self.getName()))
            self.reparentTo(self.fakeRender2d)

            self._setupTextureBuffer()
            self.accept('beastCollectionUpdate', self._update)
            base.taskMgr.add(self._update, 'updateTask-%s-%s' % (self.__id, self.getName()), sort = -1000)
        else:
            self.reparentTo(render2d)

    def wasRequestedDynamic(self):
        return self.__dynamic

    def isDynamic(self):
        if self.__beastRenderCache == False:
            return False
        else:
            return self.__dynamic

    def addSprite(self, sprite):
        if type(sprite) == str or type(sprite) == unicode:
            sprite = Sprite(sprite)
        sprite.reparentTo(self)
        return sprite

    def _setupTextureBuffer(self):
        if self.buffer:
            self.card.remove()
            self.camera2d.remove()
            base.graphicsEngine.removeWindow(self.buffer)

        self.buffer = base.win.makeTextureBuffer("textureBuffer-%s-%s" % (self.__id, self.getName()), base.win.getXSize(), base.win.getYSize())
        self.buffer.setSort(100)
        self.buffer.setOneShot(True)
        self.buffer.setActive(True)
        self.buffer.getTexture().setOrigFileSize(base.win.getXSize(), base.win.getYSize())

        self.camera2d = base.makeCamera2d(self.buffer)
        self.camera2d.reparentTo(self.fakeRender2d)

        cm = CardMaker('card-%s-%s' % (self.__id, self.getName()))
        cm.setFrameFullscreenQuad()
        cm.setUvRange(self.buffer.getTexture())
        self.card = base.render2d.attachNewNode(cm.generate())
        self.card.setTransparency(TransparencyAttrib.MAlpha)
        self.card.setTexture(self.buffer.getTexture())

    def _update(self, task = None):
        if globalClock.getFrameCount() == self.__lastRender:
            if task:
                return task.cont
            return

        render = False
        bx = self.buffer.getTexture().getOrigFileXSize()
        by = self.buffer.getTexture().getOrigFileYSize()
        cx = base.win.getXSize()
        cy = base.win.getYSize()
        if bx != cx or by != by:
            if self.__beastDebug:
                print ':beast::render::resolutionChanged from(%s, %s) to(%s, %s)' % (bx, by, cx, cy)
            self._setupTextureBuffer()
            render = True

        for np in self.findAllMatches('**/=dirty'):
            if np.hasPythonTag('Sprite'):
                sprite = np.getPythonTag('Sprite')
                sprite.setDirty(False)
                render = True

        if render:
            if self.__beastDebug:
                print 'SpriteCollection-%s: render %s' % (self.__id, globalClock.getFrameCount())
            self.__lastRender = globalClock.getFrameCount()
            self.buffer.setOneShot(True)
            if self.__beastForceNewFrame:
                base.graphicsEngine.renderFrame() #- Render a new frame right now, improves responsiveness

        if task:
            return task.cont

    @staticmethod
    def destroyChildren(np):
        Sprite.destroyChildren(np) #- Destroy any sprites
        for child in np.getChildren():
            if child.hasPythonTag('SpriteCollection'):
                spriteCollection = child.getPythonTag('SpriteCollection')
                spriteCollection.destroy()

    def destroy(self):
        if self.buffer:
            self.card.remove()
            self.camera2d.remove()
            base.graphicsEngine.removeWindow(self.buffer)

        self.clearPythonTag('SpriteCollection')
        taskMgr.remove('updateTask-%s-%s' % (self.__id, self.getName()))
        self.ignoreAll()
        SpriteCollection.destroyChildren(self)
        self.remove()
        self.fakeRender2d.remove()

