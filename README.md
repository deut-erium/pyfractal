# pyfractal
A simple gui based fractal generator

## Introduction
This project is aimed to provide a simple gui for drawing fractals so that anyone enthusiastic enough can give them a try.

I was exploring [an awesome site](http://www.fractalcurves.com/) which taught me how a [turtle](https://docs.python.org/3/library/turtle.html) would draw amazing fractal curves.
Perhaps I made a small script which would draw fractals pretty neatly but it had two issues :-
* **It was slow** as it took sleeps in between each step (huh is it a turtle or a rabbit) and even after turning the animations off, it was still slow due to implementation styles
* Python Turtle's audience is beginners to programming, so it limited the extendibility of the script
* I wanted to learn more about GUI programming, python packaging, good coding practices and [other important stuff](https://stackoverflow.com/questions/11828270/how-do-i-exit-the-vim-editor)
* It had **limited scope** in scrolling, panning and zooming (the most fun things to do with a fractal)
* There is no pyfractal python library hehe

# Features
* A GUI(obviously)
* Exporting fractals to your desired format (namely svg, postscript and png)
* Loading and storing curve parameters for future endeavours
* Scrolling, panning and zooming to any extent
* Preview of base shape of fractal
* Drawing multiple fractals at once on a canvas
* Appending rules of several fractals (more people may consider it a bug, but i consider it a feature)
* Degree and radian support

# TODO 
This is probably a VERY long list but here are key TODO's :-
* **Curved Edges** 
  * Adding option to curve the corners/edges to make the fractal smoother and to see more clearly the sweep of the fractal
  * Adding splines instead of boring straight lines
* Conversion of degree to radians in input feild on pressing radio buttons (not really important but OK)
* Help Pages
  * No amount of help pages is sufficient
* Menubar
  * Adding a Menubar for easy access to resources and help pages
* More graphic options
  * Color support for lines and fills
  * Background color/image specification 
* Animations
  * Animating the turtle (why?? wasn't this the main purpose behind building this project) to momentarily enjoy the chaos caused by simple rules of life  
* More types of fractals
  * Support for [L systems](https://en.wikipedia.org/wiki/L-system)
  * Support for General [IFS](https://en.wikipedia.org/wiki/Iterated_function_system)
  * A more non-math peep friendly system?
* Grid based input
As described [here](http://www.fractalcurves.com/Taxonomy.html)
  * Square grid
  * Triangular grid
  * A general lattice maybe?
  * A general 3 dimensional lattice (okay I admit I am being too optimistic)
* Fractal type specifier
  * Automatically specify self-avoiding, self-contacting(edge/vertex), self-crossing types from the base rules
  * Dimension calculator
* Fractal tile extraction
  * Extract tiles from tile-able fractals
* More toooooools
  * Clone fractals
  * Drag and drop items around on the canvas
  
