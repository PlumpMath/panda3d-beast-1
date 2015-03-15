# Introduction #

To use the Beast's configuration variables, you should be comfortable, or at least have an understanding of [Panda3D's Configuration File](http://www.panda3d.org/manual/index.php/Configuring_Panda3D).

# Using the variables #
It's actually very simple, all you have to do is either read up on loading Configuration Variables at runtime (ie in your Python program) OR simply locate the Config.prc file inside your etc folder.

After that all you have to do is give the configuration variable name, and assign it a value.

Read further for the variable names, possible values, and the effects they have.

# Variables #
| **Variable Name** | **Default Value** | **Variable Effect** |
|:------------------|:------------------|:--------------------|
| beast-point-size | 1.0 | Changes the number of pixels that a point represents, 0.5 makes your UI half it's size, 2.0 makes your UI twice it's size |
| beast-point-size-auto | False | If enabled (True) then the point size is set to automatically scale with the size of the window, making your UI look identical, only 'larger' on bigger resolution windows |
| beast-render-brute-force | False | If enabled (True) then Beast uses no render optimizations for slow-updating UI's, and instead renders the UI each frame, as DirectGui (comes with Panda3D by default) would. |
| beast-render-debug | False | If enabled (True) then Beast will verbosely inform you when it's rendering a new frame, useful for tracking down render-related bugs |

# Practicality #
In general usage, these config variables are set to what you probably want them at, so in most cases, there is no need to set these, only set them if you actually understand the effect they will have.