import math

from .dtypes import normalizeTextureSplit
from .tools import getTopLeft,coordinateDifference,addDiffToCoords

def fillShape(texture=list,backgroundChars=[" "],fillChar=str):
    nTex = []
    for line in texture:
        sline = list(line)
        si = None
        ei = None
        nline = ""
        chars = []
        for i,char in enumerate(sline):
            if char not in backgroundChars:
                chars.append(i)
        si = min(chars)
        ei = max(chars)
        indexes = list(range(si + 1, ei))
        for index in indexes:
            if 0 <= index < len(sline) and sline[index] in backgroundChars:
                sline[index] = fillChar
        nline = ''.join(sline)
        nTex.append(nline)
    return nTex

def stretchShapeX(texture=list, backgroundChars=[" "]):
    doubled_texture = []
    for line in texture:
        doubled_line = ""
        for i, char in enumerate(line):
            if char in backgroundChars:
                # Check left and right characters for edge preservation
                left_char = line[i - 1] if i > 0 else ' '
                right_char = line[i + 1] if i < len(line) - 1 else ' '

                # Determine the character to use for preserving edges
                if left_char in backgroundChars:
                    doubled_line += char + " "
                elif right_char in backgroundChars:
                    doubled_line += " " + char
                else:
                    doubled_line += " " * 2
            else:
                # Double the non-empty characters
                doubled_line += char * 2
        doubled_texture.append(doubled_line)
    return doubled_texture

def stretchShapeXlp(texture=list, backgroundChars=[" "]):
    stretched_texture = []
    for lIndex,line in enumerate(texture):
        stretched_line = ""
        for i, char in enumerate(line):
            if char in backgroundChars:
                left_char = line[i - 1] if i > 0 else ' '
                right_char = line[i + 1] if i < len(line) - 1 else ' '

                if left_char in backgroundChars or right_char in backgroundChars:
                    stretched_line += ' ' + char
                else:
                    stretched_line += char
            else:
                #Bottom half
                if lIndex > round(len(texture)/2):
                    if lIndex == len(texture)-1:
                        stretched_line += char * 2
                    else:
                        # left
                        if i < round(len(line)/2):
                            # Get border
                            border = None
                            for _char in line:
                                if _char not in backgroundChars and border == None:
                                    border = _char
                            if texture[lIndex+1][i] == border:
                                # get nbc
                                nbc = None
                                for _i in range(len(line)):
                                    if nbc == None:
                                        if line[_i] != border and (line[_i] in backgroundChars) == False:
                                            nbc = line[_i]
                                if nbc == None: nbc = " "
                                # append
                                stretched_line += char + nbc
                            else:
                                stretched_line += char * 2
                        # right
                        else:
                            rline = line[::-1]
                            # Get border
                            border = None
                            for _char in rline:
                                if _char not in backgroundChars and border == None:
                                    border = _char
                            if texture[lIndex+1][i] == border:
                                # get nbc
                                nbc = None
                                for _i in range(len(rline)):
                                    if nbc == None:
                                        if rline[_i] != border and (rline[_i] in backgroundChars) == False:
                                            nbc = rline[_i]
                                if nbc == None: nbc = " "
                                # append
                                stretched_line += nbc + char
                            else:
                                stretched_line += char * 2
                #Top half
                else:
                    if lIndex == 0:
                        stretched_line += char * 2
                    else:
                        # left
                        if i < round(len(line)/2):
                            # Get border
                            border = None
                            for _char in line:
                                if _char not in backgroundChars and border == None:
                                    border = _char
                            if texture[lIndex-1][i] == border:
                                # get nbc
                                nbc = None
                                for _i in range(len(line)):
                                    if nbc == None:
                                        if line[_i] != border and (line[_i] in backgroundChars) == False:
                                            nbc = line[_i]
                                if nbc == None: nbc = " "
                                # append
                                stretched_line += char + nbc
                            else:
                                stretched_line += char * 2
                        #right
                        else:
                            rline = line[::-1]
                            # Get border
                            border = None
                            for _char in rline:
                                if _char not in backgroundChars and border == None:
                                    border = _char
                            if texture[lIndex-1][i] == border:
                                # get nbc
                                nbc = None
                                for _i in range(len(rline)):
                                    if nbc == None:
                                        if rline[_i] != border and (rline[_i] in backgroundChars) == False:
                                            nbc = rline[_i]
                                if nbc == None: nbc = " "
                                # append
                                stretched_line += nbc + char
                            else:
                                stretched_line += char * 2
        stretched_texture.append(stretched_line)
    return stretched_texture

