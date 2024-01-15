# [Imports]
from .core import base_draw,base_mdraw,NoOutput
from .coloring import autoNoneColor,DrawlibStdPalette
from .tools import check_clampTX,clampTX

# [Functions Tools]
def _join_with_delimiter(strings, delimiter):
    # Join a list of strings with the given delimiter
    return delimiter.join(strings)

def _split_with_delimiter(string, delimiter):
    # Split a string into a list using the given delimiter
    return string.split(delimiter)

def normalizeTextureSplit(texture):
    if type(texture) == str:
        return texture.split("\n")
    else:
        return texture
def normalizeTextureString(texture):
    if type(texture) == list:
        return texture.join("\n")
    else:
        return texture

def determineDataType(object):
    _type = None
    #pixelgroup

# [Convert]
def pixelGroup_to_cmpxPixelGroup(char,pixelGroup):
    cmpxPixelGroup = []
    for pixel in pixelGroup:
        cmpxPixelGroup.append({"char":char,"pos":pixel})
    return cmpxPixelGroup

def cmpxPixelGroup_to_pixelGroup(char,cmpxPixelGroup):
    if char == None or char == "": char = cmpxPixelGroup[0]["char"]
    pixels = []
    for pixel in cmpxPixelGroup:
        pos = pixel["pos"]
        pixels.append(pos)
    return char,pixels

def splitPixelGroup_to_cmpxPixelGroup(splitPixelGroup=dict):
    pixels = splitPixelGroup["po"]
    chars = splitPixelGroup["ch"]
    cmpxPixelGroup = []
    for i,char in enumerate(chars):
        cmpxPixelGroup.append( {"char":char,"pos":pixels[i]} )
    return cmpxPixelGroup

def cmpxPixelGroup_to_splitPixelGroup(cmpxPixelGroup):
    chars = []
    poss = []
    for pGroup in cmpxPixelGroup:
        chars.append(pGroup["char"])
        poss.append(pGroup["pos"])
    return {"ch":chars,"po":poss}

def pixelGroup_to_sprite(pixel_data, char="#", negChar=" "):
    # Return empty
    if not pixel_data:
        return []
    # Calculate minimum coords
    min_x = min(pixel[0] for pixel in pixel_data)
    max_x = max(pixel[0] for pixel in pixel_data)
    min_y = min(pixel[1] for pixel in pixel_data)
    max_y = max(pixel[1] for pixel in pixel_data)
    # Get some atributes
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    # fill in negChar's in rows
    rows = [[negChar for _ in range(width)] for _ in range(height)]
    # Add pixels by indexing
    for pixel in pixel_data:
        x, y = pixel
        rows[y - min_y][x - min_x] = char
    # Create sprite and return it
    sprite = {"xPos":min_x, "yPos":min_y, "tx":rows}
    return sprite

def cmpxPixelGroup_to_sprite(pixel_data, negChar=" "):
    # Sort out lowest values
    lowest_x = min(pixel['pos'][0] for pixel in pixel_data)
    lowest_y = min(pixel['pos'][1] for pixel in pixel_data)
    # Normalize the coordinates to top-left=0,0
    normalized_pixels = [{'char': pixel['char'], 'pos': [pixel['pos'][0] - lowest_x, pixel['pos'][1] - lowest_y]} for pixel in pixel_data]
    # Get some attributes
    width = max(pixel['pos'][0] for pixel in normalized_pixels) + 1
    height = max(pixel['pos'][1] for pixel in normalized_pixels) + 1
    # Made a grid from negChars
    grid = [[negChar for _ in range(width)] for _ in range(height)]
    # Fill in characters
    for pixel in normalized_pixels:
        x, y = pixel['pos']
        char = pixel['char']
        grid[y][x] = char
    # Create sprite and return it
    sprite = {"xPos":lowest_x, "yPos":lowest_y, "tx":grid}
    return sprite

def sprite_to_pixelGroup(sprite, char, exclusionChar):
    # Get sprite data
    texture = sprite["tx"]
    xPos = sprite["xPos"]
    yPos = sprite["yPos"]
    # Check each cell, if not exlChar add to pixelGroup
    pixels = []
    for y, row in enumerate(texture):
        for x, cell in enumerate(row):
            if cell != exclusionChar:
                pixels.append([x+xPos, y+yPos])
    # Return
    return char, pixels

def sprite_to_cmpxPixelGroup(sprite, exclusionChar):
    # Get sprite data
    texture = sprite["tx"]
    xPos = sprite["xPos"]
    yPos = sprite["yPos"]
    pixel_list = []
    # Check each cell, if not exlChar add char and pos to cmpxPixelGroup
    for y, row in enumerate(texture):
        for x, char in enumerate(row):
            if char != exclusionChar:
                pixel = {"char": char, "pos": [x+xPos, y+yPos]}
                pixel_list.append(pixel)
    # Return
    return pixel_list

