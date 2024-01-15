# Try the normal import way
try:
    from getDrawlib import getDrawlib
# If it fails do the more complicated way
except:
    import os,sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..")))
    from ObjectiveCli.getDrawlib import getDrawlib
drawlib = getDrawlib()

def isBetweenExcl(value,minv,maxv) -> bool:
    '''Checks if a value is between a min and max value, excluding the min/max values from the valid check.
    {value} > {minv} < {maxv}'''
    if value > minv and value < maxv: return True
    else: return False

def isBetweenIncl(value,minv,maxv) -> bool:
    '''Checks if a value is between a min and max value, including the min/max values in the valid check.
    {value} >= {minv} <= {maxv}'''
    if value >= minv and value <= maxv: return True
    else: return False

def getTopMostOfSpg(spg,_unsafe=False) -> int:
    '''Get the top-most y value of a splitPixelGroup, returns y-value as int.'''
    if _unsafe != True:
        if (type(spg) != dict and not isinstance(spg, drawlib.dtypes.splitPixelGroup)) or spg == None:
            raise InvalidInputType("ObjectiveCli: Invalid input, must be splitPixelGroup-data (dict) or the drawlib splitPixelGroup datatype.")
        # Given the previous check we can assume spg to either be splitPixelGroupData or splitPixelGroupObj, so if not a dict (data format) then retrive "splitPixelGroup" property, see drawlib.dtypes.splitPixelGroup
        if type(spg) != dict:
            spg = spg.asSplitPixelGroup()
    topMostFound = None
    for pos in spg["po"]:
        if topMostFound == None:
            topMostFound = pos[1]
        else:
            if pos[1] < topMostFound:
                topMostFound = pos[1]
    return topMostFound

def getBottomMostOfSpg(spg,_unsafe=False) -> int:
    '''Get the bottom-most y value of a splitPixelGroup, returns y-value as int.'''
    if _unsafe != True:
        if (type(spg) != dict and not isinstance(spg, drawlib.dtypes.splitPixelGroup)) or spg == None:
            raise InvalidInputType("ObjectiveCli: Invalid input, must be splitPixelGroup-data (dict) or the drawlib splitPixelGroup datatype.")
        # Given the previous check we can assume spg to either be splitPixelGroupData or splitPixelGroupObj, so if not a dict (data format) then retrive "splitPixelGroup" property, see drawlib.dtypes.splitPixelGroup
        if type(spg) != dict:
            spg = spg.asSplitPixelGroup()
    bottomMostFound = None
    for pos in spg["po"]:
        if bottomMostFound == None:
            bottomMostFound = pos[1]
        else:
            if pos[1] > bottomMostFound:
                bottomMostFound = pos[1]
    return bottomMostFound

def getLeftMostOfSpg(spg,_unsafe=False) -> int:
    '''Get the left-most x value of a splitPixelGroup, returns x-value as int.'''
    if _unsafe != True:
        if (type(spg) != dict and not isinstance(spg, drawlib.dtypes.splitPixelGroup)) or spg == None:
            raise InvalidInputType("ObjectiveCli: Invalid input, must be splitPixelGroup-data (dict) or the drawlib splitPixelGroup datatype.")
        # Given the previous check we can assume spg to either be splitPixelGroupData or splitPixelGroupObj, so if not a dict (data format) then retrive "splitPixelGroup" property, see drawlib.dtypes.splitPixelGroup
        if type(spg) != dict:
            spg = spg.asSplitPixelGroup()
    leftMostFound = None
    for pos in spg["po"]:
        if leftMostFound == None:
            leftMostFound = pos[0]
        else:
            if pos[0] < leftMostFound:
                leftMostFound = pos[0]

