#!/usr/bin/python
#encoding: utf-8
'''
    This file is part of the Panda3D user interface library, Beast.
    See included "License.txt"
'''

class Color(object):
    '''
        Converts a full color eg, 255 color, (255, 255, 255) OR (255, 255, 255, 255) to a float color (1.0, 1.0, 1.0, 1.0)
        Also accepts a float color, in which case it simply returns the float color after validation.
        Good for ensuring a full 255 or float color is indeed a float color.
    '''
    @staticmethod
    def fullToFloat(floatOrFull):
        assert type(floatOrFull) == list or type(floatOrFull) == tuple
        assert len(floatOrFull) == 3 or len(floatOrFull) == 4
        # Float color must stay within 0-1, and (1, 1, 1) could be 255 full color!
        # So within range 0-1, with floats is float color
        # And within range 1 with int is full 255 color
        isFloatColor = True
        for c in floatOrFull:
            if c > 1.0:
                isFloatColor = False
                break
            elif (c == 1) and (type(c) == int or type(c) == long):
                isFloatColor = False
                break
        if isFloatColor:
            if len(floatOrFull) == 3:
                floatOrFull = (floatOrFull[0], floatOrFull[1], floatOrFull[2], 1.0)
            return floatOrFull

        r = floatOrFull[0] / 255.0
        g = floatOrFull[1] / 255.0
        b = floatOrFull[2] / 255.0
        if len(floatOrFull) == 4:
            a = floatOrFull[3] / 255.0
        else:
            a = 1.0

        return (r, g, b, a)

    '''
        Converts a hex color eg, #FFFFFF OR #FFFFFFFF, to a float color (1.0, 1.0, 1.0, 1.0)
    '''
    @staticmethod
    def hexToFloat(hexColor):
        assert type(hexColor) == str or type(hexColor) == unicode
        if hexColor.startswith('#'):
            hexColor = hexColor[1:]
        assert len(hexColor) == 6 or len(hexColor) == 8, 'Hex color must be either #RRGGBB or #RRGGBBAA format!'
        r, g, b = int(hexColor[:2], 16), int(hexColor[2:4], 16), int(hexColor[4:6], 16)
        if len(hexColor) == 8:
            a = int(hexColor[6:8], 16)
        else:
            a = 255
        return Color.fullToFloat((r, g, b, a))

    '''
        Converts a float color eg, (1.0, 1.0, 1.0) OR (1.0, 1.0, 1.0, 1.0) to a full color, (255, 255, 255, 255)
    '''
    @staticmethod
    def floatToFull(floatColor):
        assert type(floatColor) == list or type(floatColor) == tuple
        assert len(floatColor) == 3 or len(floatColor) == 4
        r = int(round(floatColor[0] * 255.0, 0))
        g = int(round(floatColor[1] * 255.0, 0))
        b = int(round(floatColor[2] * 255.0, 0))
        if len(floatColor) == 4:
            a = int(round(floatColor[3] * 255.0, 0))
        else:
            a = 255
        return (r, g, b, a)

    '''
        Converts a float color eg, (1.0, 1.0, 1.0) OR (1.0, 1.0, 1.0, 1.0) to a hex color, #FFFFFFFF
    '''
    @staticmethod
    def floatToHex(floatColor, withPound = True):
        fullColor = Color.floatToFull(floatColor)
        assert type(fullColor) == list or type(fullColor) == tuple
        assert len(fullColor) == 3 or len(fullColor) == 4
        if len(fullColor) == 3:
            hexColor = '%02x%02x%02x' % fullColor
        elif len(fullColor) == 4:
            hexColor = '%02x%02x%02x%02x' % fullColor

        if len(hexColor) == 6:
            hexColor = hexColor + 'FF'
        hexColor = hexColor.upper()

        if withPound:
            return '#' + hexColor
        else:
            return hexColor


    '''
        Color storage class, takes a single color, in any compatible format, and can convert it to other formats
        (1.0, 1.0, 1.0), or (1.0, 1.0, 1.0, 1.0)
        (255, 255, 255), or (255, 255, 255, 255)
        #RRGGBB, or #RRGGBBAA (with or without pound sign)
    '''
    def __init__(self, color = None):
        self.__color = (0.0, 0.0, 0.0, 0.0)
        if color:
            self.setColor(color)

    '''
        Change the color stored by this instance to a different one, this is the same as the constructor optional argument
    '''
    def setColor(self, color):
        if type(color) == str or type(color) == unicode:
            self.__color = self.hexToFloat(color)
        elif type(color) == tuple or type(color) == list:
            self.__color = self.fullToFloat(color)
        else:
            raise AssertionError('Invalid color format, should be either string, unicode, tuple, or list')

    '''
        Convert the stored color into a tuple of floats, ranging from 0-1, eg (0.5, 0.5, 0.5, 0.5)
    '''
    def getAsFloat(self):
        return tuple(self.__color)

    '''
        Convert the stored color into a full 255 color, ranging from 0-255, eg (128, 128, 128, 128)
    '''
    def getAsFull(self):
        return self.floatToFull(self.__color)

    '''
        Convert the stored color into a hex color, optionally starting with a pound # sign, eg #80808080
        Note: Third argument is Alpha/Transparency, which may just be FF. For "fully solid"
    '''
    def getAsHex(self, withPound = True):
        return self.floatToHex(self.__color, withPound)


if __name__ == '__main__':
    def log(col, c):
        c.setColor(col)
        print '-> %s' % (col,)
        print '-> float -> %s' % (c.getAsFloat(),)
        print '-> full  -> %s' % (c.getAsFull(),)
        print '-> hex   -> %s' % (c.getAsHex(),)
        print

    c = Color()
    log((0.5, 0.5, 0.5), c)
    log((0.5, 0.5, 0.5, 0.5), c)

    log((128, 128, 128), c)
    log((128, 128, 128, 128), c)

    log('#808080', c)
    log('#80808080', c)

