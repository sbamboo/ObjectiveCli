# [Imports]
import shutil

# [Tools]
# Caps an int to the terminal size for X (for coordinates)
def capIntsX(values=list):
    sc_width, _ = shutil.get_terminal_size()
    for value in values:
        if type(value) == int:
            if value > sc_width or value < 0:
                raise ValueError("X cappedInt's value must be inside terminalResolution")
# Caps an int to the terminal size for Y (for coordinates)
def capIntsY(values=list):
    _, sc_height = shutil.get_terminal_size()
    for value in values:
        if type(value) == int:
            if value > sc_height or value < 0:
                raise ValueError("Y cappedInt's value must be inside terminalResolution")

# To fix an issue since the drawlib rectangle needs the points in order of TL,TR,BR,BL and this function organies them in that order
def arrange_coordinates_to_rectangle(x1, y1, x2, y2, x3, y3, x4, y4):
    # Find the center point
    center_x = (x1 + x2 + x3 + x4) / 4
    center_y = (y1 + y2 + y3 + y4) / 4
    # Calculate the distances from the center to each point
    distances = [(x - center_x)**2 + (y - center_y)**2 for x, y in [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]]
    # Sort the points based on their distances from the center
    sorted_indices = sorted(range(4), key=lambda i: distances[i])
    # Arrange the points to form a rectangle
    p1 = (x1, y1)
    p2 = (x2, y2)
    p3 = (x3, y3)
    p4 = (x4, y4)
    sorted_points = [p1, p2, p3, p4]
    arranged_points = [sorted_points[i] for i in sorted_indices]
    _x1, _y1 = arranged_points[0][0],arranged_points[0][1]
    _x2, _y2 = arranged_points[1][0],arranged_points[1][1]
    _x3, _y3 = arranged_points[2][0],arranged_points[3][1]
    _x4, _y4 = arranged_points[3][0],arranged_points[3][1]
    return _x1,_y1,_x2,_y2,_x3,_y3,_x4,_y4

def getTopLeft(*points):
    if not points:
        return None  # Return None if no points are provided
    x,y = [],[]
    for point in points:
        x.append(point[0])
        y.append(point[1])
    min_x = min(*x)
    min_y = min(*y)
    return (min_x, min_y)

def coordinateDifference(refPoint, leftMost):
    # Calculate the difference for X and Y
    diff_x = refPoint[0] - leftMost[0]
    diff_y = refPoint[1] - leftMost[1]
    return (diff_x, diff_y)

def addDiffToCoords(coordinates, xDiff, yDiff):
    updated_coordinates = [(x + xDiff, y + yDiff) for x, y in coordinates]
    return updated_coordinates

def resolveClamps(clamps):
    allowedTypes = [list,tuple]
    if type(clamps) in allowedTypes:
        if len(clamps) == 2:
            xClamps = clamps[0]
            yClamps = clamps[1]
        elif len(clamps) == 4:
            xClamps = [clamps[0],clamps[1]]
            yClamps = [clamps[2],clamps[3]]
        else:
            raise ValueError("Clamps must be made of 2 or 4 elements!")
    else:
        raise ValueError("Clamps must be list or tuple!")
    return xClamps,yClamps

def clampToRanges(xClamps,yClamps):
    return range(xClamps[0],xClamps[1]),range(yClamps[0],yClamps[1])

# Clamp checkers:
def check_clamp(coord,clamps):
    '''Returns true if "valid"/"inside the clamps" and false if outside.'''
    # Check clamp values
    if clamps == None: return coord # fix al None
    try:
        xClamps,yClamps = resolveClamps(clamps)
    except:
        return coord # fix failed resolve
    if xClamps == None or yClamps == None: return coord # fix either None
    if type(coord) not in [list,tuple]:
        raise ValueError("Coord must be list or tuple!")
    if coord[0] < xClamps[0] or coord[0] > xClamps[1]:
        return False
    elif coord[1] < yClamps[0] or coord[1] > yClamps[1]:
        return False
    else:
        return True
def check_clampM(coords,clamps):
    '''Returns true if "valid"/"inside the clamps" and false if outside.'''
    if clamps == None: return coords
    for clamp in coords:
        if check_clamp(clamp,clamps) == False:
            return False
    return True
def check_clampS(*args,c):
    '''Returns true if "valid"/"inside the clamps" and false if outside.'''
    if c == None: return args
    if len(args) % 2 == 0:
        # Pair coords [a,b,c,d] -> [[a,b],[c,d]] and clamp the values finaly returning non-paired list
        for i in range(0,len(args),2):
            if check_clamp([args[i],args[i+1]],c=c) == False:
                return False
        return True
    else:
        return False