def getRightMostOfSpg(spg,_unsafe=False) -> bool:
    '''Get the right-most x value of a splitPixelGroup, returns x-value as int.'''
    if _unsafe != True:
        if (type(spg) != dict and not isinstance(spg, drawlib.dtypes.splitPixelGroup)) or spg == None:
            raise InvalidInputType("ObjectiveCli: Invalid input, must be splitPixelGroup-data (dict) or the drawlib splitPixelGroup datatype.")
        # Given the previous check we can assume spg to either be splitPixelGroupData or splitPixelGroupObj, so if not a dict (data format) then retrive "splitPixelGroup" property, see drawlib.dtypes.splitPixelGroup
        if type(spg) != dict:
            spg = spg.asSplitPixelGroup()
    rightMostFound = None
    for pos in spg["po"]:
        if rightMostFound == None:
            rightMostFound = pos[0]
        else:
            if pos[0] > rightMostFound:
                rightMostFound = pos[0]

def isOverlapping(positions=list,coord=tuple) -> bool:
    '''Function to check if a coord is in a position list, effectively if the coord is overlapping an object made from the positions list.'''
    if coord in positions: return True
    else: return False

def isInbetweenX(positions=list,coord=tuple) -> bool:
    '''
    Checks if the coord is inbetween to X-points on the same y.\n
    1. Gets al positions matching coord.y\n
    2. Checks if coord.x is inbetween two of the matched points.
    '''
    leftMostXAtY = None
    rightMostXAtY = None
    for pos in positions:
        if pos[1] == coord[1]:
            if leftMostXAtY == None:
                leftMostXAtY = pos[0]
            else:
                if pos[0] < leftMostXAtY:
                    leftMostXAtY = pos[0]
            if rightMostXAtY == None:
                rightMostXAtY = pos[0]
            else:
                if pos[0] > rightMostXAtY:
                    rightMostXAtY = pos[0]
    if isBetweenExcl(coord[0],leftMostXAtY,rightMostXAtY): return True
    else: return False

def isInbetweenY(positions=list,coord=tuple) -> bool:
    '''
    Checks if the coord is inbetween to Y-points on the same x.\n
    1. Gets al positions matching coord.x\n
    2. Checks if coord.y is inbetween two of the matched points.
    '''
    topMostYAtX = None
    bottomMostYAtX = None
    for pos in positions:
        if pos[0] == coord[0]:
            if topMostYAtX == None:
                topMostYAtX = pos[1]
            else:
                if pos[1] < topMostYAtX:
                    topMostYAtX = pos[1]
            if bottomMostYAtX == None:
                bottomMostYAtX = pos[1]
            else:
                if pos[1] > bottomMostYAtX:
                    bottomMostYAtX = pos[1]
    if isBetweenExcl(coord[1],topMostYAtX,bottomMostYAtX): return True
    else: return False

def addXspg(spg,x=int,_unsafe=False) -> dict:
    '''Add x to every x-value in the splitPixelGroup.'''
    if _unsafe != True:
        if (type(spg) != dict and not isinstance(spg, drawlib.dtypes.splitPixelGroup)) or spg == None:
            raise InvalidInputType("ObjectiveCli: Invalid input, must be splitPixelGroup-data (dict) or the drawlib splitPixelGroup datatype.")
        # Given the previous check we can assume spg to either be splitPixelGroupData or splitPixelGroupObj, so if not a dict (data format) then retrive "splitPixelGroup" property, see drawlib.dtypes.splitPixelGroup
        if type(spg) != dict:
            spg = spg.asSplitPixelGroup()
    for i,pos in enumerate(spg["po"]):
        spg["po"][i] = [pos[0]+x,pos[1]]
    return spg

def addYspg(spg,y=int,_unsafe=False) -> dict:
    '''Add y to every y-value in the splitPixelGroup.'''
    if _unsafe != True:
        if (type(spg) != dict and not isinstance(spg, drawlib.dtypes.splitPixelGroup)) or spg == None:
            raise InvalidInputType("ObjectiveCli: Invalid input, must be splitPixelGroup-data (dict) or the drawlib splitPixelGroup datatype.")
        # Given the previous check we can assume spg to either be splitPixelGroupData or splitPixelGroupObj, so if not a dict (data format) then retrive "splitPixelGroup" property, see drawlib.dtypes.splitPixelGroup
        if type(spg) != dict:
            spg = spg.asSplitPixelGroup()
    for i,pos in enumerate(spg["po"]):
        spg["po"][i] = [pos[0],pos[1]+y]
    return spg

