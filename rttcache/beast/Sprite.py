#!/usr/bin/python
#encoding: utf-8
'''
    This file is part of the Panda3D user interface library, Beast.
    See included "License.txt"
'''
from panda3d.core import NodePath, PGItem, TextNode, MouseButton, KeyboardButton, ConfigVariableBool
from direct.showbase.DirectObject import DirectObject
from SpriteOptions import *

'''
    Todo:
        FIXME!'s
        Add clipping support (panels larger than they appear)
        
'''


SpriteCounter = 0

import threading
base.textThreadLock = threading.Lock()

class Sprite(NodePath, DirectObject):
    #- Just constant identifiers
    MouseLeftDown = 'left-down'
    MouseLeftUp = 'left-up'
    MouseLeftClick = 'left-click'
    MouseCenterDown = 'center-down'
    MouseCenterUp = 'center-up'
    MouseCenterClick = 'center-click'
    MouseRightDown = 'right-down'
    MouseRightUp = 'right-up'
    MouseRightClick = 'right-click'
    MouseFourDown = 'four-down'
    MouseFourUp = 'four-up'
    MouseFourClick = 'four-click'
    MouseFiveDown = 'five-down'
    MouseFiveUp = 'five-up'
    MouseFiveClick = 'five-click'
    MouseScrollUp = 'scroll-up'
    MouseScrollDown = 'scroll-down'
    MouseEnter = 'enter'
    MouseExit = 'exit'
    MouseWithin = 'within'
    MouseWithout = 'without'
    StateDefault = 'state-default'
    StateHover = 'state-hover'
    StateClick = 'state-click'
    StateFocus = 'state-focus'
    StateDisabled = 'state-disabled'

    def __init__(self, name):
        NodePath.__init__(self, name)
        DirectObject.__init__(self)
        self.setPythonTag('Sprite', self)

        global SpriteCounter
        SpriteCounter += 1
        self.__id = int(SpriteCounter)

        #- Use PGItem to detect mouse and keyboard input via PGTop (eg, aspect2d, pixel2d, etc)
        self.__pgItem = PGItem(name)
        self.__pgItem.setActive(True)
        self.__pgItemNp = self.attachNewNode(self.__pgItem)

        #- Use TextNode to generate both text and cards for displaying background images
        self.__textNode = TextNode(name)
        self.__textNodeNp = None
        #self.__textNodeNp = self.attachNewNode(self.__textNode)
        #self.__textNode.setCardDecal(True) #- This is what we would do, should Sprite support being non-under PGTop

        self.accept(self.__pgItem.getPressEvent(MouseButton.one()), self.__onMouse, [Sprite.MouseLeftDown])
        self.accept(self.__pgItem.getPressEvent(MouseButton.two()), self.__onMouse, [Sprite.MouseCenterDown])
        self.accept(self.__pgItem.getPressEvent(MouseButton.three()), self.__onMouse, [Sprite.MouseRightDown])
        self.accept(self.__pgItem.getPressEvent(MouseButton.four()), self.__onMouse, [Sprite.MouseFourDown])
        self.accept(self.__pgItem.getPressEvent(MouseButton.five()), self.__onMouse, [Sprite.MouseFiveDown])

        self.accept(self.__pgItem.getReleaseEvent(MouseButton.one()), self.__onMouse, [Sprite.MouseLeftUp])
        self.accept(self.__pgItem.getReleaseEvent(MouseButton.two()), self.__onMouse, [Sprite.MouseCenterUp])
        self.accept(self.__pgItem.getReleaseEvent(MouseButton.three()), self.__onMouse, [Sprite.MouseRightUp])
        self.accept(self.__pgItem.getReleaseEvent(MouseButton.four()), self.__onMouse, [Sprite.MouseFourUp])
        self.accept(self.__pgItem.getReleaseEvent(MouseButton.five()), self.__onMouse, [Sprite.MouseFiveUp])

        self.accept(self.__pgItem.getPressEvent(MouseButton.wheelDown()), self.__onMouse, [Sprite.MouseScrollDown])
        self.accept(self.__pgItem.getPressEvent(MouseButton.wheelUp()), self.__onMouse, [Sprite.MouseScrollUp])

        self.accept(self.__pgItem.getEnterEvent(), self.__onMouse, [Sprite.MouseEnter])
        self.accept(self.__pgItem.getExitEvent(), self.__onMouse, [Sprite.MouseExit])
        self.accept(self.__pgItem.getWithinEvent(), self.__onMouse, [Sprite.MouseWithin])
        self.accept(self.__pgItem.getWithoutEvent(), self.__onMouse, [Sprite.MouseWithout])

        self.__beastDebug = ConfigVariableBool('beast-debug', False).getValue()

        self.__mouseInside = False
        self.__disabled = False

        #- Setup state configuration
        self.__lastStateOptions = None
        self.__state = None
        self.__states = {
            'default': SpriteOptions(),
            'hover': SpriteOptions(),
            'click': SpriteOptions(),
            'focus': SpriteOptions(),
            'disabled': SpriteOptions(),
        }
        self.updateToState('default')

    def setDirty(self, dirty = True):
        if dirty:
            self.setTag('dirty', '')
        else:
            self.clearTag('dirty')

    def setDisabled(self, disabled):
        self.__disabled = disabled
        if self.__disabled:
            self.updateToState('disabled')
        else:
            #- FIXME! Account for focus?
            self.updateToState('default')

    def isDisabled(self):
        return self.__disabled

    def bind(self, event, method, extraArgs = [], onlyOnce = False):
        actualEvent = self.getEvent(event)
        if onlyOnce:
            self.acceptOnce(event, method, extraArgs=extraArgs)
        else:
            self.accept(event, method, extraArgs=extraArgs)

    def unbind(self, event):
        actualEvent = self.getEvent(event)
        self.ignore(actualEvent)

    def getEvent(self, event):
        return 'Sprite-' + str(self.__id) + '-' + self.getName() + '-' + event

    def __onMouse(self, event, mwr):
        if event == Sprite.MouseEnter:
            self.__mouseInside = True
        elif event == Sprite.MouseExit:
            self.__mouseInside = False

        actualEvents = []
        actualEvents.append(event)

        if self.__mouseInside:
            if event == Sprite.MouseLeftUp:
                actualEvents.append(Sprite.MouseLeftClick)
            elif event == Sprite.MouseCenterUp:
                actualEvents.append(Sprite.MouseCenterClick)
            elif event == Sprite.MouseRightUp:
                actualEvents.append(Sprite.MouseRightClick)
            elif event == Sprite.MouseFourUp:
                actualEvents.append(Sprite.MouseFourClick)
            elif event == Sprite.MouseFiveUp:
                actualEvents.append(Sprite.MouseFiveClick)

        #- Handle state changing
        for event in actualEvents:
            if self.__state == 'default':
                if event == Sprite.MouseEnter:
                    self.updateToState('hover')
            elif self.__state == 'hover':
                if event == Sprite.MouseExit:
                    self.updateToState('default')
                if event == Sprite.MouseLeftDown:
                    self.updateToState('click')
            elif self.__state == 'click':
                if event == Sprite.MouseLeftClick:
#                    self.updateToState('focus')
                   self.updateToState('hover')
                if event == Sprite.MouseLeftUp and self.__mouseInside == False:
#                    self.updateToState('focus')
                    self.updateToState('default')

        #- Finally, we can send out user events
        for event in actualEvents:
            messenger.send(self.getEvent(event))

    def updateToState(self, newState = None):
        if newState == self.__state:
            return
        if newState:
            self.__state = newState
        if self.__beastDebug:
            print self.__state, globalClock.getFrameCount()
        messenger.send(self.getEvent('state-' + self.__state))
        defaultOptions = self.__states['default']
        hoverOptions = self.__states['hover']
        clickOptions = self.__states['click']
        focusOptions = self.__states['focus']
        disabledOptions = self.__states['disabled']

        if self.__state == 'default':
            self._applySpriteOptions(SpriteOptions.combine(defaultOptions))
        elif self.__state == 'hover':
            self._applySpriteOptions(SpriteOptions.combine(defaultOptions, hoverOptions))
        elif self.__state == 'click':
            self._applySpriteOptions(SpriteOptions.combine(defaultOptions, hoverOptions, clickOptions))
        elif self.__state == 'focus':
            self._applySpriteOptions(SpriteOptions.combine(defaultOptions, focusOptions))
        elif self.__state == 'disabled':
            self._applySpriteOptions(SpriteOptions.combine(defaultOptions, disabledOptions))

    def _applySpriteOptions(self, options):
        dirty = False
        if options.options.values() == self.__lastStateOptions:
            return
        else:
            self.__lastStateOptions = options.options.values()
            self.setDirty()
            dirty = True


        #- First we do checks for size
        if options.hasSize():
            self.__pgItem.setActive(True) #- It has a size, so it's active
            x, y = options.getSize()
            self.__pgItem.setFrame(0, x, -y, 0)
            #- Set both the card and frame bounds to match the size specified
            self.__textNode.setCardActual(0, x, -y, 0)

            if options.hasBorderColor():
                #- They want a border, no matter what
                self.__textNode.setFrameActual(0, x, -y, 0)
                if options.hasBorderWidth():
                    self.__textNode.setFrameLineWidth(options.getBorderWidth())
                else:
                    self.__textNode.setFrameLineWidth(1)
            else:
                #- They want no border
                self.__textNode.clearFrame()
                self.__textNode.setFrameLineWidth(0) #- Unimportant I think
        else:
            self.__pgItem.setActive(False) #- It has no size, it's un active
            self.__pgItem.setFrame(0, 0, 0, 0)
            self.__textNode.clearCard()
            self.__textNode.clearFrame()

        if options.hasFont():
            self.__textNode.setFont(options.getFont())
        else:
            self.__textNode.clearFont()

        if options.hasFontSize():
            #- FIXME! change for point2d later
            textNodeScale = 1.0 / options.getFontSize() #- Applied later
        #    #self.__textNodeNp.setScale(1.0 / options.getFontSize())
        # FIXME? Make sure it's 4 spaces    self.__textNode.setTabWidth(options.getFontSize() * 4.0)
        else:
            textNodeScale = 1.0
        #    #self.__textNodeNp.setScale(1.0)

        if options.hasBackgroundColor():
            color = options.getBackgroundColor().getAsFloat()
            self.__textNode.setCardColor(*color)
        else:
            if options.hasSize():
                self.__textNode.setCardColor(1, 1, 1, 1) #- White
            else:
                self.__textNode.setCardColor(0, 0, 0, 0) #- Clear

        if options.hasBorderColor():
            color = options.getBorderColor().getAsFloat()
            self.__textNode.setFrameColor(*color)
        else:
            self.__textNode.setFrameColor(0, 0, 0, 0) #- Clear

        if options.hasText():
            text = options.getText()
            self.__textNode.setWtext(options.getText())

            if options.hasTextPadding():
                px, py = options.getTextPadding()
            else:
                px, py = (0, 0)

            #- Set sizes, even if they have no color
            self.__textNode.setCardAsMargin(px, px, py, py)
            self.__textNode.setFrameAsMargin(px, px, py, py)

            l, r, b, t = self.__textNode.getCardActual()
            #- Offset the TextNode so it only extends right and down

            #- FIXME! change for point2d later? (Does scale apply there even haha?)
            s = textNodeScale
            l, r, b, t = l*s, r*s, b*s, t*s

            textNodeX = -l #- Applied later
            textNodeZ = -t #- Applied later
            #self.__textNodeNp.setX(-l)
            #self.__textNodeNp.setZ(-t)
            self.__pgItem.setActive(True) #- It has a size now, it's active
            self.__pgItem.setFrame(0, -l + r, -t + b, 0)
        else:
            self.__textNode.setWtext(u' ') #- It's important to have a space, otherwise no card is rendered!
            textNodeX = 0 #- Applied later
            textNodeZ = 0 #- Applied later
            #self.__textNodeNp.setX(0)
            #self.__textNodeNp.setZ(0)
            if not options.hasSize():
                self.__pgItem.setFrame(0, 0, 0, 0)

        if options.hasTextAlign():
            align = options.getTextAlign()
            if align == 'left':
                self.__textNode.setAlign(TextNode.ALeft)
            elif align == 'center':
                self.__textNode.setAlign(TextNode.ACenter)
            elif align == 'right':
                self.__textNode.setAlign(TextNode.ARight)
        else:
            self.__textNode.clearAlign()

        if options.hasTextColor():
            color = options.getTextColor().getAsFloat()
            self.__textNode.setTextColor(*color)
            #self.__textNodeNp.setColor(*color)
        #else:
            self.__textNode.setTextColor(0, 0, 0, 1) #- Black
        #    self.__textNodeNp.clearColor()

        if options.hasTextSmallCaps():
            self.__textNode.setSmallCaps(options.getTextSmallCaps())
        else:
            self.__textNode.clearSmallCaps()

        if options.hasTextSmallCapsScale():
            self.__textNode.setSmallCapsScale(options.getTextSmallCapsScale())
        else:
            self.__textNode.clearSmallCapsScale()

        if options.hasTextSlant():
            self.__textNode.setSlant(options.getTextSlant())
        else:
            self.__textNode.clearSlant()

        if options.hasTextUnderline():
            self.__textNode.setUnderscore(options.getTextUnderline())
        else:
            self.__textNode.clearUnderscore()

        if options.hasTextShadow():
            self.__textNode.setShadow(*options.getTextShadow())
        else:
            self.__textNode.clearShadow()

        if options.hasTextShadowColor():
            color = options.getTextShadowColor().getAsFloat()
            self.__textNode.setShadowColor(*color)
        else:
            self.__textNode.clearShadowColor()

        if self.__textNodeNp:
            self.__textNodeNp.remove()
        self.__textNodeNp = self.attachNewNode(self.__textNode.generate())
        self.__textNodeNp.setScale(textNodeScale)
        self.__textNodeNp.setX(textNodeX)
        self.__textNodeNp.setZ(textNodeZ)

        '''
        def setup(self, textNodeScale, textNodeX, textNodeZ):
            print 'getting lock...'
            base.textThreadLock.acquire()
            print 'Got lock'
            if self.__textNodeNp:
                self.__textNodeNp.remove()
            self.__textNodeNp = self.attachNewNode('foobar')
            #textNode.generate()
            print 'yes, it generated'
            base.textThreadLock.release()
        '''
            #self.__textNodeNp = self.attachNewNode(self.__textNode.generate())
            #self.__textNodeNp.setScale(textNodeScale)
            #self.__textNodeNp.setX(textNodeX)
            #self.__textNodeNp.setZ(textNodeZ)

        '''
        import direct.stdpy.threading
        t = threading.Thread(target=setup, args=(self, textNodeScale, textNodeX, textNodeZ))
        t.start()
        '''

        if dirty:
            messenger.send('beastCollectionUpdate')

    def getOptions(self, state):
        return self.__states[state]

    def getCurrentOptions(self):
        return self.__states[self.__state]

    def getCurrentState(self):
        return self.__state

    def getPgItem(self):
        return self.__pgItem

    def getPgItemNp(self):
        return self.__pgItemNp

    def getTextNode(self):
        return self.__textNode

    def getTextNodeNp(self):
        return self.__textNodeNp

    @staticmethod
    def destroyChildren(np):
        for child in np.getChildren():
            if child.hasPythonTag('Sprite'):
                sprite = child.getPythonTag('Sprite')
                sprite.destroy()

    def destroy(self):
        self.clearPythonTag('Sprite')
        self.ignoreAll()
        Sprite.destroyChildren(self)
        self.remove()

