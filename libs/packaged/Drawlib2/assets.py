from .core import base_draw
from .coloring import DrawlibStdPalette
from .tools import clampTX,check_clampTX

# ============================[DrawlibV1/DrawlibV2 assets format]============================
# De tokenising function (Variables in string surrounded by %)
def deTokenize_procent(string,variables=globals()):
	# Get tokens
	prepLine = str(string)
	tokens = re.findall(r'%.*?%',prepLine)
	# Get variable from token name and replace the token with the variables value
	for token in tokens:
		token = str(token)
		var = token.replace('%','')
		value = str(variables[var])
		string = string.replace(token,value)
	# Return de-tokenised string
	return string
def deTokenizeTexture_procent(texture,variables=globals()):
	for i,line in enumerate(texture):
		texture[i] = deTokenize(line,variables)
	return texture

# Function to load a texture file to a list of texture_lines
def load_texture(filepath,encoding="utf-8"):
	'''Load the texture from a .ta file.'''
	# Get content from file
	rawContent = open(filepath, 'r', encoding=encoding).read()
	splitContent = rawContent.split("\n")
	# Fix empty last-line issue
	if splitContent[-1] == "":
		splitContent.pop(-1)
	# Return content as a list
	return splitContent

# Asset loader loading a texture and texture-info from an asset file
def load_asset(filepath,encoding="utf-8"):
	'''Load the data from a .asset file. (Same as DrawlibV1 format but with additional sendback for extra config parameters and the comment text)'''
	# Get content from file
	rawContent = open(filepath, 'r', encoding=encoding).read()
	splitContent = rawContent.split("\n") # Line splitter
	# Get asset configuration from file
	configLine = (splitContent[0]).split("#")[0].strip()
	commentLine = ((splitContent[0]).split("#")[1]).strip()
	configLine_split = configLine.split(";")
	posX = configLine_split[0]
	posY = configLine_split[1]
	color = configLine_split[2]
	xtra = configLine_split[3:]
	splitContent.pop(0)
	# Get texture
	texture = splitContent
	# Return config and texture
	return int(posX), int(posY), list(texture), str(color), list(xtra), str(commentLine)
def toV1frmt(args,posX=None,posY=None,texture=None,color=None,extra=None,comment=None):
	'''Simple converter function that takes params and strips out extra config parameters and the comment text.'''
	if posX == None:
		posX = args[0]
	if posY == None:
		posY = args[1]
	if texture == None:
		texture = args[2]
	if color == None:
		color = args[3]
	return posX,posY,texture,color

def render_asset(posX,posY,texture,output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False,supressDraw=False,clamps=None,excludeClamped=True):
    '''Note: Not excludingClamped values will cause the render attempt to be ignored!'''
    if excludeClamped == True:
        if check_clampTX(posX,posY,texture,clamps) == False and clamps != None:
            return
    else:
        texture = clampTX(posX,posY,texture,clamps)
    # Use a modified sprite renderer
    #print("\033[s") # Save cursorPos
    c = 0
    OposY = int(posY)
    for line in texture:
        posY = OposY + c
        base_draw(line,posX,posY,output,baseColor,palette,drawNc,supressDraw=supressDraw)
        c += 1
    #print("\033[u\033[2A") # Load cursorPos

# Exception for unloaded files
class UnloadedAsset(Exception):
    def __init__(self,message="Drawlib.Assets: Attempted operation on unloaded asset, please use .load() first or use the autoLoad=True param when creating the object!"):
        self.message = message
        super().__init__(self.message)
class UnloadedTexture(Exception):
    def __init__(self,message="Drawlib.Assets: Attempted operation on unloaded texture, please use .load() first or use the autoLoad=True param when creating the object!"):
        self.message = message
        super().__init__(self.message)

# Asset class for ease of use
class asset():
	def __init__(self,filepath=str,output=object,palette=DrawlibStdPalette,autoLoad=True):
		self.filepath = filepath

		self.posX = None
		self.posY = None
		self.texture = None
		self.color = None
		self.extra = None
		self.comment = None

		self.output = output
		self.palette = palette
		if autoLoad == True: self.load()
	def load(self,encoding="utf-8"):
		self.posX,self.posY,self.texture,self.color,self.extra,self.comment = load_asset(self.filepath,encoding)
	def render(self,drawNc=False,clamps=None,excludeClamped=True):
		'''Note: Not excludingClamped values will cause the render attempt to be ignored!'''
		if self.texture == None: raise UnloadedAsset()
		render_asset(self.posX, self.posY, self.texture, self.output, self.color,self.palette,self.palette,drawNc,clamps=clamps,excludeClamped=excludeClamped)
	def render_put(self,clamps=None,excludeClamped=True):
		'''Note: Not excludingClamped values will cause the render attempt to be ignored!'''
		if self.texture == None: raise UnloadedAsset()
		render_asset(self.posX, self.posY, self.texture, self.output, self.color,self.palette,self.palette,supressDraw=True,clamps=clamps,excludeClamped=excludeClamped)
	def asTexture(self):
		if self.texture == None: raise UnloadedAsset()
		return self.texture
	def asAsset(self):
		if self.texture == None: raise UnloadedAsset()
		return self.posX, self.posY, self.texture, self.color
	def asAssetObj(self):
		if self.texture == None: raise UnloadedAsset()
		return {"posX":self.posX,"posY":self.posY,"texture":self.texture,"color":self.color,"extra":self.extra,"comment":self.comment}

# Texture class for ease of use
class texture():
	def __init__(self,filepath=str,output=object,baseColor=None,palette=DrawlibStdPalette,autoLoad=True):
		self.filepath = filepath
		
		self.texture = None

		self.output = output
		self.baseColor = baseColor
		self.palette = palette
		if autoLoad == True: self.load()
	def load(self,encoding="utf-8"):
		self.texture = load_texture(self.filepath,encoding)
	def render(self,posX=int,posY=int,drawNc=False,clamps=None,excludeClamped=True):
		'''Note: Not excludingClamped values will cause the render attempt to be ignored!'''
		if self.texture == None: raise UnloadedTexture()
		render_asset(self.posX, self.posY, self.texture, self.output, self.baseColor,self.palette,self.palette,drawNc,clamps=clamps,excludeClamped=excludeClamped)
	def render_put(self,posX=int,posY=int,clamps=None,excludeClamped=True):
		'''Note: Not excludingClamped values will cause the render attempt to be ignored!'''
		if self.texture == None: raise UnloadedTexture()
		render_asset(self.posX, self.posY, self.texture, self.output, self.baseColor,self.palette,self.palette,supressDraw=True,clamps=clamps,excludeClamped=excludeClamped)
	def asTexture(self):
		if self.texture == None: raise UnloadedTexture()
		return self.texture
	def asAsset(self,posX=int,posY=int,color=None):
		if self.texture == None: raise UnloadedTexture()
		return posX, posY, self.texture, color
	def asAssetObj(self,posX=int,posY=int,color=None,extra=None,comment=None):
		if self.texture == None: raise 
		if color == None: color = ""
		if extra == None: extra = []
		if comment == None: comment = ""
		return {"posX":posX,"posY":posY,"texture":self.texture,"color":color,"extra":extra,"comment":comment}