def applyDiffSpg(spg,diff=(int,int),_unsafe=False) -> dict:
    '''Adds x and y to each x-value and y-value in a splitPixelGroup.\n
    x-value = x-value+x\n
    y-value = y-value+y\n
    Takes (x,y)'''
    if _unsafe != True:
        if (type(spg) != dict and not isinstance(spg, drawlib.dtypes.splitPixelGroup)) or spg == None:
            raise InvalidInputType("ObjectiveCli: Invalid input, must be splitPixelGroup-data (dict) or the drawlib splitPixelGroup datatype.")
        # Given the previous check we can assume spg to either be splitPixelGroupData or splitPixelGroupObj, so if not a dict (data format) then retrive "splitPixelGroup" property, see drawlib.dtypes.splitPixelGroup
        if type(spg) != dict:
            spg = spg.asSplitPixelGroup()
    spg = addXspg(spg,diff[0],_unsafe=True)
    spg = addYspg(spg,diff[1],_unsafe=True)
    return spg

def getPosDiff(value1=int,value2=int) -> int:
    '''Gets the positive difference between two values. |v1-v2|'''
    return abs(value1-value2)

def getDiff(value1=int,value2=int) -> int:
    '''Gets the difference between two points. (v1-v2)'''
    return value1-value2

class InvalidInputType(Exception):
    '''Exception for invalid input type.'''
    def __init__(self,message="ObjectiveCli: Invalid input!"):
        self.message = message
        super().__init__(self.message)

class InvalidOrigin(Exception):
    '''Exception for invalid origin type/value.'''
    def __init__(self,message="ObjectiveCli: Invalid origin!"):
        self.message = message
        super().__init__(self.message)

