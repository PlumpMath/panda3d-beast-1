from panda3d.core import loadPrcFileData
loadPrcFileData('', 'beast-render-debug #t')
loadPrcFileData('', 'want-pstats #t')
from direct.showbase.ShowBase import ShowBase
hmm = ShowBase()

from beast import *

def onClick():
	print 'yay!'
#	alignButtons()

buttons = []
def addButtons():
	for i in range(90 * 1):
		a = beastButton('mybutton-' + str(i))
		a.reparentTo(point2d)
		a.setText('H')
		#a.setText('Hello world!')
		a.setBackgroundColor((1, 1, 1, 1))
	#	a.setMargin(4, 4, 4, 4)
		a.setColor((0, 1, 1, 1))
		a.setFontSize(1)
		a.setBackgroundImage('data/default.png')
		a.setStretchingCorners(7)

	#	a.getState('hover').setText('Hello world!!')
		a.getState('hover').setBackgroundImage('data/click.png')
	#	a.getState('click').setText('Hello world!!!')
		a.getState('click').setBackgroundImage('data/click.png')
	#	a.getState('disabled').setText('Hello world')
		a.getState('disabled').setBackgroundImage('data/disabled.png')
		a.bind(beast.leftClick, onClick)
		buttons.append(a)


def alignButtons():
	addButtons()
	a = None
	z = 350
	n = 0
	for pos, button in enumerate(buttons):
		z = -(pos / 90) * 16
		if pos == 0:
			button.setX(-600)
		button.setZ(z)
		if (pos / 90) > n:
			n = (pos / 90)
			button.setX(-600)
		elif pos > 0:
			button.align('right', a, inner = False)
		a = button

#alignButtons()

base.accept('1', alignButtons)

run()