def stretchShapeY(texture, background_chars=[" "]):
    stretched_texture = []
    for i, line in enumerate(texture):
        stretched_texture.append(line)
        stretched_texture.append(line)
    return stretched_texture

def stretchShapeYlp(texture, backgroundChars=[" "]):
    stretched_texture = []
    for lIndex, line in enumerate(texture):
        #top half
        if lIndex < round(len(texture)/2):
            topLine = line
            botLine = line
            # handle botLine
            newBotLine = ""
            for i,char in enumerate(botLine):
                # Left
                if i < round(len(botLine)/2):
                    # Get border
                    border = None
                    for _char in botLine:
                        if _char not in backgroundChars and border == None:
                            border = _char
                    # Append
                    if char == border and topLine[i] == border:
                        if i != 0:
                            if botLine[i-1] == border:
                                # Get yStack
                                yStack = ""
                                for _i in range(len(texture)):
                                    yStack += texture[_i][i]
                                # Get nbc
                                nbc = None
                                for _i in range(len(yStack)):
                                    if nbc == None:
                                        if yStack[_i] != border and (yStack[_i] in backgroundChars) == False:
                                            nbc = yStack[_i]
                                if nbc == None: nbc = " "
                                # Append
                                newBotLine += nbc
                            else:
                                newBotLine += char
                        else:
                            newBotLine += char
                    else:
                        newBotLine += char
                else:
                    rBotLine = botLine[::-1]
                    # Get border
                    border = None
                    for _char in rBotLine:
                        if _char not in backgroundChars and border == None:
                            border = _char
                    # Append
                    if char == border and topLine[i] == border:
                        if i != len(botLine)-1:
                            if botLine[i+1] == border:
                                # Get yStack
                                yStack = ""
                                for _i in range(len(texture)):
                                    yStack += texture[_i][i]
                                # Get nbc
                                nbc = None
                                for _i in range(len(yStack)):
                                    if nbc == None:
                                        if yStack[_i] != border and (yStack[_i] in backgroundChars) == False:
                                            nbc = yStack[_i]
                                if nbc == None: nbc = " "
                                # Append
                                newBotLine += nbc
                            else:
                                newBotLine += char
                        else:
                            newBotLine += char
                    else:
                        newBotLine += char
            # append
            stretched_texture.append(topLine)
            stretched_texture.append(newBotLine)
        # Bottom half
        else:
            topLine = line
            botLine = line
            # handle topLine
            newTopLine = ""
            for i,char in enumerate(topLine):
                # Left
                if i < round(len(topLine)/2):
                    # Get border
                    border = None
                    for _char in topLine:
                        if _char not in backgroundChars and border == None:
                            border = _char
                    # Append
                    if char == border and botLine[i] == border:
                        if i != 0:
                            if topLine[i-1] == border:
                                # Get yStack
                                yStack = ""
                                for _i in range(len(texture)):
                                    yStack += texture[_i][i]
                                # Get nbc
                                nbc = None
                                for _i in range(len(yStack)):
                                    if nbc == None:
                                        if yStack[_i] != border and (yStack[_i] in backgroundChars) == False:
                                            nbc = yStack[_i]
                                if nbc == None: nbc = " "
                                # Append
                                newTopLine += nbc
                            else:
                                newTopLine += char
                        else:
                            newTopLine += char
                    else:
                        newTopLine += char
                else:
                    rTopLine = topLine[::-1]
                    # Get border
                    border = None
                    for _char in rTopLine:
                        if _char not in backgroundChars and border == None:
                            border = _char
                    # Append
                    if char == border and botLine[i] == border:
                        if i != len(topLine)-1:
                            if topLine[i+1] == border:
                                # Get yStack
                                yStack = ""
                                for _i in range(len(texture)):
                                    yStack += texture[_i][i]
                                yStack = yStack[::-1]
                                # Get nbc
                                nbc = None
                                for _i in range(len(yStack)):
                                    if nbc == None:
                                        if yStack[_i] != border and (yStack[_i] in backgroundChars) == False:
                                            nbc = yStack[_i]
                                if nbc == None: nbc = " "
                                # Append
                                newTopLine += nbc
                            else:
                                newTopLine += char
                        else:
                            newTopLine += char
                    else:
                        newTopLine += char
            # append
            stretched_texture.append(newTopLine)
            stretched_texture.append(botLine)
    return stretched_texture

def stretchShape(texture=list,backgroundChars=[" "],axis="x",lp=True):
    if axis.lower() == "x":
        if lp == True:
            return stretchShapeXlp(texture,backgroundChars)
        else:
            return stretchShapeX(texture,backgroundChars)
    else:
        if lp == True:
            return stretchShapeYlp(texture,backgroundChars)
        else:
            return stretchShapeY(texture,backgroundChars)