def texture_to_sprite(texture,xPos=0,yPos=0):
    return {"xPos":xPos, "yPos":yPos, "tx":texture.split("\n")}

def listTexture_to_sprite(texture=list,xPos=0,yPos=0):
    return {"xPos":xPos, "yPos":yPos, "tx":texture}

def sprite_to_texture(sprite):
    return sprite["xPos"],sprite["yPos"],"\n".join(sprite["tx"])


# [Functions Render]
def render_pixelGroup(char,data_pixelGroup,output=object,baseColor=None,palette=None,drawNc=False,supressDraw=False,clamps=None,excludeClamped=True):
    # Draw points
    base_mdraw(char,data_pixelGroup,output,baseColor,palette,drawNc,supressDraw=supressDraw,clamps=clamps,excludeClamped=excludeClamped)

def render_cmpxPixelGroup(data_cmpxPixelGroup,output=object,baseColor=None,palette=None,drawNc=False,supressDraw=False,clamps=None,excludeClamped=True):
    # Get points and draw them
    for pixel in data_cmpxPixelGroup:
        char = pixel["char"]
        pos = pixel["pos"]
        base_draw(char,pos[0],pos[1],output,baseColor,palette,drawNc,supressDraw=supressDraw,clamps=clamps,excludeClamped=excludeClamped)

def render_splitPixelGroup(data_splitPixelGroup=dict,output=object,baseColor=None,palette=None,drawNc=False,supressDraw=False,clamps=None,excludeClamped=True):
    # Get points and draw them
    for i,pos in enumerate(data_splitPixelGroup["po"]):
        char = data_splitPixelGroup["ch"][i]
        base_draw(char,pos[0],pos[1],output,baseColor,palette,drawNc,supressDraw=supressDraw,clamps=clamps,excludeClamped=excludeClamped)

def render_texture(xPos=0,yPos=0,data_texture=str,output=object,baseColor=None,palette=None,drawNc=False,supressDraw=False,clamps=None,excludeClamped=True):
    # Convert to sprite and render
    sprite = texture_to_sprite(data_texture,xPos,yPos)
    render_sprite(sprite,output=output,baseColor=baseColor,palette=palette,drawNc=drawNc,supressDraw=supressDraw,clamps=clamps,excludeClamped=excludeClamped)
def render_listTexture(xPos=0,yPos=0,data_texture=list,output=object,baseColor=None,palette=None,drawNc=False,supressDraw=False,clamps=None,excludeClamped=True):
    # Convert to sprite and render
    sprite = listTexture_to_sprite(data_texture,xPos,yPos)
    render_sprite(sprite,output=output,baseColor=baseColor,palette=palette,drawNc=drawNc,supressDraw=supressDraw,clamps=clamps,excludeClamped=excludeClamped)

def render_sprite(spriteTexture,output=object,baseColor=None,palette=None,drawNc=False,supressDraw=False,clamps=None,excludeClamped=True):
    # Get sprite data
    texture = spriteTexture["tx"]
    xPos = spriteTexture["xPos"]
    yPos = spriteTexture["yPos"]
    # Clamp check
    if excludeClamped == True:
        if check_clampTX(xPos,yPos,texture,clamps) == False and clamps != None:
            return
    else:
        texture = clampTX(xPos,yPos,texture,clamps)
    # Use a modified sprite renderer
    #print("\033[s") # Save cursorPos
    c = 0
    OposY = int(yPos)
    for line in texture:
        yPos = OposY + c
        if type(line) == list: line = ''.join(line) # list-texture fix
        base_draw(line,xPos,yPos,output,baseColor,palette,drawNc,supressDraw=supressDraw)
        c += 1
    #print("\033[u\033[2A") # Load cursorPos

# [Classes]
# Theese classes are to allow more methods and conversions to bee avaliable between the dataTypes using the functions above.
# And have a few standard methods: asPixelGroup, asCmpxPixelGroup, asSprite, asTexture, draw
# (These take arguments if the conversion/method is missing parameters)

