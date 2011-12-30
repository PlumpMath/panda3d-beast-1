from panda3d.core import loadPrcFileData
loadPrcFileData('', 'beast-render-debug #t')
#loadPrcFileData('', 'beast-render-brute-force #t')
loadPrcFileData('', 'want-pstats #t')
from direct.showbase.ShowBase import ShowBase
hmm = ShowBase()

from beast import *

btn = beastButton('mybutton')
btn.setText('Hello world!')
btn.setFontSize(12)
btn.reparentTo(point2d)
btn.setPos(0, 0, 300)

messenger.toggleVerbose()

entry = beastEntry('myentry')
entry.setText('Hello world!')
entry.setFontSize(32)
entry.reparentTo(point2d)
entry.getState('default').setBackgroundColor((1, 1, 1, 1))
entry.getState('hover').setBackgroundColor((0, 0, 1, 1))
entry.getState('active').setBackgroundColor((0, 1, 0, 1))
entry.getState('disabled').setBackgroundColor((1, 0, 0, 1))
base.accept('1', entry.setDisabled, [True])
base.accept('2', entry.setDisabled, [False])

run()
