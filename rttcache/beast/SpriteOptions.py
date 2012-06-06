#!/usr/bin/python
#encoding: utf-8
'''
    This file is part of the Panda3D user interface library, Beast.
    See included "License.txt"
'''
from Color import *

class SpriteOptions(object):
    '''
        This function combines several SpriteOptions instances, into a single SpriteOptions instance.
    '''
    @staticmethod
    def combine(*optionsList):
        if len(optionsList) == 1:
            return optionsList[0]
        assert len(optionsList) >= 2

        combined = SpriteOptions()
        for options in optionsList:
            optionsDict = options.options
            for option, value in optionsDict.items():
                if value:
                    combined.options[option] = value
        return combined

    '''
        This class contains set/get/has methods for sprite state options, a SpriteOptions instance represents
        a single sprite state (without inheritance involved), it's just a container for options, with convience methods.
    '''
    def __init__(self):
        self.options = {
            'size': None,
            'font': None,
            'fontSize': 12.0,
            'backgroundColor': None,
            'borderColor': None,
            'borderWidth': None,
            'text': None,
            'textAlign': None,
            'textColor': None,
            'textPadding': None,
            'textSmallCaps': None,
            'textSmallCapsScale': None,
            'textSlant': None,
            'textUnderline': None,
            'textShadow': None,
            'textShadowColor': None,
        }

    def __str__(self):
        return str(self.options)

    '''
        Size Methods
    '''
    def setSize(self, x, y):
        self.options['size'] = (x, y)

    def hasSize(self):
        return self.options['size'] != None

    def getSize(self):
        return self.options['size']

    '''
        Font methods
    '''
    def setFont(self, font):
        self.options['font'] = font

    def hasFont(self):
        return self.options['font'] != None

    def getFont(self):
        return self.options['font']

    '''
        Font Size methods
    '''
    def setFontSize(self, size):
        self.options['fontSize'] = size

    def hasFontSize(self):
        return self.options['fontSize'] != None

    def getFontSize(self):
        return self.options['fontSize']

    '''
        Background Color methods
    '''
    def setBackgroundColor(self, *args, **kwargs):
        self.options['backgroundColor'] = Color(*args, **kwargs)

    def hasBackgroundColor(self):
        return self.options['backgroundColor'] != None

    def getBackgroundColor(self):
        return self.options['backgroundColor']

    '''
        Border Color methods
    '''
    def setBorderColor(self, *args, **kwargs):
        self.options['borderColor'] = Color(*args, **kwargs)

    def hasBorderColor(self):
        return self.options['borderColor'] != None

    def getBorderColor(self):
        return self.options['borderColor']

    '''
        Border Width methods
    '''
    def setBorderWidth(self, width):
        self.options['borderWidth'] = width

    def hasBorderWidth(self):
        return self.options['borderWidth'] != None

    def getBorderWidth(self):
        return self.options['borderWidth']

    '''
        Text methods
    '''
    def setText(self, text):
        if type(text) != unicode:
            text = unicode(text)
        self.options['text'] = text

    def hasText(self):
        return self.options['text'] != None

    def getText(self):
        return self.options['text']

    '''
        Text Align methods
    '''
    def setTextAlign(self, align):
        self.options['textAlign'] = align

    def hasTextAlign(self):
        return self.options['textAlign'] != None

    def getTextAlign(self):
        return self.options['textAlign']

    '''
        Text Color methods
    '''
    def setTextColor(self, *args, **kwargs):
        self.options['textColor'] = Color(*args, **kwargs)

    def hasTextColor(self):
        return self.options['textColor'] != None

    def getTextColor(self): 
        return self.options['textColor']

    '''
        Text Padding methods
    '''
    def setTextPadding(self, xPadding, yPadding):
        self.options['textPadding'] = (xPadding, yPadding)

    def hasTextPadding(self):
        return self.options['textPadding'] != None

    def getTextPadding(self): 
        return self.options['textPadding']

    '''
        Text Small Caps methods
    '''
    def setTextSmallCaps(self, smallCaps):
        self.options['textSmallCaps'] = smallCaps

    def hasTextSmallCaps(self):
        return self.options['textSmallCaps'] != None

    def getTextSmallCaps(self):
        return self.options['textSmallCaps']

    '''
        Text Small Caps Scale methods
    '''
    def setTextSmallCapsScale(self, scale):
        self.options['textSmallCapsScale'] = scale

    def hasTextSmallCapsScale(self):
        return self.options['textSmallCapsScale'] != None

    def getTextSmallCapsScale(self):
        return self.options['textSmallCapsScale']

    '''
        Text Slant methods
    '''
    def setTextSlant(self, slant):
        self.options['textSlant'] = slant

    def hasTextSlant(self):
        return self.options['textSlant'] != None

    def getTextSlant(self):
        return self.options['textSlant']

    '''
        Text Underline methods
    '''
    def setTextUnderline(self, underline):
        self.options['textUnderline'] = underline

    def hasTextUnderline(self):
        return self.options['textUnderline'] != None

    def getTextUnderline(self):
        return self.options['textUnderline']

    '''
        Text Shadow methods
    '''
    def setTextShadow(self, shadow):
        self.options['textShadow'] = shadow

    def hasTextShadow(self):
        return self.options['textShadow'] != None

    def getTextShadow(self):
        return self.options['textShadow']

    '''
        Text Shadow Color methods
    '''
    def setTextShadowColor(self, *args, **kwargs):
        self.options['textShadowColor'] = Color(*args, **kwargs)

    def hasTextShadowColor(self):
        return self.options['textShadowColor'] != None

    def getTextShadowColor(self):
        return self.options['textShadowColor']