def fillSpriteObj(shapeObj,fillChar=str,bgChars=[" "]) -> None:
    xPos,yPos,tx = shapeObj.asTexture()
    tx = fillShape(normalizeTextureSplit(tx),bgChars,fillChar)
    shapeObj.sprite = {"xPos":xPos,"yPos":yPos,"tx":tx}

def stretchSpriteObj(shapeObj,bgChars=[" "],axis="X",linePreserve=False) -> None:
    xPos,yPos,tx = shapeObj.asTexture()
    if axis.lower() == "x":
        if linePreserve == True:
            tx = stretchShapeXlp(normalizeTextureSplit(tx),bgChars)
        else:
            tx = stretchShapeX(normalizeTextureSplit(tx),bgChars)
    else:
        if linePreserve == True:
            tx = stretchShapeYlp(normalizeTextureSplit(tx),bgChars)
        else:
            tx = stretchShapeY(normalizeTextureSplit(tx),bgChars)
    shapeObj.sprite = {"xPos":xPos,"yPos":yPos,"tx":tx}

def rotateSplitPixelGroup(splitPixelGroup, degrees, fixTopLeft=False):
    # Get
    characters = splitPixelGroup["ch"]
    coordinates = splitPixelGroup["po"]
    # Calculate the rotation angle in radians
    radians = math.radians(degrees)
    # Initialize empty lists for the rotated characters and coordinates
    rotated_characters = []
    rotated_coordinates = []
    # Find the center of rotation (average of all coordinates)
    cx = sum(x for x, _ in coordinates) / len(coordinates)
    cy = sum(y for _, y in coordinates) / len(coordinates)
    # Iterate through each pixel
    for char, (x, y) in zip(characters, coordinates):
        # Calculate the new coordinates after rotation
        new_x = int((x - cx) * math.cos(radians) - (y - cy) * math.sin(radians) + cx)
        new_y = int((x - cx) * math.sin(radians) + (y - cy) * math.cos(radians) + cy)
        # Append the rotated character and coordinates to the lists
        rotated_characters.append(char)
        rotated_coordinates.append((new_x, new_y))
    # Fix top left
    if fixTopLeft == True:
        oldTL = getTopLeft(splitPixelGroup["po"])
        newTL = getTopLeft(rotated_coordinates)
        diff = coordinateDifference(oldTL,newTL)
        rotated_coordinates = addDiffToCoords(rotated_coordinates, diff[0], diff[1])
    # Return
    return {"ch":rotated_characters,"po":rotated_coordinates}

def fillBoundaryGap(splitPixelGroup):
    characters = splitPixelGroup["ch"]
    coordinates = splitPixelGroup["po"]
    # fix
    if not characters or not coordinates:
        return {"ch":characters,"po":coordinates}
    # Find the minimum and maximum X and Y coordinates to define the bounding box
    min_x = min(x for x, _ in coordinates)
    max_x = max(x for x, _ in coordinates)
    min_y = min(y for _, y in coordinates)
    max_y = max(y for _, y in coordinates)
    # Initialize a set to keep track of existing coordinates
    existing_coords = set(coordinates)
    # Initialize lists for the new characters and coordinates
    new_characters = characters.copy()
    new_coordinates = coordinates.copy()
    # Iterate through the bounding box
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            # Check if the current coordinate is not in the existing coordinates set
            current_coord = (x, y)
            if current_coord not in existing_coords:
                # Check if the surrounding coordinates are in the existing coordinates set
                neighbors = [(x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
                if any(neighbor in existing_coords for neighbor in neighbors):
                    # Get the left neighbor
                    #leftN = None
                    #mi = 1
                    #while leftN not in existing_coords:
                    #    if mi > (max_x - min_x):
                    #        leftN = coordinates[0]
                    #        break
                    #    leftN = (current_coord[0]-mi,current_coord[1])
                    #    mi += 1
                    left = (current_coord[0]-1,current_coord[1])
                    if left in existing_coords:
                        leftN = left
                    else:
                        leftN = coordinates[0]
                    leftNIndex = coordinates.index(leftN)
                    # Add the left-surrounded character and the empty pixel coordinate
                    new_characters.append(characters[leftNIndex])
                    new_coordinates.append(current_coord)
    # Return
    return {"ch":new_characters,"po":new_coordinates}

def fixPostStretchLPcorner(texture):
    if len(texture) > 1:
        if len(texture[-1]) == len(texture[-2])-1:
            texture[-1] += texture[-1][-1]
        return texture
    else: return texture