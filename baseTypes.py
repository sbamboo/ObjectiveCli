from getDrawlib import getDrawlib
drawlib = getDrawlib()

from tools import *

class InsufficientIngestData(Exception):
    '''Exception for insufficient ingest data.'''
    def __init__(self,message="ObjectiveCli: Insufficient ingest data!"):
        self.message = message
        super().__init__(self.message)

class InvalidIngestData(Exception):
    '''Exception for invalid ingest data.'''
    def __init__(self,message="ObjectiveCli: Invalid ingest data!"):
        self.message = message
        super().__init__(self.message)

class renObject(OriginPointConnector):
    '''Main render-object for ObjectiveCli.'''
    def __init__(self,objectOrData,origin="TL",_additionalData=None,bgChar=" "):
        self.origin = origin
        self.bgChar = bgChar
        self._additionalData = _additionalData
        _ingested = self._ingest(objectOrData,_return=True)
        super().__init__(_ingested["data"],self.origin)
    def _ingest_data(self,data):
        '''INTERNAL: Function to ingest object-data.'''
        # pixelGroup: tuple/list < [str,list]
        # cmpxPixelGroup: list < {"char":str,"pos":tuple/list}
        # Texture: list = []
        # Sprite: dict = {xPos:int,yPos:int,tx:list}
        # SplitPixelGroup: dict = {ch:list,po:list}
        if type(data) == tuple:
            cmpx = drawlib.dtypes.pixelGroup_to_cmpxPixelGroup(data[0],data[1]) #pixelGroup
            data = drawlib.dtypes.cmpxPixelGroup_to_SplitPixelGroup(cmpx)
            dtype = "splitPixelGroup"
        elif type(data) == list:
            if type(data[0]) == dict:
                data = drawlib.dtypes.cmpxPixelGroup_to_SplitPixelGroup(cmpx) # cmpxPixelGroup
                dtype = "splitPixelGroup"
            elif type(data[0]) == str:
                cmpx = drawlib.dtypes.pixelGroup_to_cmpxPixelGroup(data[0],data[1]) #pixelGroup
                data = drawlib.dtypes.cmpxPixelGroup_to_SplitPixelGroup(cmpx)
                dtype = "splitPixelGroup"
            else:
                if self._additionalData == None:
                    raise InsufficientIngestData("ObjectiveCli: AdditionalData is required for ingesting this datatype!")
                if self._additionalData.get("xPos") == None or self._additionalData.get("yPos") == None:
                    raise InsufficientIngestData("ObjectiveCli: AdditionalData must contain xPos and yPos for this datatype!")
                data = {"xPos":self._additionalData["xPos"], "yPos":self._additionalData["yPos"], "tx":data} # Texture
                dtype = "sprite"
        elif type(data) == dict:
            if data.get("xPos") != None:
                dtype = "sprite" # Sprite
            else:
                dtype = "splitPixelGroup" # SplitPixelGroup
        else:
            raise InvalidIngestData(f"ObjectiveCli: Invalid data datatype!\n{data}")
        # Return
        return {"dtype":dtype,"data":data}
    def _ingest_object(self,_object):
        '''INTERNAL: Function to ingest data from objects.'''
        # texture or sprite
        if   isinstance(_object,drawlib.dtypes.sprite):
            data = _object.asSprite()
            dtype = "sprite"
        elif isinstance(_object,drawlib.dtypes.texture):
            if self._additionalData == None:
                raise InsufficientIngestData("ObjectiveCli: AdditionalData is required for ingesting this datatype!")
            if self._additionalData.get("xPos") == None or self._additionalData.get("yPos") == None:
                raise InsufficientIngestData("ObjectiveCli: AdditionalData must contain xPos and yPos for this datatype!")
            data = _object.asSprite(self._additionalData["xPos"],self._additionalData["yPos"])
            dtype = "sprite"
        # Other
        elif isinstance(_object,drawlib.dtypes.pixelGroup) or isinstance(_object,drawlib.dtypes.cmpxPixelGroup) or isinstance(_object,drawlib.dtypes.splitPixelGroup):
            data = _object.asSplitPixelGroup()
            dtype = "splitPixelGroup"
        # Objects
        elif isinstance(_object,drawlib.objects.drawlibObj):
            data = _object.asSplitPixelGroup()
            dtype = "splitPixelGroup"
        # Else fail
        else:
            raise InvalidIngestData(f"ObjectiveCli: Invalid object datatype!\n{_object}")
        # Return
        return {"dtype":dtype,"data":data}
    def _ingest(self,objectOrData,_return=False):
        '''INTERNAL: Function to ingest data from objects/data.'''
        if isinstance(objectOrData,object):
            ingested = self._ingest_object(objectOrData)
        else:
            ingested = self._ingest_data(objectOrData)
        if ingested == None:
            raise InvalidIngestData(f"ObjectiveCli: Invalid ingest data!\n{objectOrData}")
        if _return == True: return ingested
        else:
            self._updateData(ingested["data"])
    def _getType(self):
        '''INTERNAL: Function to to get the type of the internal data.'''
        local = self.getData()
        if self._isSprite(local) == True:
            return "sprite"
        else:
            return "splitPixelGroup"
    def asSprite(self):
        '''Get the internal data as a sprite.'''
        local = self.getData()
        if self._isSprite(local) == True:
            return local
        elif self._isSplitPixelGroup(local) == True:
            cmpx = drawlib.dtypes.splitPixelGroup_to_cmpxPixelGroup(local)
            return drawlib.dtypes.cmpxPixelGroup_to_sprite(cmpx,self.bgChar)
        else:
            raise InvalidIngestData(f"ObjectiveCli: Invalid ingest data!\n{local}")
    def asSplitPixelGroup(self):
        '''Get the internal data as a splitPixelGroup.'''
        local = self.getData()
        if self._isSprite(local) == True:
            cmpx = drawlib.dtypes.sprite_to_cmpxPixelGroup(local,exclusionChar=self.bgChar)
            return drawlib.dtypes.cmpxPixelGroup_to_splitPixelGroup(cmpx)
        elif self._isSplitPixelGroup(local) == True:
            return local
        else:
            raise InvalidIngestData(f"ObjectiveCli: Invalid ingest data!\n{local}")
    def updateData(self,objectOrData):
        '''Takes a object/data and ingests it. (converts to internal data)'''
        self._ingest(objectOrData)
    def stretchShape2X(self,axis="x",lp=True):
        """
        NOTE! Manip functions may not be fully compatible with formatted data.
        Stretches the object-pixels by 2x, in given axis. (manip.stretchShape2X)
        axis: "x" or "y"
        lp: Goes quadrant by quadrant, instead of stretching the whole shape, some shapes may look better with this and some may look worse.
            lp tries to keep shape-width so might interfere with some things.
        """
        local = self.getData()
        if self._isSprite(local) == True:
            local["tx"] = drawlib.manip.stretchShape(local["tx"],axis=axis,lp=lp)
            self._updateData(local)
        elif self._isSplitPixelGroup(local) == True:
            cmpx = drawlib.dtypes.splitPixelGroup_to_cmpxPixelGroup(local)
            sprite = drawlib.dtypes.cmpxPixelGroup_to_sprite(cmpx,self.bgChar)
            sprite["tx"] = drawlib.manip.stretchShape(sprite["tx"],axis=axis,lp=lp)
            cmpx = drawlib.dtypes.sprite_to_cmpxPixelGroup(sprite,self.bgChar)
            splitPixelGroup = drawlib.dtypes.cmpxPixelGroup_to_splitPixelGroup(cmpx)
            self._updateData(splitPixelGroup)
    def fillShape(self,fillChar=str):
        """
        NOTE! Manip functions may not be fully compatible with formatted data.
        Fills the object-pixels. (manip.fillShape)
        """
        local = self.getData()
        if self._isSprite(local) == True:
            local["tx"] = drawlib.manip.fillShape(local["tx"],fillChar=fillChar)
            self._updateData(local)
        elif self._isSplitPixelGroup(local) == True:
            cmpx = drawlib.dtypes.splitPixelGroup_to_cmpxPixelGroup(local)
            sprite = drawlib.dtypes.cmpxPixelGroup_to_sprite(cmpx,self.bgChar)
            sprite["tx"] = drawlib.manip.fillShape(sprite["tx"],fillChar=fillChar)
            cmpx = drawlib.dtypes.sprite_to_cmpxPixelGroup(sprite,self.bgChar)
            splitPixelGroup = drawlib.dtypes.cmpxPixelGroup_to_splitPixelGroup(cmpx)
            self._updateData(splitPixelGroup)
    def rotateShape(self,degrees,fixTopLeft=False):
        """
        NOTE! Manip functions may not be fully compatible with formatted data.
        Rotates the object-pixels by a given degree. (manip.rotateShape)\nfixTopLeft: Somtimes the top-left pixel gets funky then enable this to attempt a fix.
        """
        local = self.getData()
        if self._isSprite(local) == True:
            cmpx = drawlib.dtypes.sprite_to_cmpxPixelGroup(local,self.bgChar)
            spg = drawlib.dtypes.cmpxPixelGroup_to_splitPixelGroup(cmpx)
            spg = drawlib.manip.rotateSplitPixelGroup(spg, degrees, fixTopLeft)
            cmpx = drawlib.dtypes.splitPixelGroup_to_cmpxPixelGroup(spg)
            splitPixelGroup = drawlib.dtypes.cmpxPixelGroup_to_sprite(cmpx,self.bgChar)
            self._updateData(splitPixelGroup)
        elif self._isSplitPixelGroup(local) == True:
            local = drawlib.manip.rotateSplitPixelGroup(local, degrees, fixTopLeft)
            self._updateData(local)
    def fillBoundaryGap(self):
        """
        NOTE! Manip functions may not be fully compatible with formatted data.
        Fills-in gaps in the object-pixels. (manip.fillBoundaryGap)
        """
        local = self.getData()
        if self._isSprite(local) == True:
            cmpx = drawlib.dtypes.sprite_to_cmpxPixelGroup(local,self.bgChar)
            spg = drawlib.dtypes.cmpxPixelGroup_to_splitPixelGroup(cmpx)
            spg = drawlib.manip.fillBoundaryGap(spg)
            cmpx = drawlib.dtypes.splitPixelGroup_to_cmpxPixelGroup(spg)
            splitPixelGroup = drawlib.dtypes.cmpxPixelGroup_to_sprite(cmpx,self.bgChar)
            self._updateData(splitPixelGroup)
        elif self._isSplitPixelGroup(local) == True:
            local = drawlib.manip.fillBoundaryGap(local)
            self._updateData(local)
    def draw(self,output=object,baseColor=None,palette=None,drawNc=False,clamps=None,excludeClamped=True):
        '''Attempts drawing the object to given output.'''
        local = self.getData()
        if self._isSprite(local) == True:
            drawlib.dtypes.render_sprite(local,output=output,baseColor=baseColor,palette=palette,drawNc=drawNc,clamps=clamps,excludeClamped=excludeClamped)
        elif self._isSplitPixelGroup(local) == True:
            drawlib.dtypes.render_splitPixelGroup(local,output=output,baseColor=baseColor,palette=palette,drawNc=drawNc,clamps=clamps,excludeClamped=excludeClamped)
    def put(self,output=object,baseColor=None,palette=None,clamps=None,excludeClamped=True):
        '''Attempts putting the object to given output.'''
        local = self.getData()
        if self._isSprite(local) == True:
            drawlib.dtypes.render_sprite(local,output=output,baseColor=baseColor,palette=palette,supressDraw=True,clamps=clamps,excludeClamped=excludeClamped)
        elif self._isSplitPixelGroup(local) == True:
            drawlib.dtypes.render_splitPixelGroup(local,output=output,baseColor=baseColor,palette=palette,supressDraw=True,clamps=clamps,excludeClamped=excludeClamped)

