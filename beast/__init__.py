#! /usr/bin/python
#---------------------------------------------------------------------------#
#- Beast - An Panda3d user interface library - See included "License.txt" - #
#---------------------------------------------------------------------------#
#- Beast, __init__.py simply imports all sub modules
import __builtin__
assert hasattr(__builtin__, 'base'), 'You must import DirectStart or instance ShowBase before importing beast'
from styleDocument import *
from xmlDocument import *
from beastSpriteOptions import *

from beastGlobals import *
from beastNodePath import *
from beastSprite import *
from beastButton import *