class pixelGroup():
    def __init__(self,char=str,pixels=list, baseColor=None,palette=None,output=None):
        self.char = char
        self.pixels = pixels
        self.baseColor = baseColor
        self.palette = palette
        self.output = output
    def asPixelGroup(self):
        return self.char,self.pixels
    def asCmpxPixelGroup(self):
        return pixelGroup_to_cmpxPixelGroup(self.char,self.pixels)
    def asSprite(self,backgroundChar=" "):
        return pixelGroup_to_sprite(self.pixels,self.char,backgroundChar)
    def asTexture(self,backgroundChar=" "):
        sprite = pixelGroup_to_sprite(self.pixels,self.char,backgroundChar)
        return sprite["xPos"],sprite["yPos"],sprite_to_texture(sprite)
    def asSplitPixelGroup(self):
        cmpxPixelGroup = pixelGroup_to_cmpxPixelGroup(self.char,self.pixels)
        return cmpxPixelGroup_to_splitPixelGroup(cmpxPixelGroup)
    def draw(self,output=None,drawNc=False,clamps=None,excludeClamped=True):
        if output == None:
            if self.output == None: raise NoOutput()
            else: output = self.output
        render_pixelGroup(self.char,self.pixels,output,self.baseColor,self.palette,drawNc,clamps=clamps,excludeClamped=excludeClamped)
    def put(self,output=None,clamps=None,excludeClamped=True):
        if output == None:
            if self.output == None: raise NoOutput()
            else: output = self.output
        render_pixelGroup(self.char,self.pixels,output,self.baseColor,self.palette,supressDraw=True,clamps=clamps,excludeClamped=excludeClamped)
    
class cmpxPixelGroup():
    def __init__(self,data_cmpxPixelGroup=list, baseColor=None,palette=None,output=None):
        self.data_cmpxPixelGroup = data_cmpxPixelGroup
        self.baseColor = baseColor
        self.palette = palette
        self.output = output
    def asPixelGroup(self,char=None):
        return cmpxPixelGroup_to_pixelGroup(char,self.data_cmpxPixelGroup)
    def asCmpxPixelGroup(self):
        return self.data_cmpxPixelGroup
    def asSprite(self,backgroundChar=" "):
        return cmpxPixelGroup_to_sprite(self.data_cmpxPixelGroup,backgroundChar)
    def asTexture(self,backgroundChar=" "):
        sprite = cmpxPixelGroup_to_sprite(self.data_cmpxPixelGroup,backgroundChar)
        return sprite["xPos"],sprite["yPos"],sprite_to_texture(sprite)
    def asSplitPixelGroup(self):
        return cmpxPixelGroup_to_splitPixelGroup(self.data_cmpxPixelGroup)
    def draw(self,output=None,drawNc=False,clamps=None,excludeClamped=True):
        if output == None:
            if self.output == None: raise NoOutput()
            else: output = self.output
        render_cmpxPixelGroup(self.data_cmpxPixelGroup,output,self.baseColor,self.palette,drawNc,clamps=clamps,excludeClamped=excludeClamped)
    def put(self,output=None,clamps=None,excludeClamped=True):
        if output == None:
            if self.output == None: raise NoOutput()
            else: output = self.output
        render_cmpxPixelGroup(self.data_cmpxPixelGroup,output,self.baseColor,self.palette,supressDraw=True,clamps=clamps,excludeClamped=excludeClamped)

class sprite():
    def __init__(self,xPos=None,yPos=None,spriteTexture=None,sprite=None, baseColor=None,palette=None,output=None):
        if sprite != None:
            self.sprite = sprite
        else:
            if xPos == None or yPos == None or spriteTexture == None:
                raise ValueError("When not defining a sprite, al three variables must be defined: xPos, yPos, spriteTexture")
            self.sprite = {"xPos":xPos,"yPos":yPos,"tx":spriteTexture}
        self.baseColor = baseColor
        self.palette = palette
        self.output = output
    def asPixelGroup(self,char,exclusionChar=" "):
        return sprite_to_pixelGroup(self.sprite,char,exclusionChar)
    def asCmpxPixelGroup(self,exclusionChar=" "):
        return sprite_to_cmpxPixelGroup(self.sprite,exclusionChar)
    def asSprite(self):
        return self.sprite
    def asTexture(self):
        return self.sprite["xPos"],self.sprite["yPos"],sprite_to_texture(self.sprite)
    def asSplitPixelGroup(self,exclusionChar=" "):
        cmpxPixelGroup = sprite_to_cmpxPixelGroup(self.sprite, exclusionChar)
        return cmpxPixelGroup_to_splitPixelGroup(cmpxPixelGroup)
    def draw(self,output=None,drawNc=False,clamps=None,excludeClamped=True):
        if output == None:
            if self.output == None: raise NoOutput()
            else: output = self.output
        render_sprite(self.sprite,output,self.baseColor,self.palette,drawNc,clamps=clamps,excludeClamped=excludeClamped)
    def put(self,output=None,clamps=None,excludeClamped=True):
        if output == None:
            if self.output == None: raise NoOutput()
            else: output = self.output
        render_sprite(self.sprite,output,self.baseColor,self.palette,supressDraw=True,clamps=clamps,excludeClamped=excludeClamped)