default_canvas_outOpts = {
    "overwWidth": None,
    "overwHeight": None,
    "buffIChar": None,
    "buffAutoStr": True,
    "buffInst": None,
    "channelObj": None,
    "outputObj": None,
    "autoLink": False
}

class canvas():
    def __init__(self,width=int,height=int,outputMode="Buffer",outputOpts=default_canvas_outOpts):
        self.width = width
        self.height = height
        self.outputMode = outputMode
        self.outputOpts = outputOpts
        self.drawlib = drawlib
        self._getOutputObj()
        self.objects = {}
        self.drawnObjects = []
    def _getOutputObj(self):
        self.output = self.drawlib.DrawlibOut(mode=self.outputMode,**self.outputOpts)
    def resetHead(self,x=0,y=0):
        self.drawlib.terminal.reset_write_head(x,y)
    def clear(self):
        self.output.clear()
        if self.outputMode not in ["Console","Hybrid"]:
            self.drawlib.lib_conUtils.clear()

# current implementation uses clear() and with multiple canvases this will cause problem, should it:
#   a) clear only the canvas
#   b) clear the whole screen (current)
#   c) cause a redraw of the canvas
#   d) should the canvas be implemented into the window like before
#
# i guess smartest would be to differ between when the canvas in in window-coupled mode and just as an object,
# apon object it should "erase" and if window-coupled it should clear()