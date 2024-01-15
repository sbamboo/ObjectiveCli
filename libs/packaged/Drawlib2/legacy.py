# This file contains any features/functions/classes/objects that are considered "legacy".
# In other words, deprecated and/or replaced by newer or better features. 
# The code is however still kept here for refference or if someone finds it usefull.
# Be worry that no support will be given for these so use them at your own risk.

# A lil msg for anyone importing them:
print("""\033[33m
This project is using legacy features! (Imported from legacy.py)
In other words features that are deprecated and/or replaced by newer or better alternatives. 
Be worry that no support will be given for these so use them at your own risk.
\033[0m""")

# region MANUAL VERSION INTEAD OF IMPORTS
DrawlibStdPalette = {"f_Black": "90m","b_Black": "100m","f_Red": "91m","b_Red": "101m","f_Green": "92m","b_Green": "102m","f_Yellow": "93m","b_Yellow": "103m","f_Blue": "94m","b_Blue": "104m","f_Magenta": "95m","b_Magenta": "105m","f_Cyan": "96m","b_Cyan": "106m","f_White": "97m","b_White": "107m","f_DarkBlack": "30m","b_DarkBlack": "40m","f_DarkRed": "31m","b_DarkRed": "41m","f_DarkGreen": "32m","b_DarkGreen": "42m","f_DarkYellow": "33m","b_DarkYellow": "43m","f_DarkBlue": "34m","b_DarkBlue": "44m","f_DarkMagenta": "35m","b_DarkMagenta": "45m","f_DarkCyan": "36m","b_DarkCyan": "46m","f_DarkWhite": "37m","b_DarkWhite": "47m"}
def capIntsX(values=list):
    sc_width, _ = shutil.get_terminal_size()
    for value in values:
        if type(value) == int: raise ValueError("X cappedInt's value must be inside terminalResolution") if value > sc_width or value < 0 else None
def capIntsY(values=list):
    _, sc_height = shutil.get_terminal_size()
    for value in values:
        if type(value) == int: raise ValueError("Y cappedInt's value must be inside terminalResolution") if value > sc_height or value < 0 else None
