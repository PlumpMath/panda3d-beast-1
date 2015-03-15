## Beast aims to be a _simplistic_, _easy to use_, and _feature complete_ user interface library and toolkit for Panda3D. ##


# Why use Beast? #

## Beast comes complete, with a fully feature complete rendering system: ##

### Scaleable ###
Based upon pixels, Beast uses 'points' in place of the units of pixels, points are completely identical to pixels, except after creating your pixel-perfect UI, you, or your end-users can dynamically change the number of pixels a point represents, meaning your UI will be 100% scaleable.

### Non brute force rendering ###
Typical Panda3D GUI systems, such as DirectGui (comes with Panda3D by default) render everything each frame, now if you take into consideration how much wasted time that is, when the user interface actually never changed over a period of a several thousand frames, that's quite a bit of wasted performance.

Beast only renders a window-sized resolution frame of the UI when things actually change, which add's a heaping load of performance for user interfaces where it counts.

### Aims to be feature complete ###
Beast aims to be a fully feature complete user interface, this means that you can expect to be able to do anything from, simplistically creating a button on the screen that changes when you click it, all the way to creating full fledged user movable windows that contain several different widgets.

### Written in pure Python ###
Beast is written in pure Python, following the basic code layout of Panda3D, and trying to be as easy to use and object oriented as all of Panda3D's other libraries are, if you are comfortable using Panda3D, you'll feel right at home using Beast as a library in your games.

### Documentation ###
With Beast, we're trying to build a solid foundation of documentation for game developers so that building user interfaces is as easy as possible, so that they can focus on game development and looks, and we can focus on giving developers the documentation and tools they need to create easy user interfaces.

### License ###
Beast is licensed under the very liberal [New BSD License](License.md), which is completely compatible with Panda3D's BSD License, and works for creating both Open Source and Commercial applications with Beast.