class rectBoundryBox():
    '''Class for rectangleBoundryBox taking tlCorner=(x1,y1) and brCorner=(x2,y2)'''
    def __init__(self,tlCorner=tuple,brCorner=tuple):
        self.tlCorner = tlCorner
        self.brCorner = brCorner
    def _isSprite(self,data):
        '''INTERNAL: Checks if data is sprite'''
        if (type(data) == dict and data.get("tx") != None) or isinstance(data, drawlib.dtypes.sprite):
            return True
        else:
            return False
    def _isSplitPixelGroup(self,data):
        '''INTERNAL: Checks if data is a splitPixelGroup'''
        if (type(data) == dict and data.get("po") != None) or isinstance(data, drawlib.dtypes.splitPixelGroup):
            return True
        else:
            return False
    def _isXinside(self,x=int) -> bool:
        '''INTERNAL: Checks if x is within the boundry box by checking corners.'''
        if x < self.tlCorner[0] or x > self.brCorner[0]: return False
        else: return True
    def _isYinside(self,y=int) -> bool:
        '''INTERNAL: Checks if y is within the boundry box by checking corners.'''
        if y < self.tlCorner[1] or y > self.brCorner[1]: return False
        else: return True
    def isInside(self,coord=tuple) -> bool:
        '''Checks if a coord is inside the rectBoundryBox.'''
        if self._isXinside(coord[0]) and self._isYinside(coord[1]): return True
        else: return False
    def getWidth(self) -> int:
        '''Gets the width of the rectBoundryBox.'''
        return self.brCorner[0] - self.tlCorner[0]
    def getHeight(self) -> int:
        '''Gets the height of the rectBoundryBox.'''
        return self.brCorner[1] - self.tlCorner[1]
    def isAdjacentTop(self,coord=tuple) -> bool:
        '''Checks if a coord is adjacent to the top of the rectBoundryBox.'''
        if coord[1]-1 == self.tlCorner[1]:
            if isBetweenExcl(coord[0],self.tlCorner[0],self.brCorner[0]): return True
            else: return False
        else: return False
    def isAdjacentBottom(self,coord=tuple) -> bool:
        '''Checks if a coord is adjacent to the bottom of the rectBoundryBox.'''
        if coord[1]+1 == self.brCorner[1]:
            if isBetweenExcl(coord[0],self.tlCorner[0],self.brCorner[0]): return True
            else: return False
        else: return False
    def isAdjacentLeft(self,coord=tuple) -> bool:
        '''Checks if a coord is adjacent to the left of the rectBoundryBox.'''
        if coord[0]+1 == self.tlCorner[0]:
            if isBetweenExcl(coord[1],self.tlCorner[1],self.brCorner[1]): return True
            else: return False
        else: return False
    def isAdjacentRight(self,coord=tuple) -> bool:
        '''Checks if a coord is adjacent to the right of the rectBoundryBox.'''
        if coord[0]-1 == self.brCorner[0]:
            if isBetweenExcl(coord[1],self.tlCorner[1],self.brCorner[1]): return True
            else: return False
        else: return False
    def isEnclosedWithin(self,tlCorner=tuple,brCorner=tuple) -> bool:
        '''Checks if a box built from tlCorder and brCorner is fully enclosed within the rectBoundryBox.'''
        if tlCorner[0] >= self.tlCorner[0] and brCorner[0] <= self.brCorner[0] and tlCorner[1] >= self.tlCorner[1] and brCorner[1] <= self.brCorner[1]: return True
        else: return False
    def isEncasedWithin(self,tlCorner=tuple,brCorner=tuple) -> bool:
        '''Checks if the rectBoundryBox is fully enclosed within a box built from tlCorner and brCorner.'''
        if tlCorner[0] <= self.tlCorner[0] and brCorner[0] >= self.brCorner[0] and tlCorner[1] <= self.tlCorner[1] and brCorner[1] >= self.brCorner[1]: return True
        else: return False
    def updateCornersByObj(self,objectOrData):
        '''Updates the corners after the inputed object.'''
        if objectOrData == None:
            raise InvalidInputType("ObjectiveCli.rectBoundryBox: Invalid Input, can't be None!")
        # Sprite
        if self._isSprite(objectOrData):
            if type(objectOrData) != dict:
                objectOrData = objectOrData.asSprite()
            self.tlCorner = (objectOrData["xPos"],objectOrData["yPos"])
            self.brCorner = (objectOrData["xPos"]+len(objectOrData["tx"][0]),objectOrData["yPos"]+len(objectOrData["tx"]))
        # splitPixelGroup
        elif self._isSplitPixelGroup(objectOrData):
            if type(objectOrData) != dict:
                objectOrData = objectOrData.asSplitPixelGroup()
            top = getTopMostOfSpg(objectOrData,_unsafe=True)
            bottom = getBottomMostOfSpg(objectOrData,_unsafe=True)
            left = getLeftMostOfSpg(objectOrData,_unsafe=True)
            right = getRightMostOfSpg(objectOrData,_unsafe=True)
            self.tlCorner = (left,top)
            self.brCorner = (right,bottom)