import importlib,os
spec = importlib.util.spec_from_file_location("module", os.path.join(os.path.dirname(os.path.abspath(__file__)),"pointGroupAlgorithms.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
globals().update(module.__dict__)
# endregion MANUAL VERSION INTEAD OF IMPORTS

# region =============================[Core.Buffering]=============================
class CoreSPBuffer():
    def __init__(self,width,height,iChar=" "):
        if height == "vh" or isinstance(height,MethodType): height = getConSize()[-1]
        if width == "vw" or isinstance(width,MethodType): width = getConSize()[0]
        if type(width) != int:
            width = max(width)+1
        if type(height) != int:
            height = max(height)+1
        self.bufferSize = (width,height)
        self.buffer = None
        self.bufferBaseChar = iChar
    def isCreated(self):
        if self.buffer == None:
            return False
        else:
            return True
    def isOutOfBoundsX(self,x):
        if x < 0 or x > self.bufferSize[0]: return True
        else: return False
    def isOutOfBoundsY(self,y):
        if y < 0 or y > self.bufferSize[1]: return True
        else: return False
    def anyOutOfBounds(self,xs=[],ys=[]):
        for x in xs:
            if self.isOutOfBoundsX(x):
                raise CellOpOutofBounds()
        for y in ys:
            if self.isOutOfBoundsY(y):
                raise CellOpOutofBounds()
    def create(self):
        if self.isCreated() == False:
            _buffer = []
            for y in range(self.bufferSize[-1]):
                for x in range(self.bufferSize[0]):
                    if len(_buffer)-1 < y:
                        _buffer.append(list())
                    _buffer[y].append(self.bufferBaseChar)
            self.buffer = _buffer
    def clear(self):
        if self.isCreated() == True:
            _buffer = []
            for y in range(self.bufferSize[-1]):
                for x in range(self.bufferSize[0]):
                    if len(_buffer)-1 < y:
                        _buffer.append(list())
                    _buffer[y].append(self.bufferBaseChar)
            self.buffer = _buffer
    def destroy(self):
        if self.isCreated() == True:
            self.buffer = None
    def getY(self):
        if self.isCreated() == False:
            raise UncreatedBuffer()
        return len(self.buffer)
    def getX(self):
        if self.isCreated() == False:
            raise UncreatedBuffer()
        return len(self.buffer[0])
    def getLines(self,stX=None,stY=None,enX=None,enY=None):
        # raise on non-created
        if self.isCreated() == False:
            raise UncreatedBuffer()
        # handle st,en vals
        if type(stX) != int:
            stX = 0
        if type(stY) != int:
            stY = 0
        if type(enX) != int:
            enX = self.bufferSize[0]
        if type(enY) != int:
            enY = self.bufferSize[-1]
        # handle out-of-bounds
        self.anyOutOfBounds([stX,enX],[stY,enY])
        # fix return
        toRet = []
        for y in list(range(stY+1,enY+1)):
            y = y-1
            st = ""
            for _x in self.buffer[y][stX:enX]:
                st += str(_x)
            st = st[0:self.bufferSize[0]]
            toRet.append(st)
        return toRet
    def draw(self,stX=None,stY=None,enX=None,enY=None,nc=False):
        # raise on non-created
        if self.isCreated() == False:
            raise UncreatedBuffer()
        # handle st,en vals
        if type(stX) != int:
            stX = 0
        if type(stY) != int:
            stY = 0
        if type(enX) != int:
            enX = self.bufferSize[0]
        if type(enY) != int:
            enY = self.bufferSize[-1]
        # handle out-of-bounds
        self.anyOutOfBounds([stX,enX],[stY,enY])
        # get lines
        lines = self.getLines(stX,stY,enX,enY)
        # print
        if nc != True: clear()
        for y in range(len(lines)+1):
            if lines[y-1].strip() != "":
                tx = lines[y-1]
                draw(0,y,tx)
    def put(self,x=int,y=int,st=str):
        # raise on non-created
        if self.isCreated() == False:
            raise UncreatedBuffer()
        # handle out-of-bounds
        self.anyOutOfBounds([x],[y])
        # put
        ln = len(st)
        try:
            affLi = self.buffer[y]
            for i in range(ln):
                affLi[x+i] = st
            self.buffer[y] = affLi
        except:
            pass
    def getBuf(self,retEmpty=False):
        if retEmpty == True:
            return self.buffer
        cbuf = self.buffer
        for yi,y in enumerate(cbuf):
            eX = []
            for xi,x in enumerate(cbuf[yi]):
                if cbuf[yi][xi] == self.bufferBaseChar:
                    cbuf[yi][xi] = ""
                eX.append("")
            if cbuf[yi] == eX:
                cbuf[yi] = []
        return cbuf
#endregion

# region =============================[Core.Functions]=============================
def base_draw(x,y,st=str,overwWidth=None,overwHeight=None,drawNc=False,mode="Console",buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None,baseColor=None,palette=DrawlibStdPalette):
    _obj = DrawlibOut(
        mode=mode,
        overwWidth=overwWidth,
        overwHeight=overwHeight,
        buffIChar=buffIChar,
        buffAutoStr=buffAutoStr,
        buffInst=buffInst,
        channelObj=channelObj,
        outputObj=outputObj
    )
    _obj.put(x,y,st,baseColor,palette)
    if _obj.mode != "Console":
        _obj.draw(drawNc,baseColor,palette)

def base_mdraw(coords,st=str,overwWidth=None,overwHeight=None,drawNc=False,mode="Console",buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None,baseColor=None,palette=DrawlibStdPalette):
    _obj = DrawlibOut(
        mode=mode,
        overwWidth=overwWidth,
        overwHeight=overwHeight,
        buffIChar=buffIChar,
        buffAutoStr=buffAutoStr,
        buffInst=buffInst,
        channelObj=channelObj,
        outputObj=outputObj
    )
    _obj.mPut(coords,st,baseColor,palette)
    if _obj.mode != "Console":
        _obj.draw(drawNc,baseColor,palette)

def base_fill(st=str,overwWidth=None,overwHeight=None,mode="Console",drawNc=False,buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None,baseColor=None,palette=DrawlibStdPalette):
    _obj = DrawlibOut(
        mode=mode,
        overwWidth=overwWidth,
        overwHeight=overwHeight,
        buffIChar=buffIChar,
        buffAutoStr=buffAutoStr,
        buffInst=buffInst,
        channelObj=channelObj,
        outputObj=outputObj
    )
    _obj.fill(st,baseColor,palette)
    if _obj.mode != "Console":
        _obj.draw(drawNc,baseColor,palette)

def base_texture(textureFile=str,tlCoordX=int,tlCoordY=int, overwWidth=None,overwHeight=None,mode="Console",drawNc=False,buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None,baseColor=None,palette=DrawlibStdPalette):
    # Start by initializing a drawlib-output object
    _obj = DrawlibOut(
        mode = mode,
        overwWidth=overwWidth,
        overwHeight=overwHeight,
        buffIChar=buffIChar,
        buffAutoStr=buffAutoStr,
        buffInst=buffInst,
        channelObj=channelObj,
        outputObj=outputObj
    )
    # Get the texture content from the file
    if os.path.exists(textureFile):
        rawContent = open(textureFile, 'r').read()
    else:
        raise FileNotFoundError(f"Drawlib: Texture file not found! '{textureFile}'")
    # Split the rawContent into lines of text
    spriteLines = rawContent.split('\n')
    # Render the texture at the tl-coords:
    c = 0 # Set incr-counter to 0
    orgScreenCoordY = int(tlCoordY) # Save the original y-coord
    for line in spriteLines: # iterate through the lines
        coordY = orgScreenCoordY + c # Increment the Y coordinate
        # Prep line
        line = line.replace("\\033","\033")
        line = line.replace("\033[0m","")
        line += "\033[0m"
        # Use the object to put the texture on the output
        _obj.put(tlCoordX,coordY,line,baseColor,palette)
        # Icrement y
        c += 1
    # If not mode=console then draw
    if mode != "Console":
        _obj.draw(baseColor,palette)
#endregion

# region ===========================[Linedraw.Functions]===========================
def fill_terminal(st, baseColor=None,palette=DrawlibStdPalette, wi=None,hi=None,overwWidth=None,overwHeight=None,mode=None,drawNc=False, buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    if wi != None: overwWidth = wi
    if hi != None: overwHeight = hi
    base_fill(st,overwWidth,overwHeight,mode,drawNc,buffIChar,buffAutoStr,buffInst,channelObj,outputObj,baseColor,palette)

def draw_point(st,x,y, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    base_draw(x,y,st,overwWidth,overwHeight,mode,drawNc,buffIChar,buffAutoStr,buffInst,channelObj,outputObj,baseColor,palette)

def draw_line(st,x1,y1,x2,y2, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    coords = beethams_line_algorithm(x1,y1,x2,y2)
    base_mdraw(coords,st,overwWidth,overwHeight,mode,drawNc,buffIChar,buffAutoStr,buffInst,channelObj,outputObj,baseColor,palette)

def draw_triangle_sides(st,s1,s2,s3, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    # side 1
    draw_line(st,*s1[0],*s1[1], baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)
    # side 2
    draw_line(st,*s2[0],*s2[1], baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)
    # side 3
    draw_line(st,*s3[0],*s3[1], baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)
# Same but using points
def draw_triangle_points(st,p1,p2,p3, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    draw_line(st,*p1,*p2, baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)
    draw_line(st,*p1,*p3, baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)
    draw_line(st,*p2,*p3, baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)
# Same but using coords
def draw_triangle_coords(st,x1,y1,x2,y2,x3,y3, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    p1 = [x1,y1]
    p2 = [x2,y2]
    p3 = [x3,y3]
    draw_line(st,*p1,*p2, baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)
    draw_line(st,*p1,*p3, baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)
    draw_line(st,*p2,*p3, baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)

def draw_circle(st=str,xM=int,yM=int,r=int, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    rigX = xM+r
    lefX = xM-r
    topY = yM+r
    botY = yM-r
    diam = (r*2)+1
    # CapValues
    capIntsX([xM,rigX,lefX])
    capIntsY([yM,topY,botY])
    # Calculate Coordinates
    coords = beethams_circle_algorithm(xM,yM,r)
    # Draw coordinates
    base_mdraw(coords,st,overwWidth,overwHeight,mode,drawNc,buffIChar,buffAutoStr,buffInst,channelObj,outputObj,baseColor,palette)

def draw_ellipse(char=str,cX=int,cY=int,xRad=int,yRad=int, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    rigX = cX+xRad
    lefX = cX-xRad
    topY = cY+yRad
    botY = cY-yRad
    # CapValues
    capIntsX([cX,rigX,lefX])
    capIntsY([cY,topY,botY])
    # Calculate Coordinates
    coords = beethams_ellipse_algorithm(cX,cY,xRad,yRad)
    # Draw coordinates
    base_mdraw(coords,st,overwWidth,overwHeight,mode,drawNc,buffIChar,buffAutoStr,buffInst,channelObj,outputObj,baseColor,palette)

def draw_quadBezier(char,sX=int,sY=int,cX=int,cY=int,eX=int,eY=int, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    # CapValues
    capIntsX([sX,cX,eX])
    capIntsY([sY,cY,eY])
    # Calculate Coordinates
    coords = generate_quadratic_bezier(sX,sY,cX,cY,eX,eY)
    # Draw coordinates
    base_mdraw(coords,st,overwWidth,overwHeight,mode,drawNc,buffIChar,buffAutoStr,buffInst,channelObj,outputObj,baseColor,palette)

def draw_cubicBezier(char,sX=int,sY=int,c1X=int,c1Y=int,c2X=int,c2Y=int,eX=int,eY=int, algorithm="step",modifier=None, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    '''
    Alogrithm: "step" or "point"
    Modifier: With step algorithm, def: 0.01; With point algorithm, def: 100
    '''
    # CapValues
    capIntsX([sX,c1X,c2X,eX])
    capIntsY([sY,c1Y,c2Y,eY])
    # Calculate Coordinates
    coords = generate_cubic_bezier(sX, sY, c1X, c1Y, c2X, c2Y, eX, eY, algorithm,modifier)
    # Draw coordinates
    base_mdraw(coords,st,overwWidth,overwHeight,mode,drawNc,buffIChar,buffAutoStr,buffInst,channelObj,outputObj,baseColor,palette)
# endregion

# region =================================[Dtypes]=================================
def render_textureAlt(xPos=0,yPos=0,texture=str,ansi=None):
    # Use a modified sprite renderer
    print("\033[s") # Save cursorPos
    prefline = "\033[" + str(yPos) + ";" + str(xPos) + "H"
    if ansi != None:
        prefline += "\033[" + str(ansi)
        if str(ansi).endswith("m") != True: prefline += "m"
    print(prefline, str(texture), "\033[0m")
    print("\033[u\033[2A") # Load cursorPos
#endregion
