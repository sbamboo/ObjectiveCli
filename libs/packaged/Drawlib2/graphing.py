import re
import numpy as np
from sympy import symbols, lambdify
import matplotlib.pyplot as plt

from .pointGroupAlgorithms import beethams_line_algorithm

def parse_function_string(function_string):
    function_string = function_string.replace("^","**")
    # Using regular expression to parse the function string
    match = re.match(r'^(\w)\((\w)\)\s*=\s*(.+)$', function_string)
    
    if match:
        func_char, var, equation = match.groups()
        return func_char, var, equation
    else:
        raise ValueError("Invalid function string format. Example format: f(x) = x**2")

def remove_duplicates(plot_return):
    seenPostions = []
    filter = {"positions":[],"data":[],"func":plot_return["func"]}
    for i in range(len(plot_return["positions"])):
        pos = plot_return["positions"][i]
        if pos not in seenPostions:
            seenPostions.append(pos)
            filter["positions"].append(pos)
            filter["data"].append(plot_return["data"][i])
    return filter


def plot_function(function_string, x_range=(-10, 10), y_range=(-10,10), step=1, xFactor=1, yFactor=1,floatRndDecis=2, intRound=True, debug=False, debug_x_scale=1.0, debug_y_scale=1.0, debugGrid=False):
    func_char, var, equation = parse_function_string(function_string)

    # Create a symbolic variable
    x = symbols(var)

    # Convert the equation to a symbolic expression
    expr = eval(equation)

    # Lambdify the expression for numerical evaluation
    func = lambdify(x, expr, 'numpy')

    # Create a list of tuples for each scaled point within the specified ranges
    posPoints = [
        (round(x_val, floatRndDecis), round(func(x_val), floatRndDecis))
        for x_val in np.arange(x_range[0], x_range[1] + 1, step)
        if y_range is None or (y_range[0] <= func(x_val) <= y_range[1])
    ]

    # Multiply the values by a calculated scale factor to ensure ints
    dataPoints = posPoints.copy()
    posPoints = [(x_val*xFactor, y_val*yFactor) for x_val, y_val in posPoints]
    if intRound:
        posPoints = [(round(x_val), round(y_val)) for x_val, y_val in posPoints]

    if debug:
        x_values = np.linspace(x_range[0], x_range[1], 1000)
        y_values = func(x_values)

        plt.plot(x_values, y_values, label=f'{func_char}({var})={equation.replace("**","^")}')
        plt.scatter(*zip(*dataPoints), color='gray', label=f'Data Points (xF:{xFactor},yF:{yFactor})')
        plt.scatter(*zip(*posPoints), color='red', label='Positions')
        plt.xlabel(var)
        plt.ylabel(f'{func_char}({var})')

        # Adjust ticks based on x_scale and y_scale
        plt.xticks(np.arange(int(x_range[0]), int(x_range[1]) + 1, debug_x_scale))
        if y_range is not None:
            plt.yticks(np.arange(int(y_range[0]), int(y_range[1]) + 1, debug_y_scale))  # Use y_scale

        plt.legend()
        plt.grid(debugGrid)
        plt.title(f'Graph of {func_char}({var})={equation.replace("**","^")}')
        
        # Set limits for x and y axes
        plt.xlim(x_range)
        if y_range is not None:
            plt.ylim(y_range)

        plt.show()

    return remove_duplicates({"positions":posPoints,"data":dataPoints,"func":func})

class AttemptedOperationOnUnplottedGraph(Exception):
    def __init__(self,message="Drawlib.Graphing: Attempted method on unplotted grap, use .plot(...) first!"):
        self.message = message
        super().__init__(self.message)

