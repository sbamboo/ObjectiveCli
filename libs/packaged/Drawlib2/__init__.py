# Exists to allow relative import
try:
    from . import assets
    from . import coloring
    from . import consoletools
    from . import core
    from . import dtypes
    from . import fonts
    from . import generators
    from . import imaging
    from . import linedraw
    from . import manip
    from . import objects
    from . import pointGroupAlgorithms
    from . import shapes
    from . import terminal
    from . import tools
    from . import version
except:
    from Drawlib2 import assets
    from Drawlib2 import coloring
    from Drawlib2 import consoletools
    from Drawlib2 import core
    from Drawlib2 import dtypes
    from Drawlib2 import fonts
    from Drawlib2 import generators
    from Drawlib2 import imaging
    from Drawlib2 import linedraw
    from Drawlib2 import manip
    from Drawlib2 import objects
    from Drawlib2 import pointGroupAlgorithms
    from Drawlib2 import shapes
    from Drawlib2 import terminal
    from Drawlib2 import tools
    from Drawlib2 import version

from .libs import conUtils as lib_conUtils
from .libs import crshpiptools as lib_crshpiptools
from .libs import stringTags as lib_stringTags

fill_terminal = linedraw.fill_terminal
reset_write_head = terminal.reset_write_head
stdpalette = coloring.DrawlibStdPalette
DrawlibOut = core.DrawlibOut

baseGenerator = generators.baseGenerator
repeatGenerator = generators.repeatGenerator
numberGenerator = generators.numberGenerator
rainbowGenerator = generators.rainbowGenerator
rainbowGeneratorZero = generators.rainbowGeneratorZero

def getLegacy():
    import os
    return lib_crshpiptools.fromPath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"legacy.py"))

class DrawlibRenderer():
    '''Main drawlib renderer class. (Works as an import-wrapper)'''
    def __init__(self):
        self.assets = assets
        self.coloring = coloring
        self.consoletools = consoletools
        self.core = core
        self.dtypes = dtypes
        self.fonts = fonts
        self.generators = generators
        self.imaging = imaging
        self.linedraw = linedraw
        self.manip = manip
        self.objects = objects
        self.pointGroupAlgorithms = pointGroupAlgorithms
        self.shapes = shapes
        self.terminal = terminal
        self.tools = tools
        self.version = version
        
        self.fill_terminal = fill_terminal
        self.stdpalette = stdpalette
        self.reset_write_head = terminal.reset_write_head
        self.DrawlibOut = core.DrawlibOut

        self.getLegacy = getLegacy