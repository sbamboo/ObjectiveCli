# Drawlib

## Drawlib is a simple CLI/TUI drawing library (renderer) made in python.

Author:  Simon Kalmi Claesson
* For version information see lib.json

### Files:
 - ̲ ̲ init__.py: Contains the renderer wrapper class. (As well as functioning as the package root)
 - assets.py: Asset/TextureAsset rendering and handling functions.
 - coloring.py: Mostly internal but contains functions and palettes for handling colors and advanced formatting in drawlib.
 - consoletools.py: Contains some tools regarding console, for example sizeAssist. (Not to be confused with /libs/conUtils)
 - core.py: As the name implies contains the core of drawlib, the Exceptions/Classes and main functionality.
 - dtypes.py: Datatype classes for converting and handling data in drawlib.
 - fonts.py: Additional tools for font management, requires BeutifulSoup4 and matplotlib.
 - generators.py: Contains some character-generators for use with shapeObjects from objects.py (Not to be confused with shapes from /shapes.py)
 - imaging.py: Contains classes/wrappers for the imageRenderer functionality of drawlib.
 - legacy.py: Contains legacy/broken/deprecated code, no support will be given for anything in here.
 - linedraw.py: Contains functions for linedrawing, including some functions for some predefined shapes.
 - manip.py: Tools and functions for manipulating texture-data.
 - objects.py: Contains some premade shape-classes buidling on drawlibObj, support for character-generators.
 - pointGroupAlgorithms.py: Contains raster-algorithms for drawlibs included shapes/linedrawers.
 - shapes.py: Contains classes for some premade shapes, building on the linedraw.py implementations. (No support for character-generators)
 - terminal.py: The most basic core functionality of drawlib, its building-blocks live here. Some basic ANSI rendering functions.
 - tools.py: Contains some tools for internal use in drawlib aswell as use by the users.
 - version.py: Contains some tools regarding drawlib versioning and reading lib.json.

### Difference between objects.py and shapes.py
As noted above objects.py and shapes.py are very similar, except classes from objects.py support character-generators.

The classes in objects.py are based of the datatypes, more specifically splitPixelGroup.
Thus allowing for more use cases.

The classes in shapes.py are instead building directly of the linedrawer functions and exists more to halfly "object-orient" the linedrawer functions.

*They are kept in their own file since merging with linedraw.py would make it even harder to understand the difference. (In my opinion)*

### Examples:
## Buffered Outputs
```
# Importing from the definitions in __init__.py
from Drawlib2 import DrawlibOut # alias to core.DrawlibOut

# Creating a drawlib output object with a buffer
out = DrawlibOut(mode="Buffer")

# We use the put method to place an "X" character on the position 0,0.
out.put(0,0,"X")

# Draw draws our buffer to the screen
out.draw()
```

## Console Outputs
```
# Importing from the definitions in __init__.py
from Drawlib2 import DrawlibOut # alias to core.DrawlibOut

# Creating a drawlib output object with a console-connector, thus we won't have to use the draw function just .put() when drawing.
out = DrawlibOut(mode="Console")

# We use the put method to place an "X" character on the position 0,0. (Since we are using console output, "putting" just places it on the screen)
out.put(0,0,"X")
```

### Notes:
Fonts.py has some tools to check if a user has nerd-fonts installed, see [www.nerdfonts.com](https://www.nerdfonts.com/).
The function scrapes their download page to get a list of fonts, thus it can break at any time.
The script won't download any fonts just check if the user has them installed,
but best of al would be to download the font you need yourself and tell your users to do the same.

I am in no way a part/contributor/affilate with the amazing nerdfont team, so if anyone on the team has a problem with this
just contact me and i will see what i can do.

But thank you nerdfont team for your work!