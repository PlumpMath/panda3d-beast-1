from panda3d.core import *
loadPrcFileData('', 'support-render-texture 1') #- enable or disable render to texture support, this is Panda/GPU
loadPrcFileData('', 'threading-model Cull/Draw')
loadPrcFileData('', 'support-threading #t')
loadPrcFileData('', 'video-sync #f')

loadPrcFileData('', 'beast-render-cache #t') #- (RTT caching) Use render to texture caching, greatly improves performance
loadPrcFileData('', 'beast-force-new-frame #t') #- Force rendering of a new frame upon updates, improves responsiveness
loadPrcFileData('', 'beast-debug #f') #- This is mostly 100% useless to you.

import direct.directbase.DirectStart
from beast.beast import *

sc = SpriteCollection('myCollection')
sc.setScale(0.5)

from random import random
for i in range(100):
    s = sc.addSprite('button'+str(i))
    s.setPos((random()-random()), 0, (random()-random()))

    default_color = '#404040'
    hover_color = '#404040'
    click_color = '#404040'


    default = s.getOptions('default')
    default.setText('Hello world!\nI bet you wish you where me!')
    default.setSize(300, 300)
    default.setTextColor('#FF0000')
    default.setBackgroundColor('#00FF00')
    default.setBorderColor('#0000FF')
    default.setTextPadding(1, 1)


    hover = s.getOptions('hover')
    hover.setTextColor('#00FF00')
    hover.setBackgroundColor('#0000FF')
    hover.setBorderColor('#FF0000')

    click = s.getOptions('click')
    click.setTextColor('#0000FF')
    click.setBackgroundColor('#FF0000')
    click.setBorderColor('#00FF00')

    s.updateToState()

run()