class OverlapBox():
    '''Class for an overlapBox, similar to boundryBox but less strict, taking a positions list.'''
    def __init__(self,positions=list):
        self.positions = positions
    def isOverlapping(self,coord=tuple):
        '''Check is coord is overlapping with the OverlapBox.'''
        return isOverlapping(self.positions,coord)
    def isInbetweenX(self,coord=tuple):
        '''Check if coord is in between two points on X axis, effectly if within on x-axis.'''
        return isInbetweenX(self.positions,coord)
    def isInbetweenY(self,coord=tuple):
        '''Check if coord is in between two points on Y axis, effectly if within on y-axis.'''
        return isInbetweenY(self.positions,coord)
    def isWithinXY(self,coord=tuple):
        '''Check if coord is within the OverlapBox, (Checking if the point is within a "Cross").'''
        if self.isInbetweenX(coord) and self.isInbetweenY(coord): return True
        else: return False
    def isOverlappingWithingXY(self,coord=tuple):
        '''Check if coord is overlapping with the OverlapBox, (Checking if the point is overlapping with a "Cross").'''
        if self.isOverlapping(coord) and self.isWithinXY(coord): return True
        else: return False
    def isAlignedWithTop(self,coord=tuple):
        '''Checks if a coordinate is aligned with the top of the overlapBox's y.\ncoord.y -1 == topMost.y'''
        if coord[1]-1 == self.tlCorner[1]: return True
        else: return False
    def isAlignedWithBottom(self,coord=tuple):
        '''Checks if a coordinate is aligned with the bottom of the overlapBox's y.\ncoord.y +1 == bottomMost.y'''
        if coord[1]+1 == self.brCorner[1]: return True
        else: return False
    def isAlignedWithLeft(self,coord=tuple):
        '''Checks if a coordinate is aligned with the left of the overlapBox's x.\ncoord.x +1 == leftMost.x'''
        if coord[0]+1 == self.tlCorner[0]: return True
        else: return False
    def isAlignedWithRight(self,coord=tuple):
        '''Checks if a coordinate is aligned with the right of the overlapBox's x.\ncoord.x -1 == rightMost.x'''
        if coord[0]-1 == self.brCorner[0]: return True
        else: return False
    def getBoxWidth(self):
        '''Gets the max-width of the overlapBox. (rightMost-leftMost)'''
        left = getLeftMostOfSpg({"po":self.positions},_unsafe=True)
        right = getRightMostOfSpg({"po":self.positions},_unsafe=True)
        return right-left
    def getBoxHeight(self):
        '''Gets the max-height of the overlapBox. (bottomMost-topMost)'''
        top = getTopMostOfSpg({"po":self.positions},_unsafe=True)
        bottom = getBottomMostOfSpg({"po":self.positions},_unsafe=True)
        return bottom-top

def getBBtexture(xPos,yPos,texture):
    '''Gets the boundyBox for a texture, creates a rectBoundryBox object from a texture.'''
    if (type(texture) != list and not isinstance(texture, drawlib.dtypes.texture)) or texture == None:
        raise InvalidInputType("ObjectiveCli: Invalid input, must be textureData (list) or the drawlib texture datatype.")
    if xPos == None or type(xPos) != int:
        raise InvalidInputType("ObjectiveCli: Invalid input, xPos must be an integer.")
    if yPos == None or type(yPos) != int:
        raise InvalidInputType("ObjectiveCli: Invalid input, yPos must be an integer.")
    # Given the previous check we can assume texture to either be textureData or textureObj, so if not a list (data format) then retrive "texture" property, see drawlib.dtypes.texture
    if type(texture) != list:
        texture = texture.asTexture()
    tlCorner = (xPos,yPos)
    brCorner = (xPos+len(texture[0]),yPos+len(texture))
    return rectBoundryBox(tlCorner,brCorner)

def getBBspg(spg):
    '''Gets the boundyBox for a splitPixelGroup, creates a rectBoundryBox object from a splitPixelGroup.'''
    if (type(spg) != dict and not isinstance(spg, drawlib.dtypes.splitPixelGroup)) or spg == None:
        raise InvalidInputType("ObjectiveCli: Invalid input, must be splitPixelGroup-data (dict) or the drawlib splitPixelGroup datatype.")
    # Given the previous check we can assume spg to either be splitPixelGroupData or splitPixelGroupObj, so if not a dict (data format) then retrive "splitPixelGroup" property, see drawlib.dtypes.splitPixelGroup
    if type(spg) != dict:
        spg = spg.asSplitPixelGroup()
    top = getTopMostOfSpg(spg,_unsafe=True)
    bottom = getBottomMostOfSpg(spg,_unsafe=True)
    left = getLeftMostOfSpg(spg,_unsafe=True)
    right = getRightMostOfSpg(spg,_unsafe=True)
    return rectBoundryBox( (left,top) , (right,bottom) )
    