class texture():
    def __init__(self,data_texture=str, baseColor=None,palette=None,output=None):
        self.data_texture = data_texture
        self.baseColor = baseColor
        self.palette = palette
        self.output = output
    def asPixelGroup(self,char=str,xPos=0,yPos=0,exclusionChar=" "):
        sprite = texture_to_sprite(xPos=xPos,yPos=yPos,texture=self.data_texture)
        return sprite_to_pixelGroup(sprite,char,exclusionChar)
    def asCmpxPixelGroup(self,char=str,xPos=0,yPos=0,exclusionChar=" "):
        sprite = texture_to_sprite(xPos=xPos,yPos=yPos,texture=self.data_texture)
        return sprite_to_cmpxPixelGroup(sprite,char,exclusionChar)
    def asSprite(self,xPos=0,yPos=0):
        return texture_to_sprite(self.data_texture,xPos,yPos)
    def asTexture(self):
        return self.data_texture
    def asSplitPixelGroup(self,xPos=0,yPos=0,exclusionChar=" "):
        sprite = texture_to_sprite(xPos=xPos,yPos=yPos,texture=self.data_texture)
        cmpxPixelGroup = sprite_to_cmpxPixelGroup(sprite, exclusionChar)
        return cmpxPixelGroup_to_splitPixelGroup(cmpxPixelGroup)
    def draw(self,xPos=0,yPos=0,output=None,drawNc=False,clamps=None,excludeClamped=True):
        if output == None:
            if self.output == None: raise NoOutput()
            else: output = self.output
        render_texture(xPos,yPos,self.data_texture,output,self.baseColor,self.palette,drawNc,clamps=clamps,excludeClamped=excludeClamped)
    def put(self,xPos=0,yPos=0,output=None,clamps=None,excludeClamped=True):
        if output == None:
            if self.output == None: raise NoOutput()
            else: output = self.output
        render_texture(xPos,yPos,self.data_texture,output,self.baseColor,self.palette,supressDraw=True,clamps=clamps,excludeClamped=excludeClamped)

class splitPixelGroup():
    def __init__(self,chars=None,positions=None,splitPixelGroup=None, baseColor=None,palette=None,output=None):
        if chars != None:
            if isinstance(chars, list) != True: raise ValueError("Chars must be a list!")
        if positions != None:
            if isinstance(positions, list) != True: raise ValueError("Positions must be a list!")
        if splitPixelGroup != None:
            if isinstance(splitPixelGroup, dict) != True: raise ValueError("SplitPixelGroup must be a dict!")
        self.chars = chars
        self.positions = positions
        if splitPixelGroup != None:
            self.chars = splitPixelGroup["ch"]
            self.positions = splitPixelGroup["po"]
        self.baseColor = baseColor
        self.palette = palette
        self.output = output
    def asPixelGroup(self):
        return self.positions
    def asCmpxPixelGroup(self):
        splitPixelGroup_to_cmpxPixelGroup({"ch":self.chars,"po":self.positions})
    def asSprite(self,exclusionChar=" "):
        cmpxPixelGroup = splitPixelGroup_to_cmpxPixelGroup({"ch":self.chars,"po":self.positions})
        return cmpxPixelGroup_to_sprite(cmpxPixelGroup,exclusionChar)
    def asTexture(self,exclusionChar=" "):
        cmpxPixelGroup = splitPixelGroup_to_cmpxPixelGroup({"ch":self.chars,"po":self.positions})
        sprite = cmpxPixelGroup_to_sprite(cmpxPixelGroup,exclusionChar)
        return sprite["xPos"],sprite["yPos"],sprite_to_texture(sprite)
    def asSplitPixelGroup(self):
        return {"ch":self.chars,"po":self.positions}
    def draw(self,output=None,drawNc=False,clamps=None,excludeClamped=True):
        if output == None:
            if self.output == None: raise NoOutput()
            else: output = self.output
        render_splitPixelGroup({"ch":self.chars,"po":self.positions},output,self.baseColor,self.palette,drawNc,clamps=clamps,excludeClamped=excludeClamped)
    def put(self,output=None,clamps=None,excludeClamped=True):
        if output == None:
            if self.output == None: raise NoOutput()
            else: output = self.output
        render_splitPixelGroup({"ch":self.chars,"po":self.positions},output,self.baseColor,self.palette,supressDraw=True,clamps=clamps,excludeClamped=excludeClamped)