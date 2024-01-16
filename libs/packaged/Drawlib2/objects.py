from .coloring import DrawlibStdPalette
from .dtypes import splitPixelGroup,sprite,texture,sprite_to_texture,sprite_to_cmpxPixelGroup,cmpxPixelGroup_to_splitPixelGroup
from .generators import baseGenerator
from .assets import load_asset,load_texture
from .pointGroupAlgorithms import *

# Base-class to inherit from. Contains pixelGenerator and objectcreator
class drawlibObj():
    def __init__(self,charset, output=object,baseColor=None,palette=DrawlibStdPalette, charFunc=baseGenerator, generateArgs=None,generateKwargs=None):
        if type(charset) == str:
            if ";;" in charset:
                self.charset = charset.split(";;")
            else:
                self.charset = list(charset)
        elif type(charset) == list:
            self.charset = charset
        else:
            raise ValueError("Charset must either be string or list!")
        self.charFunc = charFunc
        self.genData = {} # SHOULD BE FILLED IN BY SUBCLASS
        self.drawData = {
            "output": output,
            "baseColor": baseColor,
            "palette": palette
        }
        self.pixels = None
        self.splitPixelGroup = None
    def generate(self):
        pass # THIS SHOULD BE REPLACED IN SUBCLASS
    def objectify(self):
        chars = self.charFunc(self.charset,self.pixels)
        self.splitPixelGroup = splitPixelGroup(chars=chars,positions=self.pixels, baseColor=self.drawData["baseColor"],palette=self.drawData["palette"],output=self.drawData["output"])
    def make(self):
        if self.pixels == None: self.generate()
        if self.splitPixelGroup == None: self.objectify()
    def clear(self):
        self.pixels = None
        self.splitPixelGroup = None
    # Conversion Methods
    def asPixelGroup(self):
        if self.splitPixelGroup == None: self.make()
        return self.splitPixelGroup.asPixelGroup()
    def asCmpxPixelGroup(self):
        if self.splitPixelGroup == None: self.make()
        return self.splitPixelGroup.asCmpxPixelGroup()
    def asSprite(self,exclusionChar=" "):
        if self.splitPixelGroup == None: self.make()
        return self.splitPixelGroup.asSprite(exclusionChar)
    def asTexture(self,exclusionChar=" "):
        if self.splitPixelGroup == None: self.make()
        return self.splitPixelGroup.asSprite(exclusionChar)
    def asSplitPixelGroup(self):
        if self.splitPixelGroup == None: self.make()
        return {"ch":self.splitPixelGroup.chars,"po":self.pixels}
    # Draw
    def draw(self,output=None,drawNc=False,clamps=None,excludeClamped=True):
        if self.splitPixelGroup == None: self.make()
        self.splitPixelGroup.draw(output,drawNc,clamps=clamps,excludeClamped=excludeClamped)
        return self
    # Put
    def put(self,output=None,clamps=None,excludeClamped=True):
        if self.splitPixelGroup == None: self.make()
        self.splitPixelGroup.put(output,clamps=clamps,excludeClamped=excludeClamped)
        return self

# Template object for custom generator function to be added by user
# template =  templateDrawlibObj(char="#")
# def customGenerator(self,x1,y1):
#     return [[x,y],[x,y],[x,y]]
# template._customGenerator = customGenerator
# template.draw()
class templateDrawlibObj(drawlibObj):
    def __init__(self,charset, output=object,baseColor=None,palette=DrawlibStdPalette, charFunc=baseGenerator,autoGenerate=False,autoDraw=False,**kwargs):
        super().__init__(charset, output, baseColor, palette, charFunc)
        self.genData = kwargs
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def _customGenerator():
        raise Exception("templateDrawlibObj's must have a custom generate function defined (the '_customGenerator' method), that also takes the needed points and arguments to set 'self.pixels' to a pixelGroup")
    def generate(self,*args,**kwargs):
        self.pixels = self._customGenerator(*args,**kwargs)

