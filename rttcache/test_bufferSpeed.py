import direct.directbase.DirectStart
from panda3d.core import *

import time

a = time.time()
for i in range(25):
    myBuffer = base.win.makeTextureBuffer('buffer'+str(i), 512, 512)
    myBuffer.setSort(-1)

    myTexture = myBuffer.getTexture()
    myCamera = base.makeCamera(myBuffer)
    myScene = NodePath('scene'+str(i))
    myCamera.reparentTo(myScene)
b = time.time()

print b - a

run()