def check_clampTX(xPos,yPos,texture,clamps):
    '''Function to check if a texture at a pos will go outside clamps
    Returns true if "valid"/"inside the clamps" and false if outside.'''
    YLen = len(texture)
    try: xLen = len(texture[0])
    except: xLen = 0
    x1,y1,x2,y2 = xPos,yPos,xPos+xLen,yPos+YLen
    if clamps == None: return False
    xClamps,yClamps = resolveClamps(clamps)
    if xClamps == None or yClamps == None: return False
    if x1 < xClamps[0] or x1 > xClamps[1]:
        return False
    elif x2 < xClamps[0] or x2 > xClamps[1]:
        return False
    elif y1 < yClamps[0] or y1 > yClamps[1]:
        return False
    elif y2 < yClamps[0] or y2 > yClamps[1]:
        return False
    else:
        return True

# Inclusive clampers: (Clamps values)
def clamp(coord,clamps):
    '''Clamps a coordinate to a set of clamps [[<xMin>,<xMax>], [<yMin>,<yMax>]] or [<xMin>,<xMax>,<yMin>,<yMax>]'''
    # Check clamp values
    if clamps == None: return coord # fix al None
    try:
        xClamps,yClamps = resolveClamps(clamps)
    except:
        return coord # fix failed resolve
    if xClamps == None or yClamps == None: return coord # fix either None
    if type(coord) not in [list,tuple]:
        raise ValueError("Coord must be list or tuple!")
    # Clamp X
    x = coord[0]
    if x < xClamps[0]:
        x = xClamps[0]
    elif x > xClamps[1]:
        x = xClamps[1]
    # Clamp Y
    y = coord[1]
    if y < yClamps[0]:
        y = yClamps[0]
    elif y > yClamps[1]:
        y = yClamps[1]
    # Return values (Can be asumed to be a list or tuple since our earlier check)
    if type(coord) == list:
        return [x,y]
    else:
        return (x,y)
def clampM(coords,clamps):
    '''Clamps multiple coordinates to a list of clamps [[<xMin>,<xMax>], [<yMin>,<yMax>]] or [<xMin>,<xMax>,<yMin>,<yMax>], wrapper for clamp().'''
    if clamps == None: return coords
    clampedCoords = []
    for coord in coords:
        clampedCoords += clamp(coord,clamps)
    return clampedCoords
def clampS(*args,c):
    '''Wrapper for clamp() taking clamp-values as keywarg "c" and any other arg is passed as a coordinate partial so clampS(x1,y1,x2,y2,c=[<xClamps>,<yClamps>]) would return [x1,y1,x2,y2] clamped.
    Ex:
      x1,x2,y1,y2 = clampS(x1,y1,x2,y2,c=[<xClamps>,<yClamps>])'''
    if c == None: return args
    if len(args) % 2 == 0:
        nargs = []
        # Pair coords [a,b,c,d] -> [[a,b],[c,d]] and clamp the values finaly returning non-paired list
        for i in range(0,len(args),2):
            nargs.extend( clamp([args[i],args[i+1]],c) )
        return nargs
    else:
        return args

# Exclusive clampers: (Returns only values inside clamps)
def filter_clamp(coord,clamps):
    if check_clamp(coord,clamps) == True:
        return coord
    else:
        return None
def filter_clampM(coords,clamps):
    if clamps == None: return coords
    filteredCoords = []
    for clamp in coords:
        if filter_clamp(clamp,clamps) != None:
            filteredCoords.append(clamp)
    return filteredCoords
def filter_clampS(coords,clamps):
    if c == None: return args
    filteredCoords = []
    if len(args) % 2 == 0:
        # Pair coords [a,b,c,d] -> [[a,b],[c,d]] and clamp the values finaly returning non-paired list
        for i in range(0,len(args),2):
            coord = [args[i],args[i+1]]
            if filter_clamp(coord,clamps) != None:
                filteredCoords.append(coord)
    else:
        return filteredCoords

def clampTX(xPos,yPos,texture,clamps):
    if clamps == None: return texture
    xClamps,yClamps = resolveClamps(clamps)
    if xClamps == None or yClamps == None: return False
    YLen = len(texture)
    try: xLen = len(texture[0])
    except: xLen = 0
    xMin = xPos
    xMax = xPos+xLen
    yMin = yPos
    yMax = yPos+YLen
    clampedTXl = texture[yMin:yMax]
    clampedTX = []
    for line in clampedTXl:
        clampedTX.append(line[xMin:xMax])
    return clampedTX
def clampTXtopMajor(xPos,yPos,texture,clamps):
    '''Clamps a texture taking into account its xPos and yPos, to disregard pos set xPos and yPos to 0.'''
    if clamps == None: return False
    xClamps,yClamps = resolveClamps(clamps)
    if xClamps == None or yClamps == None: return False
    # calc distance left between positon and clampEnd
    xDist = xClamps[1] - xPos
    yDist = yClamps[1] - yPos
    if xDist < 0 or yDist < 0: return []
    clampedTXl = texture[:yDist]
    clampedTX = []
    for line in clampedTXl:
        clampedTX.append(line[:xDist])
    return clampedTX