class OriginPointConnector():
    '''Class for originPoint calculations.'''
    def __init__(self,objectOrData,origin="TL"):
        self.allowedOrigins = ["TL","TR","BL","BR","MID"]
        if objectOrData == None:
            raise InvalidInputType("ObjectiveCli: Invalid input, objectOrData must not be None.")
        if self._isSprite(objectOrData):
            self.type = "sprite"
            if type(objectOrData) != dict:
                objectOrData = objectOrData.asSprite()
            self.objectOrData = objectOrData
        elif self._isSplitPixelGroup(objectOrData):
            self.type = "splitPixelGroup"
            if type(objectOrData) != dict:
                objectOrData = objectOrData.asSplitPixelGroup()
            self.objectOrData = objectOrData
        self._validateOrigin(origin)
        self.origin = {"type":origin,"pos":self._getPosOfOrigin(origin,self.type,self.objectOrData)}
    def _isSprite(self,data) -> bool:
        '''INTERNAL: Checks if data is a sprite.'''
        if (type(data) == dict and data.get("tx") != None) or isinstance(data, drawlib.dtypes.sprite):
            return True
        else:
            return False
    def _isSplitPixelGroup(self,data) -> bool:
        '''INTERNAL: Checks if data is a splitPixelGroup.'''
        if (type(data) == dict and data.get("po") != None) or isinstance(data, drawlib.dtypes.splitPixelGroup):
            return True
        else:
            return False
    def _getWidth(self,safeType=None,safeObjOrData=None) -> int:
        '''INTERNAL: Gets the width of the object. (by-box)'''
        # sprite
        if safeType == "sprite":
            tx = safeObjOrData["tx"]
            xLen = len(tx[0])
            return xLen
        # splitPixelGroup
        elif safeType == "splitPixelGroup":
            left = getLeftMostOfSpg(safeObjOrData,_unsafe=True)
            right = getRightMostOfSpg(safeObjOrData,_unsafe=True)
            return right-left
    def _getHeight(self,safeType=None,safeObjOrData=None) -> int:
        '''INTERNAL: Gets the height of the object. (by-box)'''
        # sprite
        if safeType == "sprite":
            tx = safeObjOrData["tx"]
            yLen = len(tx)
            return yLen
        # splitPixelGroup
        elif safeType == "splitPixelGroup":
            top = getTopMostOfSpg(safeObjOrData,_unsafe=True)
            bottom = getBottomMostOfSpg(safeObjOrData,_unsafe=True)
            return bottom-top
    def _getTopLeft(self,safeType=None,safeObjOrData=None) -> tuple:
        '''INTERNAL: Gets the top-left point of the object. (by-box)'''
        # sprite
        if safeType == "sprite":
            xPos = safeObjOrData["xPos"]
            yPos = safeObjOrData["yPos"]
            #tx = sprite["tx"]
            #xLen = len(tx[0])
            #yLen = len(tx)
            return (xPos,yPos)
        # splitPixelGroup
        elif safeType == "splitPixelGroup":
            top = getTopMostOfSpg(safeObjOrData,_unsafe=True)
            #bottom = getBottomMostOfSpg(safeObjOrData,_unsafe=True)
            left = getLeftMostOfSpg(safeObjOrData,_unsafe=True)
            #right = getRightMostOfSpg(safeObjOrData,_unsafe=True)
            return (left, top)
    def _getTopRight(self,safeType=None,safeObjOrData=None) -> tuple:
        '''INTERNAL: Gets the top-right point of the object. (by-box)'''
        # sprite
        if safeType == "sprite":
            xPos = safeObjOrData["xPos"]
            yPos = safeObjOrData["yPos"]
            tx = safeObjOrData["tx"]
            xLen = len(tx[0])
            #yLen = len(tx)
            return (xPos+xLen,yPos)
        # splitPixelGroup
        elif safeType == "splitPixelGroup":
            top = getTopMostOfSpg(safeObjOrData,_unsafe=True)
            #bottom = getBottomMostOfSpg(safeObjOrData,_unsafe=True)
            #left = getLeftMostOfSpg(safeObjOrData,_unsafe=True)
            right = getRightMostOfSpg(safeObjOrData,_unsafe=True)
            return (right, top)
    def _getBottomLeft(self,safeType=None,safeObjOrData=None) -> tuple:
        '''INTERNAL: Gets the bottom-left point of the object. (by-box)'''
        # sprite
        if safeType == "sprite":
            xPos = safeObjOrData["xPos"]
            yPos = safeObjOrData["yPos"]
            tx = safeObjOrData["tx"]
            #xLen = len(tx[0])
            yLen = len(tx)
            return (xPos,yPos+yLen)
        # splitPixelGroup
        elif safeType == "splitPixelGroup":
            #top = getTopMostOfSpg(safeObjOrData,_unsafe=True)
            bottom = getBottomMostOfSpg(safeObjOrData,_unsafe=True)
            left = getLeftMostOfSpg(safeObjOrData,_unsafe=True)
            #right = getRightMostOfSpg(safeObjOrData,_unsafe=True)
            return (left, bottom)
    def _getBottomRight(self,safeType=None,safeObjOrData=None):
        '''INTERNAL: Gets the bottom-right point of the object. (by-box)'''
        # sprite
        if safeType == "sprite":
            xPos = safeObjOrData["xPos"]
            yPos = safeObjOrData["yPos"]
            tx = safeObjOrData["tx"]
            xLen = len(tx[0])
            yLen = len(tx)
            return (xPos+xLen,yPos+yLen)
        # splitPixelGroup
        elif safeType == "splitPixelGroup":
            #top = getTopMostOfSpg(safeObjOrData,_unsafe=True)
            bottom = getBottomMostOfSpg(safeObjOrData,_unsafe=True)
            #left = getLeftMostOfSpg(safeObjOrData,_unsafe=True)
            right = getRightMostOfSpg(safeObjOrData,_unsafe=True)
            return (right, bottom)
    def _getMid(self,safeType=None,safeObjOrData=None):
        '''INTERNAL: Gets the mid point of the object. (by-box)'''
        _width = self._getWidth(safeType,safeObjOrData)
        _height = self._getHeight(safeType,safeObjOrData)
        if _width % 2 == 0 or _height % 2 == 0:
            raise InvalidInputType(f"ObjectiveCli: Invalid input, object must have odd width and height to use MID origin (w:{_wdith},h:{height}).")
        # sprite
        if safeType == "sprite":
            xPos = safeObjOrData["xPos"]
            yPos = safeObjOrData["yPos"]
            tx = safeObjOrData["tx"]
            xLen = len(tx[0])
            yLen = len(tx)
            return (xPos+xLen//2,yPos+yLen//2)
        # splitPixelGroup
        elif safeType == "splitPixelGroup":            
            top = getTopMostOfSpg(safeObjOrData,_unsafe=True)
            #bottom = getBottomMostOfSpg(safeObjOrData,_unsafe=True)
            left = getLeftMostOfSpg(safeObjOrData,_unsafe=True)
            #right = getRightMostOfSpg(safeObjOrData,_unsafe=True)
            return (left+(_width//2),top+(_height//2))
    def _validateOrigin(self,origin=None):
        '''INTERNAL: Checks that an origin is valid. (by-box)'''
        if origin == None or origin not in self.allowedOrigins:
            raise InvalidOrigin(f"ObjectiveCli: Invalid origin, must be one of {self.allowedOrigins} not {origin}.")
    def _getPosOfOrigin(self,origin,safeType=None,safeObjOrData=None) -> tuple:
        '''INTERNAL: Gets the position for the current origin type.'''
        if origin == "TL": return self._getTopLeft(safeType,safeObjOrData)
        elif origin == "TR": return self._getTopRight(safeType,safeObjOrData)
        elif origin == "BL": return self._getBottomLeft(safeType,safeObjOrData)
        elif origin == "BR": return self._getBottomRight(safeType,safeObjOrData)
        elif origin == "MID": return self._getMid(safeType,safeObjOrData)
    def updateData(self,objectOrData):
        '''Replaces the data with an object/data, aswell as updating the origin point accoringly.'''
        if objectOrData == None:
            raise InvalidInputType("ObjectiveCli: Invalid input, objectOrData must not be None.")
        # sprite
        if self._isSprite(objectOrData):
            if type(objectOrData) != dict:
                objectOrData = objectOrData.asSprite()
            # Save old origin
            oldOriginPos = self.origin["pos"]
            # Change Data
            self.objectOrData = objectOrData
            self.type = "sprite"
            # Get new originPos based on our current origin
            newOriginPos = self._getPosOfOrigin(self.origin["type"],self.type,self.objectOrData)
            # Update the origin position
            self.origin["pos"] = newOriginPos
            # Calculate the diff between the old and new originPos
            diffX = getDiff(oldOriginPos[0],newOriginPos[0])
            diffY = getDiff(oldOriginPos[1],newOriginPos[1])
            # Apply the diff to the data
            self.objectOrData["xPos"] += diffX
            self.objectOrData["yPos"] += diffY
        # splitPixelGroup
        elif self._isSplitPixelGroup(objectOrData):
            if type(objectOrData) != dict:
                objectOrData = objectOrData.asSplitPixelGroup()
            # Save old origin
            oldOriginPos = self.origin["pos"]
            # Change Data
            self.objectOrData = objectOrData
            self.type = "splitPixelGroup"
            # Get new originPos based on our current origin
            newOriginPos = self._getPosOfOrigin(self.origin["type"],self.type,self.objectOrData)
            # Update the origin position
            self.origin["pos"] = newOriginPos
            # Calculate the diff between the old and new originPos
            diffX = getDiff(oldOriginPos[0],newOriginPos[0])
            diffY = getDiff(oldOriginPos[1],newOriginPos[1])
            # Apply the diff to the data
            self.objectOrData = applyDiffSpg(self.objectOrData,(diffX,diffY),_unsafe=True)
    def changeOriginPoint(self,origin="TL"):
        '''Changes the origin point type and recalculates the position.'''
        self._validateOrigin(origin)
        self.origin = {"type":origin,"pos":self._getPosOfOrigin(origin,self.type,self.objectOrData)}
    def moveBy(self,x=int,y=int):
        '''Moves the object by and x and y value, aswell as recalculating the origin-point.'''
        # Save old origin
        oldOriginPos = self.origin["pos"]
        # Get new originPos based on our current origin
        newOriginPos = (oldOriginPos[0]+x,oldOriginPos[1]+y)
        # Calculate the diff between the old and new originPos
        diffX = getDiff(newOriginPos[0],oldOriginPos[0])
        diffY = getDiff(newOriginPos[1],oldOriginPos[1])
        # Update the origin position
        self.origin["pos"] = newOriginPos
        # sprite
        if self._isSprite(self.objectOrData):
            if type(self.objectOrData) != dict:
                self.objectOrData = self.objectOrData.asSprite()
            # Apply the diff to the data
            self.objectOrData["xPos"] += diffX
            self.objectOrData["yPos"] += diffY
        # splitPixelGroup
        elif self._isSplitPixelGroup(self.objectOrData):
            if type(self.objectOrData) != dict:
                self.objectOrData = self.objectOrData.asSplitPixelGroup()
            # Apply the diff to the data
            self.objectOrData = applyDiffSpg(self.objectOrData,(diffX,diffY),_unsafe=True)
    def moveTo(self,x=int,y=int):
        '''Moves the object to and x and y value, aswell as recalculating the origin-point.'''
        # Save old origin
        oldOriginPos = self.origin["pos"]
        # Get new originPos based on our current origin
        newOriginPos = (x,y)
        # Calculate the diff between the old and new originPos
        diffX = getDiff(newOriginPos[0],oldOriginPos[0])
        diffY = getDiff(newOriginPos[1],oldOriginPos[1])
        # Update the origin position
        self.origin["pos"] = newOriginPos
        # sprite
        if self._isSprite(self.objectOrData):
            if type(self.objectOrData) != dict:
                self.objectOrData = self.objectOrData.asSprite()
            # Apply the diff to the data
            self.objectOrData["xPos"] += diffX
            self.objectOrData["yPos"] += diffY
        # splitPixelGroup
        elif self._isSplitPixelGroup(self.objectOrData):
            if type(objectOrData) != dict:
                self.objectOrData = self.objectOrData.asSplitPixelGroup()
            # Apply the diff to the data
            self.objectOrData = applyDiffSpg(self.objectOrData,(diffX,diffY),_unsafe=True)