# Drawlib objects:
class pointObj(drawlibObj):
    def __init__(self,charset,x1,y1, output=object,baseColor=None,palette=DrawlibStdPalette, charFunc=baseGenerator,autoGenerate=False,autoDraw=False):
        super().__init__(charset, output, baseColor, palette, charFunc)
        self.genData = {
            "x1": x1,
            "y1": y1
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        self.pixels = [[self.genData["x1"],self.genData["y1"]]]

class lineObj(drawlibObj):
    def __init__(self,charset,x1,y1,x2,y2, output=object,baseColor=None,palette=DrawlibStdPalette, charFunc=baseGenerator,autoGenerate=False,autoDraw=False):
        super().__init__(charset, output, baseColor, palette, charFunc)
        self.genData = {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        self.pixels = beethams_line_algorithm(**self.genData)

class triangleObj(drawlibObj):
    def __init__(self,charset,x1,y1,x2,y2,x3,y3, output=object,baseColor=None,palette=DrawlibStdPalette, charFunc=baseGenerator,autoGenerate=False,autoDraw=False):
        super().__init__(charset, output, baseColor, palette, charFunc)
        self.genData = {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "x3": x3,
            "y3": y3
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        p1 = [self.genData["x1"],self.genData["y1"]]
        p2 = [self.genData["x2"],self.genData["y2"]]
        p3 = [self.genData["x3"],self.genData["y3"]]
        self.pixels =       beethams_line_algorithm(*p1,*p2)
        self.pixels.extend( beethams_line_algorithm(*p1,*p3) )
        self.pixels.extend( beethams_line_algorithm(*p2,*p3) )

class rectangleObj(drawlibObj):
    def __init__(self,charset,x1,y1,x2,y2,x3,y3,x4,y4, output=object,baseColor=None,palette=DrawlibStdPalette, charFunc=baseGenerator,autoGenerate=False,autoDraw=False):
        super().__init__(charset, output, baseColor, palette, charFunc)
        self.genData = {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "x3": x3,
            "y3": y3,
            "x4": x4,
            "y4": y4
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        p1 = [self.genData["x1"],self.genData["y1"]]
        p2 = [self.genData["x2"],self.genData["y2"]]
        p3 = [self.genData["x3"],self.genData["y3"]]
        p4 = [self.genData["x4"],self.genData["y4"]]
        self.pixels =       beethams_line_algorithm(*p1, *p2)
        self.pixels.extend( beethams_line_algorithm(*p2,*p3) )
        self.pixels.extend( beethams_line_algorithm(*p3,*p4) )
        self.pixels.extend( beethams_line_algorithm(*p4,*p1) )

class rectangleObj2(drawlibObj):
    def __init__(self,charset,c1,c2, output=object,baseColor=None,palette=DrawlibStdPalette, charFunc=baseGenerator,autoGenerate=False,autoDraw=False):
        super().__init__(charset, output, baseColor, palette, charFunc)
        self.genData = {
            "c1": c1,
            "c2": c2
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        c1x = self.genData["c1"][0]
        c1y = self.genData["c1"][1]
        c2x = self.genData["c2"][0]
        c2y = self.genData["c2"][1]
        p1 = [c1x,c1y]
        p2 = [c2x,c1y]
        p3 = [c2x,c2y]
        p4 = [c1x,c2y]
        self.pixels =       beethams_line_algorithm(*p1, *p2)
        self.pixels.extend( beethams_line_algorithm(*p2,*p3) )
        self.pixels.extend( beethams_line_algorithm(*p3,*p4) )
        self.pixels.extend( beethams_line_algorithm(*p4,*p1) )
        #self.pixels = beethams_line_algorithm(**self.genData)

class circleObj(drawlibObj):
    def __init__(self, charset, xM, yM, r, output=object,baseColor=None,palette=DrawlibStdPalette, charFunc=baseGenerator,autoGenerate=False,autoDraw=False):
        super().__init__(charset, output, baseColor, palette, charFunc)
        self.genData = {
            "xM": xM,
            "yM": yM,
            "r": r
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        self.pixels = beethams_circle_algorithm(x_center=self.genData["xM"],y_center=self.genData["yM"],radius=self.genData["r"])

class ellipseObj(drawlibObj):
    def __init__(self, charset, cX, cY, xRad, yRad, output=object,baseColor=None,palette=DrawlibStdPalette, charFunc=baseGenerator,autoGenerate=False,autoDraw=False):
        super().__init__(charset, output, baseColor, palette, charFunc)
        self.genData = {
            "cX": cX,
            "cY": cY,
            "xRad": xRad,
            "yRad": yRad
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        self.pixels = beethams_ellipse_algorithm(self.genData["cX"],self.genData["cY"],xRadius=self.genData["xRad"],yRadius=self.genData["yRad"])

class quadBezierObj(drawlibObj):
    def __init__(self, charset, sX,sY, cX,cY, eX,eY, output=object,baseColor=None,palette=DrawlibStdPalette, charFunc=baseGenerator,autoGenerate=False,autoDraw=False):
        super().__init__(charset, output, baseColor, palette, charFunc)
        self.genData = {
            "x0": sX,
            "y0": sY,
            "x1": cX,
            "y1": cY,
            "x2": eX,
            "y2": eY
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        self.pixels = generate_quadratic_bezier(**self.genData)

class cubicBezierObj(drawlibObj):
    def __init__(self, charset, sX,sY, c1X,c1Y, c2X,c2Y, eX,eY, algorithm="step",modifier=None, output=object,baseColor=None,palette=DrawlibStdPalette, charFunc=baseGenerator,autoGenerate=False,autoDraw=False):
        '''
        Alogrithm: "step" or "point"
        Modifier: With step algorithm, def: 0.01; With point algorithm, def: 100
        '''
        super().__init__(charset, output, baseColor, palette, charFunc)
        self.genData = {
            "sX": sX,
            "sY": sY,
            "c1X": c1X,
            "c1Y": c1Y,
            "c2X": c2X,
            "c2Y": c2Y,
            "eX": eX,
            "eY": eY,
            "algorithm": algorithm,
            "modifier": modifier
        }
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        self.pixels = generate_cubic_bezier(**self.genData)

# Assets classes are not based on the same dataType as the baseClass above to they get their own classes (these are based on sprites)
# But works the same.
class assetFileObj():
    def __init__(self, filepath, output=object,baseColor=None,palette=DrawlibStdPalette, autoGenerate=False,autoDraw=False,encoding="utf-8"):
        self.filepath = filepath
        self.drawData = {
            "output": output,
            "baseColor": baseColor,
            "palette": palette
        }
        self.sprite = None
        self.spriteObj = None
        self.encoding = encoding
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
    def generate(self):
        # make texture
        posX,posY,texture,color,xtra,comment = load_asset(self.filepath,encoding=self.encoding)
        # color
        if self.color == None:
            self.drawData["baseColor"] = color
        # make sprite (NonClass)
        self.sprite = {"xPos":posX,"yPos":posY,"tx":texture}
    def objectify(self):
        self.spriteObj = sprite(sprite=self.spriteObj, baseColor=self.drawData["baseColor"],palette=self.drawData["palette"],output=self.drawData["output"])
    def make(self):
        if self.sprite == None: self.generate()
        if self.spriteObj == None: self.objectify()
    def clear(self):
        self.sprite = None
        self.spriteObj = None
    def asPixelGroup(self,char,exclusionChar=" "):
        if self.spriteObj == None: self.make()
        return self.spriteObj.asPixelGroup(char,exclusionChar)
    def asCmpxPixelGroup(self,exclusionChar=" "):
        if self.spriteObj == None: self.make()
        return self.spriteObj.asCmpxPixelGroup(exclusionChar)
    def asSprite(self):
        if self.spriteObj == None: self.make()
        return self.spriteObj.asSprite()
    def asTexture(self):
        if self.spriteObj == None: self.make()
        return sprite_to_texture(self.sprite)
    def asSplitPixelGroup(self,exclusionChar=" "):
        if self.spriteObj == None: self.make()
        cmpxPixelGroup = sprite_to_cmpxPixelGroup(self.sprite,exclusionChar)
        return cmpxPixelGroup_to_splitPixelGroup(cmpxPixelGroup)
    def draw(self,output=None,drawNc=False):
        if self.spriteObj == None: self.make()
        self.spriteObj.draw(output,drawNc)
        return self
    def put(self,output=None):
        if self.spriteObj == None: self.make()
        self.spriteObj.draw(output,supressDraw=True)
        return self
    
class assetTexture():
    def __init__(self, filepath, posov=None, output=object,baseColor=None,palette=DrawlibStdPalette, autoGenerate=False,autoDraw=False,encoding="utf-8"):
        self.filepath = filepath
        self.drawData = {
            "output": output,
            "baseColor": baseColor,
            "palette": palette
        }
        self.texture = None
        self.textureObj = None
        self.encoding = encoding
        if autoGenerate == True: self.make()
        if autoDraw == True: self.draw()
        if posov != None:
            if isinstance(posov,tuple) != True:
                raise TypeError("If defined, posov must be a tuple!")
        self.posov = posov
    def generate(self):
        self.texture = load_texture(self.filepath,encoding=self.encoding)
    def objectify(self):
        self.textureObj = texture(texture=self.texture, baseColor=self.drawData["baseColor"],palette=self.drawData["palette"],output=self.drawData["output"])
    def make(self):
        if self.texture == None: self.generate()
        if self.textureObj == None: self.objectify()
    def clear(self):
        self.texture = None
        self.textureObj = None
    def asPixelGroup(self,char,xPos=0,yPos=0,exclusionChar=" "):
        if self.textureObj == None: self.make()
        return self.textureObj.asPixelGroup(char,xPos,yPos,exclusionChar)
    def asCmpxPixelGroup(self,char,xPos=0,yPos=0,exclusionChar=" "):
        if self.textureObj == None: self.make()
        return self.textureObj.asCmpxPixelGroup(char,xPos,yPos,exclusionChar)
    def asSprite(self,xPos=0,yPos=0):
        if self.textureObj == None: self.make()
        return self.textureObj.asSprite(xPos,yPos)
    def asTexture(self):
        if self.textureObj == None: self.make()
        return sprite_to_texture(self.sprite)
    def asSplitPixelGroup(self,xPos=int,yPos=int,exclusionChar=" "):
        if self.textureObj == None: self.make()
        sprite = self.textureObj.asSprite(xPos,yPos)
        cmpxPixelGroup = sprite_to_cmpxPixelGroup(sprite,exclusionChar)
        return cmpxPixelGroup_to_splitPixelGroup(cmpxPixelGroup)
    def draw(self,xPos=0,yPos=0,output=None,drawNc=False):
        if self.posov != None:
            xPos = self.posov[0]
            yPos = self.posov[1]
        if self.textureObj == None: self.make()
        self.textureObj.draw(xPos,yPos,output,drawNc)
        return self
    def put(self,xPos=0,yPos=0,output=None):
        if self.posov != None:
            xPos = self.posov[0]
            yPos = self.posov[1]
        if self.textureObj == None: self.make()
        self.textureObj.draw(xPos,yPos,output,supressDraw=True)
        return self