# pyfractal
A simple gui based self-similar fractal generator

## Introduction
This project is aimed to provide a simple gui for drawing fractals so that anyone enthusiastic enough can give them a try.

## Table of contents
* [Features](#features)
* [Samples/Download](#samples)
* [Setup](#setup)
* [Usage](#usage)
* [Libraries Used](#libraries)
* [Feedback](#feedback)
* [TODO](#todo)
* [Sources](#sources)
* [Contact](#contact)

I was exploring [an awesome site](http://www.fractalcurves.com/) which taught me how a [turtle](https://docs.python.org/3/library/turtle.html) would draw amazing fractal curves.
Perhaps I made a small script which would draw fractals pretty neatly but it had two issues :-
* **It was slow** as it took sleeps in between each step (huh is it a turtle or a rabbit) and even after turning the animations off, it was still slow due to implementation styles
* Python Turtle's audience is beginners to programming, so it limited the extendibility of the script
* I wanted to learn more about GUI programming, python packaging, good coding practices and [other important stuff](https://stackoverflow.com/questions/11828270/how-do-i-exit-the-vim-editor)
* It had **limited scope** in scrolling, panning and zooming (the most fun things to do with a fractal)
* There is no pyfractal python library hehe

## <a name="features"></a>Features
* A GUI (obviously)
* Exporting fractals to your desired format (namely svg, postscript and png)
* Loading and storing curve parameters for future endeavours
* Scrolling, panning and zooming to any extent
* Preview of base shape of fractal
* Drawing multiple fractals at once on a canvas
* Appending rules of several fractals (more people may consider it a bug, but i consider it a feature)
* Degree and radian support

## <a name="samples"></a>Samples/Download
A few of the fractal images are available to download/view in [fractal_images](fractal_images) in png and svg formats
> NOTE: Pngs may get **HUGE** in size, deter from using them 
![](https://github.com/deut-erium/pyfractal/blob/master/fractal_images/svgs/5_curvePuppy.svg?raw=1)

![](https://github.com/deut-erium/pyfractal/blob/master/fractal_images/svgs/19_curve2_FractalFlower.svg?raw=1)

## <a name="setup"></a>Setup
```pip3 install pyfractal```

or 

```pip install pyfractal```

should do the job depending on the distribution

Having issues installing? Feel free to [report issue](https://github.com/deut-erium/pyfractal/issues/new) or simply clone the repository and run [main.py](https://github.com/deut-erium/pyfractal/blob/master/main.py?raw=true)

## <a name="usage"></a>Usage

```
import pyfractal  #import the module
pyfractal.GUI().run()  #to run the main gui
```
A GUI should pop up
![Main GUI](https://github.com/deut-erium/pyfractal/blob/master/images/main_gui.PNG)


### Curve parameter input
Pressing on the `plus` and `minus` buttons adds and removes entires for rule input

### Saving curve parameters
Press the `Save Parameters` button to save the parameters, a dialog box should appear asking for the name of the file to save
the parameters are stored in a json file

### Loading curve parameters
Press the `Load Parameters` button to load the parameters, a dialog box should appear asking for the name of the file. If the file is correctly formatted, you should see the parameters loaded onto the screen and list of rules added to the list. 

---
**NOTE**
The rules are appended to the list of pre-written rules (this is a design choice, not a bug) , clear the pre-existing rules by repeatedly pressing `minus` button then loading from file.

---

![Example Fractal](https://github.com/deut-erium/pyfractal/blob/master/images/example_fractal.PNG?raw=true)
### Drawing fractals
Feed in/ load the rules, you will see the preview of base fractal image on the smaller canvas.

Enter your desired `Recursion Depth` and you will see your fractal drawn on the canvas
Pan/scale/scroll in the canvas according to your viewing preferences

---
**NOTE**
The rules/preview-canvas is update only once `plus` or `minus` button is pressed.

Start drawing fractal from a smaller recursion-depth. The size of fractal is exponential in the recursion depth. It is recommended that you keep `Recursion depth` to a single digit integer.

---

## <a name="libraries"></a>Libraries Used
The project is almost built entirely on [tkinter](https://docs.python.org/3/library/tkinter.html)
Besides using [Pillow](https://pillow.readthedocs.io/en/stable/) and [canvasvg](https://pypi.org/project/canvasvg/) to save the canvas

## <a name="sources"></a>Feedback
Feel free to contribute/clone/[Issue](https://github.com/deut-erium/pyfractal/issues/new) or [Contact](#contact) me

## <a name="todo"></a>TODO 
This is probably a VERY long list but here are key TODO's :-
- [x] **Curved Edges** 
  - [x] Adding option to curve the corners/edges to make the fractal smoother and to see more clearly the sweep of the fractal
  - [ ] Adding splines instead of boring straight lines
- [ ] Conversion of degree to radians in input feild on pressing radio buttons (not really important but OK)
- [ ] Help Pages
  * No amount of help pages is sufficient
- [ ] Menubar
  * Adding a Menubar for easy access to resources and help pages
- [x] More graphic options
  - [x] Color support for lines and fills
  - [x] Background color/image specification 
- [ ] Animations
  - [ ] Animating the turtle (why?? wasn't this the main purpose behind building this project) to momentarily enjoy the chaos caused by simple rules of life  
- [ ] More types of fractals
  - [ ] Support for [L systems](https://en.wikipedia.org/wiki/L-system)
  - [ ] Support for General [IFS](https://en.wikipedia.org/wiki/Iterated_function_system)
  - [ ] A more non-math peep friendly system?
- [ ] Grid based input
As described [here](http://www.fractalcurves.com/Taxonomy.html)
  - [ ] Square grid
  - [ ] Triangular grid
  - [ ] A general lattice maybe?
  - [ ] A general 3 dimensional lattice (okay I admit I am being too optimistic)
- [ ] Fractal type specifier
  - [ ] Automatically specify self-avoiding, self-contacting(edge/vertex), self-crossing types from the base rules
  - [ ] Dimension calculator
- [ ] Fractal tile extraction
  - [ ] Extract tiles from tile-able fractals
- [ ] More toooooools
  - [ ] Clone fractals
  - [ ] Drag and drop items around on the canvas
  
## <a name="sources"></a>Sources
The following links are pretty useful and helpful in learning more about fractals
* http://www.fractalcurves.com is the main inspiration behind this project
* https://www.youtube.com/watch?v=gB9n2gHsHN4 is a pretty interesting watch by 3Blue1Brown

## <a name="contact"></a>Contact
* [My website](https://deut-erium.github.io/)
* Feel free to give suggestions/recommendations/criticism on [Discord](https://discord.com/users/deuterium#1689) or [LinkedIn](https://www.linkedin.com/in/himanshu-sheoran-ab047b152)