class graphPlotter():
    def __init__(self,function,output=object,pointChar="X",fillChar="*"):
        self.function = function
        self.output = output
        self.pointChar = pointChar
        self.fillChar = fillChar
        self.data = None

    def _getTopMost(self,positions) -> int:
        topMostFound = None
        for pos in positions:
            if topMostFound == None:
                topMostFound = pos[1]
            else:
                if pos[1] < topMostFound:
                    topMostFound = pos[1]
        return topMostFound
    def _getLeftMost(self,positions) -> int:
        topLeftFound = None
        for pos in positions:
            if topLeftFound == None:
                topLeftFound = pos[0]
            else:
                if pos[0] < topLeftFound:
                    topLeftFound = pos[0]
        return topLeftFound
    def _getBottomMost(self,positions) -> int:
        topBottomFound = None
        for pos in positions:
            if topBottomFound == None:
                topBottomFound = pos[1]
            else:
                if pos[1] > topBottomFound:
                    topBottomFound = pos[1]
        return topBottomFound
    def _getRightMost(self,positions) -> int:
        topRightFound = None
        for pos in positions:
            if topRightFound == None:
                topRightFound = pos[0]
            else:
                if pos[0] > topRightFound:
                    topRightFound = pos[0]
        return topRightFound
    def _getSize(self,positions):
        width = self._getRightMost(positions) - self._getLeftMost(positions)
        height = self._getBottomMost(positions) - self._getTopMost(positions)
        return (width,height)
    
    def _invertY(self,positions):
        newPositions = []
        for pos in positions:
            yDiff = 0 + pos[1]
            newPositions.append( (pos[0],pos[1]-(yDiff*2)) )
        return newPositions
    
    def _changeToDispCoords(self,reff=(0,0),positions=list):
        positions = self._invertY(positions)
        leftMost = self._getLeftMost(positions)
        topMost = self._getTopMost(positions)
        xDiff = reff[0]+1 - leftMost
        yDiff = reff[1]+1 - topMost
        newPositions = []
        for pos in positions:
            newPositions.append( (pos[0]+xDiff,pos[1]+yDiff) )
        return newPositions
    
    def plot(self,pos=(0,0),xRange=(-10,10),yRange=(-10,10),step=1.0,xFactor=1.0,yFactor=1.0,floatRndDecis=2,intRound=True,assumptionFill=False,debug=False,debug_x_scale=1.0,debug_y_scale=1.0,debugGrid=True):
        self.data = plot_function(self.function,x_range=xRange,y_range=yRange,step=step,xFactor=xFactor,yFactor=yFactor,floatRndDecis=floatRndDecis,intRound=intRound,debug=debug,debug_x_scale=debug_x_scale,debug_y_scale=debug_y_scale,debugGrid=debugGrid)
        self.data["pixels"] = self._changeToDispCoords(pos,self.data["positions"])
        self.data["fillPixels"] = []
        if assumptionFill == True:
            pixels = self.data["pixels"]
            for ii in range(0,len(pixels)):
               i = ii-1
               if i >= 0:
                p1 = pixels[i]
                p2 = pixels[ii]
                self.data["fillPixels"].extend( beethams_line_algorithm(*p1,*p2) )
            
    def put(self):
        if self.data == None: raise AttemptedOperationOnUnplottedGraph()
        if self.data["fillPixels"] != []:
            self.output.mPut(self.data["fillPixels"],self.fillChar)
        self.output.mPut(self.data["pixels"],self.pointChar)

    def getAsTx(self):
        total = self.data["pixels"].copy()
        total.extend(self.data["fillPixels"].copy())
        width,height = self._getSize(total)
        lines = []
        for _ in range(height+1):
            line = []
            for _ in range(width+1):
                line.append("")
            lines.append(line)
        for pos in self.data["fillPixels"]:
            lines[pos[1]-1][pos[0]-1] = self.fillChar
        for pos in self.data["pixels"]:
            lines[pos[1]-1][pos[0]-1] = self.pointChar
        return lines

    def getValForPx(self,pixel=tuple):
        if self.data == None: raise AttemptedOperationOnUnplottedGraph()
        index = self.data["pixels"].index(pixel)
        return self.data["data"][index]
    def getPxForVal(self,val=tuple):
        if self.data == None: raise AttemptedOperationOnUnplottedGraph()
        index = self.data["data"].index(val)
        return self.data["pixels"][index]
    
    def getY(self,x):
        return self.data["func"](x)
    def getYval(self,x):
        for pos in self.data["pixels"]:
            if x == pos[0]:
                return pos[1]
