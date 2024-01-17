from getDrawlib import getDrawlib
drawlib = getDrawlib()

from types import MethodType

from time import sleep

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

class InvalidPresetId(Exception):
    '''Exception for when the preset requested id is invalid.'''
    def __init__(self,message="ObjectiveCli: An error occured!"):
        self.message = message
        super().__init__(self.message)

class IdOperationError(Exception):
    '''Exception for errors occuring during an id-based operation.'''
    def __init__(self,message="ObjectiveCli: An error occured!"):
        self.message = message
        super().__init__(self.message)

class renObject(OriginPointConnector):
    '''Main render-object for ObjectiveCli.'''
    def __init__(self,objectOrData,origin="TL",_additionalData=None,bgChar=" ",baseColor=None,palette=None):
        self.origin = origin
        self.bgChar = bgChar
        self._additionalData = _additionalData
        _ingested = self._ingest(objectOrData,_return=True)
        super().__init__(_ingested["data"],self.origin)
        self.baseColor = baseColor
        self.palette = palette
    def _ingest_data(self,data):
        '''INTERNAL: Function to ingest object-data.'''
        # pixelGroup: tuple/list < [str,list]
        # cmpxPixelGroup: list < {"char":str,"pos":tuple/list}
        # Texture: list = []
        # Sprite: dict = {xPos:int,yPos:int,tx:list}
        # SplitPixelGroup: dict = {ch:list,po:list}
        # Asset: dict = {"posX":int,"posY":int,"texture":list,"color":str,"extra":str,"comment":str}
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
            elif data.get("posX") != None:
                data = {"xPos":data["posX"], "yPos":data["posY"], "tx":data["texture"]}
                dtype = "sprite" # Asset
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
        # Assets
        elif isinstance(_object,drawlib.assets.asset):
            data = _object.asAssetObj()
            data = {"xPos":data["posX"], "yPos":data["posY"], "tx":data["texture"]}
            dtype = "sprite"
        elif isinstance(_object,drawlib.assets.texture):
            if self._additionalData == None:
                raise InsufficientIngestData("ObjectiveCli: AdditionalData is required for ingesting this datatype!")
            if self._additionalData.get("xPos") == None or self._additionalData.get("yPos") == None:
                raise InsufficientIngestData("ObjectiveCli: AdditionalData must contain xPos and yPos for this datatype!")
            data = _object.asTexture()
            data = {"xPos":self._additionalData["xPos"], "yPos":self._additionalData["yPos"], "tx":data}
            dtype = "sprite"
        elif isinstance(_object,drawlib.objects.assetFileObj):
            data = _object.asSprite()
            dtype = "sprite"
        elif isinstance(_object,drawlib.objects.assetTexture):
            if self._additionalData == None:
                raise InsufficientIngestData("ObjectiveCli: AdditionalData is required for ingesting this datatype!")
            if self._additionalData.get("xPos") == None or self._additionalData.get("yPos") == None:
                raise InsufficientIngestData("ObjectiveCli: AdditionalData must contain xPos and yPos for this datatype!")
            data = _object.asSprite(self._additionalData["xPos"],self._additionalData["yPos"])
            dtype = "sprite"
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
    def draw(self,output=object,drawNc=False,clamps=None,excludeClamped=True):
        '''Attempts drawing the object to given output.'''
        local = self.getData()
        if self._isSprite(local) == True:
            drawlib.dtypes.render_sprite(local,output=output,baseColor=baseColor,palette=palette,drawNc=drawNc,clamps=clamps,excludeClamped=excludeClamped)
        elif self._isSplitPixelGroup(local) == True:
            drawlib.dtypes.render_splitPixelGroup(local,output=output,baseColor=baseColor,palette=palette,drawNc=drawNc,clamps=clamps,excludeClamped=excludeClamped)
    def put(self,output=object,clamps=None,excludeClamped=True):
        '''Attempts putting the object to given output.'''
        local = self.getData()
        if self._isSprite(local) == True:
            drawlib.dtypes.render_sprite(local,output=output,baseColor=self.baseColor,palette=self.palette,supressDraw=True,clamps=clamps,excludeClamped=excludeClamped)
        elif self._isSplitPixelGroup(local) == True:
            drawlib.dtypes.render_splitPixelGroup(local,output=output,baseColor=self.baseColor,palette=self.palette,supressDraw=True,clamps=clamps,excludeClamped=excludeClamped)

default_canvas_outOpts = {
    "buffIChar": None,
    "buffAutoStr": True,
    "buffInst": None,
    "channelObj": None,
    "outputObj": None,
    "autoLink": False
}

class wcCanvas():
    '''Window Coupled canvas for ObjectiveCli.'''
    def __init__(self,width=None,height=None,outputMode="Buffer",outputOpts=default_canvas_outOpts,excludeClamped=True,clampBotX=0,clampBotY=0,clearOnDraw=False):
        self.width = width
        self.height = height
        if type(width) == MethodType: self.width = self.width() # if vw then get value
        if type(height) == MethodType: self.height = self.height() # if vh then get value
        if self.width == None: self.width = drawlib.lib_conUtils.getConSize()[0]
        if self.height == None: self.height = drawlib.lib_conUtils.getConSize()[1]
        self.outputMode = outputMode
        self.outputOpts = outputOpts
        self.excludeClamped = excludeClamped
        self.clampBotX = clampBotX
        self.clampBotY = clampBotY
        self.clearOnDraw = clearOnDraw
        self.drawlib = drawlib
        self._getOutputObj()
        self.objects = {}
        self.drawnObjects = []
        self._getOutputObj()
    def _getOutputObj(self):
        self.output = self.drawlib.DrawlibOut(mode=self.outputMode,overwWidth=self.width,overwHeight=self.height,**self.outputOpts)
    def _getClamps(self) -> tuple:
        return ((self.clampBotX,self.width),(self.clampBotY,self.height))
    def resetHead(self,x=0,y=0):
        self.drawlib.terminal.reset_write_head(x,y)
    def clear(self):
        self.output.clear()
        if self.outputMode not in ["Console"]:
            self.drawlib.lib_conUtils.clear()
    def add(self, renObj=object, oid=None, _unsafe=False):
        prefId = oid
        _id = None
        if prefId == None:
            i = len(self.objects.keys())
            while i in self.objects.keys():
                i += 1
            _id = str(i)
        else:
            if _unsafe:
                _id = str(prefId)
            else:
                if str(prefId) in self.objects.keys():
                    raise InvalidPresetId("ObjectiveCli: Preset id is already present!")
                else:
                    _id = str(prefId)
        if _id != None:
            self.objects[_id] = renObj
        else:
            raise InvalidPresetId("ObjectiveCli: Preset id is invalid!")
        return _id
    def rem(self, oid):
        oid = str(oid)
        if self.objects.get(oid) == None:
            raise IdOperationError(f"ObjectiveCli: Id '{oid}' does not exit!")
        else:
            self.objects.pop(oid)
    def get(self, oid) -> object|None:
        oid = str(oid)
        obj = self.objects.get(oid)
        if obj == None:
            raise IdOperationError(f"ObjectiveCli: Id '{oid}' does not exit!")
        else:
            return obj
    def getId(self, obj):
        for oid,oobj in self.objects.items():
            if obj == oobj:
                return oid
                break
        else:
            raise IdOperationError(f"ObjectiveCli: Object '{obj}' could't be found under this canvas!")
    def moveBy(self, oidOrObj=None, x=0,y=0):
        obj:renObject
        if type(oidOrObj) == object:
            obj = oidOrObj
        else:
            obj = self.get(oidOrObj)
        if x == None or y == None:
            raise IdOperationError("ObjectiveCli: Invalid move-by value given, was None!")
        obj.moveBy(x,y)
    def moveTo(self, oidOrObj=None, x=0,y=0):
        obj:renObject
        if type(oidOrObj) == object:
            obj = oidOrObj
        else:
            obj = self.get(oidOrObj)
        if x == None or y == None or x < 0 or y < 0:
            raise IdOperationError("ObjectiveCli: Invalid move-to value given, was None or bellow 0!")
        obj.moveTo(x,y)
    def markDrawn(self, oidOrObj=None):
        if type(oidOrObj) == object:
            oid = self.getId(oidOrObj)
        if oid not in self.drawnObjects:
            self.drawnObjects.append(oid)
    def unmarkDrawn(self, oidOrObj=None):
        if type(oidOrObj) == object:
            oid = self.getId(oidOrObj)
        if oid in self.drawnObjects:
            self.drawnObjects.remove(oid)
    def putObj(self, oidOrObj=None):
        obj:renObject
        obj = None
        if type(oidOrObj) == object:
            oid = self.getId(oidOrObj)
            if oid not in self.drawnObjects:
                obj = oidOrObj
        else:
            if oidOrObj not in self.drawnObjects:
                obj = self.get(oidOrObj)
        if obj != None:
            obj.put(self.output,clamps=self._getClamps(),excludeClamped=self.excludeClamped)
    def drawObj(self, oidOrObj=None):
        obj:renObject
        obj = None
        if type(oidOrObj) == object:
            oid = self.getId(oidOrObj)
            if oid in self.drawnObjects:
                obj = oidOrObj
        else:
            if oid not in self.drawnObjects:
                obj = self.get(oid)
        if obj != None:
            obj.draw(self.output,clamps=self._getClamps(),excludeClamped=self.excludeClamped)
    def putAll(self):
        for oid in self.objects:
            if oid not in self.drawnObjects:
                self.putObj(oid)
    def draw(self):
        for oid in self.objects.keys():
            if oid not in self.drawnObjects:
                self.putObj(oid)
        self.output.draw(nc=self.clearOnDraw,clamps=self._getClamps())
    def sleep(self,seconds):
        sleep(seconds)
    def fill(self,char=str):
        self.output.fill(char)
    def getSize(self):
        return (self.width,self.height)

    def asSprite(self,oidOrObj):
        obj:renObject
        obj = None
        if type(oidOrObj) != object:
            obj = self.get(oidOrObj)
        if obj != None:
            return obj.asSprite()
    def asSplitPixelGroup(self,oidOrObj):
        obj:renObject
        obj = None
        if type(oidOrObj) != object:
            obj = self.get(oidOrObj)
        if obj != None:
            return obj.asSplitPixelGroup()
    def updateData(self,oidOrObj,objectOrData):
        obj:renObject
        obj = None
        if type(oidOrObj) != object:
            obj = self.get(oidOrObj)
        if obj != None:
            return obj.updateData(objectOrData)
    def stretchShape2X(self,oidOrObj,axis="x",lp=True):
        obj:renObject
        obj = None
        if type(oidOrObj) != object:
            obj = self.get(oidOrObj)
        if obj != None:
            return obj.stretchShape2X(axis=axis,lp=lp)
    def fillShape(self,oidOrObj,fillChar=str):
        obj:renObject
        obj = None
        if type(oidOrObj) != object:
            obj = self.get(oidOrObj)
        if obj != None:
            return obj.fillShape(fillChar=fillChar)
    def rotateShape(self,oidOrObj,degrees,fixTopLeft=False):
        obj:renObject
        obj = None
        if type(oidOrObj) != object:
            obj = self.get(oidOrObj)
        if obj != None:
            return obj.rotateShape(degrees,fixTopLeft=fixTopLeft)
    def fillBoundaryGap(self,oidOrObj):
        obj:renObject
        obj = None
        if type(oidOrObj) != object:
            obj = self.get(oidOrObj)
        if obj != None:
            return obj.fillBoundaryGap()

    def setMode(self,mode):
        if mode in self.output.allowedMods:
            self.output.setM(mode)
            self.outputMode = mode
    def resMode(self):
        self.output.resM()
        self.outputMode = self.output.mode
    def put(self,x=int,y=int,st=str):
        self.output.put(x,y,st,baseColor=self.baseColor,palette=self.palette)
    def mPut(self,coords=list,st=str):
        self.output.mPut(coords,st,baseColor=self.baseColor,palette=self.palette)
    def lPut(self,lines=list,stX=int,stY=int):
        self.output.lPut(lines,stX,stY,baseColor=self.baseColor,palette=self.palette)
    
    def create_renObject(self,classObjOrData,origin="TL",_additionalData=None,bgChar=" ",baseColor=None,palette=None,drawOnCreation=False,creationDrawMode="obj"):
        """
        Creates a rendering object from given class-object/data.
        Additional data that may be required for some datatypes:
            xPos: int (required for TextureObj/TextureData)
            yPos: int (required for Texture/TextureData)
        CreationDrawMode:
            obj: draw the object .drawObj()
            all: draw the whole canvas .putObj(); .draw()
        """
        renObj = renObject(classObjOrData,origin,_additionalData,bgChar,baseColor,palette)
        _id = self.add(renObj)
        if drawOnCreation == True:
            if _id in self.objects.keys():
                if creationDrawMode == "obj":
                    self.drawObj(_id)
                else:
                    self.draw()
        return _id
    def create_drawlibObj(self,drawlibObj,origin="TL",_additionalData=None,bgChar=" ",baseColor=None,palette=None,drawOnCreation=False,creationDrawMode="obj",*args,**kwargs):
        """
        Creates a rendering object from given a given drawlibObj.
        Additional data that may be required for some datatypes:
            xPos: int (required for TextureObj/TextureData)
            yPos: int (required for Texture/TextureData)
        CreationDrawMode:
            obj: draw the object .drawObj()
            all: draw the whole canvas .putObj(); .draw()
        """
        if isinstance(drawlibObj,self.drawlib.assets.asset) or isinstance(drawlibObj,self.drawlib.objects.assetFileObj):
            sobj = drawlibObj(*args,output=self.output,palette=palette,**kwargs)
        else:
            sobj = drawlibObj(*args,output=self.output,baseColor=baseColor,palette=palette,**kwargs)
        return self.create_renObject(sobj,origin,_additionalData,bgChar,baseColor,palette,drawOnCreation,creationDrawMode)

    def create_point(self,charset,p1=tuple,origin="TL",_additionalData=None,baseColor=None,palette=drawlib.coloring.DrawlibStdPalette,charFunc=drawlib.generators.baseGenerator,autoGenerate=False,drawOnCreation=False,creationDrawMode="obj",bgChar=" "):
        drawlibObj = self.drawlib.objects.pointObj
        return self.create_drawlibObj(drawlibObj,origin=origin,_additionalData=_additionalData,baseColor=baseColor,palette=palette,charset=charset,x1=p1[0],y1=p1[1],charFunc=charFunc,autoGenerate=autoGenerate,drawOnCreation=drawOnCreation,creationDrawMode=creationDrawMode,bgChar=bgChar)
    def create_line(self,charset,p1=tuple,p2=tuple,origin="TL",_additionalData=None,baseColor=None,palette=drawlib.coloring.DrawlibStdPalette,charFunc=drawlib.generators.baseGenerator,autoGenerate=False,drawOnCreation=False,creationDrawMode="obj",bgChar=" "):
        drawlibObj = self.drawlib.objects.lineObj
        return self.create_drawlibObj(drawlibObj,origin=origin,_additionalData=_additionalData,baseColor=baseColor,palette=palette,charset=charset,x1=p1[0],y1=p1[1],x2=p2[0],y2=p2[1],charFunc=charFunc,autoGenerate=autoGenerate,drawOnCreation=drawOnCreation,creationDrawMode=creationDrawMode,bgChar=bgChar)
    def create_triangle(self,charset,p1=tuple,p2=tuple,p3=tuple,origin="TL",_additionalData=None,baseColor=None,palette=drawlib.coloring.DrawlibStdPalette,charFunc=drawlib.generators.baseGenerator,autoGenerate=False,drawOnCreation=False,creationDrawMode="obj",bgChar=" "):
        drawlibObj = self.drawlib.objects.triangleObj
        return self.create_drawlibObj(drawlibObj,origin=origin,_additionalData=_additionalData,baseColor=baseColor,palette=palette,charset=charset,x1=p1[0],y1=p1[1],x2=p2[0],y2=p2[1],x3=p3[0],y3=p3[1],charFunc=charFunc,autoGenerate=autoGenerate,drawOnCreation=drawOnCreation,creationDrawMode=creationDrawMode,bgChar=bgChar)
    def create_rectangle(self,charset,p1=tuple,p2=tuple,p3=tuple,p4=tuple,origin="TL",_additionalData=None,baseColor=None,palette=drawlib.coloring.DrawlibStdPalette,charFunc=drawlib.generators.baseGenerator,autoGenerate=False,drawOnCreation=False,creationDrawMode="obj",bgChar=" "):
        drawlibObj = self.drawlib.objects.rectangleObj
        return self.create_drawlibObj(drawlibObj,origin=origin,_additionalData=_additionalData,baseColor=baseColor,palette=palette,charset=charset,x1=p1[0],y1=p1[1],x2=p2[0],y2=p2[1],x3=p3[0],y3=p3[1],x4=p4[0],y4=p4[1],charFunc=charFunc,autoGenerate=autoGenerate,drawOnCreation=drawOnCreation,creationDrawMode=creationDrawMode,bgChar=bgChar)
    def create_rectangle2(self,charset,p1=tuple,p2=tuple,origin="TL",_additionalData=None,baseColor=None,palette=drawlib.coloring.DrawlibStdPalette,charFunc=drawlib.generators.baseGenerator,autoGenerate=False,drawOnCreation=False,creationDrawMode="obj",bgChar=" "):
        drawlibObj = self.drawlib.objects.rectangleObj2
        return self.create_drawlibObj(drawlibObj,origin=origin,_additionalData=_additionalData,baseColor=baseColor,palette=palette,charset=charset,c1=p1,c2=p2,charFunc=charFunc,autoGenerate=autoGenerate,drawOnCreation=drawOnCreation,creationDrawMode=creationDrawMode,bgChar=bgChar)
    def create_circle(self,charset,p1=tuple,radius=int,origin="TL",_additionalData=None,baseColor=None,palette=drawlib.coloring.DrawlibStdPalette,charFunc=drawlib.generators.baseGenerator,autoGenerate=False,drawOnCreation=False,creationDrawMode="obj",bgChar=" "):
        drawlibObj = self.drawlib.objects.circleObj
        return self.create_drawlibObj(drawlibObj,origin=origin,_additionalData=_additionalData,baseColor=baseColor,palette=palette,charset=charset,xM=p1[0],yM=p1[1],r=radius,charFunc=charFunc,autoGenerate=autoGenerate,drawOnCreation=drawOnCreation,creationDrawMode=creationDrawMode,bgChar=bgChar)
    def create_ellipse(self,charset,p1=tuple,radius1=int,radius2=int,origin="TL",_additionalData=None,baseColor=None,palette=drawlib.coloring.DrawlibStdPalette,charFunc=drawlib.generators.baseGenerator,autoGenerate=False,drawOnCreation=False,creationDrawMode="obj",bgChar=" "):
        drawlibObj = self.drawlib.objects.ellipseObj
        return self.create_drawlibObj(drawlibObj,origin=origin,_additionalData=_additionalData,baseColor=baseColor,palette=palette,charset=charset,cX=p1[0],cY=p1[1],xRad=radius1,yRad=radius2,charFunc=charFunc,autoGenerate=autoGenerate,drawOnCreation=drawOnCreation,creationDrawMode=creationDrawMode,bgChar=bgChar)
    def create_quadBezier(self,charset,sp=tuple,cp=tuple,ep=tuple,origin="TL",_additionalData=None,baseColor=None,palette=drawlib.coloring.DrawlibStdPalette,charFunc=drawlib.generators.baseGenerator,autoGenerate=False,drawOnCreation=False,creationDrawMode="obj",bgChar=" "):
        drawlibObj = self.drawlib.objects.quadBezierObj
        return self.create_drawlibObj(drawlibObj,origin=origin,_additionalData=_additionalData,baseColor=baseColor,palette=palette,charset=charset,sX=sp[0],sY=sp[1],cX=cp[0],cY=cp[1],eX=ep[0],eY=ep[1],charFunc=charFunc,autoGenerate=autoGenerate,drawOnCreation=drawOnCreation,creationDrawMode=creationDrawMode,bgChar=bgChar)
    def create_cubicBezier(self,charset,sp=tuple,c1=tuple,c2=tuple,ep=tuple,origin="TL",_additionalData=None,baseColor=None,palette=drawlib.coloring.DrawlibStdPalette,charFunc=drawlib.generators.baseGenerator,autoGenerate=False,drawOnCreation=False,creationDrawMode="obj",bgChar=" "):
        drawlibObj = self.drawlib.objects.cubicBezierObj
        return self.create_drawlibObj(drawlibObj,origin=origin,_additionalData=_additionalData,baseColor=baseColor,palette=palette,charset=charset,sX=sp[0],sY=sp[1],c1X=c1[0],c1Y=c1[1],c2X=c2[0],c2Y=c2[1],eX=ep[0],eY=ep[1],charFunc=charFunc,autoGenerate=autoGenerate,drawOnCreation=drawOnCreation,creationDrawMode=creationDrawMode,bgChar=bgChar)

    def create_assetFile(self,filepath=str,origin="TL",_additionalData=None,palette=drawlib.coloring.DrawlibStdPalette,charFunc=drawlib.generators.baseGenerator,autoGenerate=False,drawOnCreation=False,creationDrawMode="obj",bgChar=" "):
        drawlibObj = self.drawlib.objects.assetFileObj
        return self.create_drawlibObj(drawlibObj,origin=origin,_additionalData=_additionalData,palette=palette,filepath=filepath,charFunc=charFunc,autoGenerate=autoGenerate,drawOnCreation=drawOnCreation,creationDrawMode=creationDrawMode,bgChar=bgChar)
    def create_assetTexture(self,p1=tuple,filepath=str,origin="TL",_additionalData=None,baseColor=None,palette=drawlib.coloring.DrawlibStdPalette,charFunc=drawlib.generators.baseGenerator,autoGenerate=False,drawOnCreation=False,creationDrawMode="obj",bgChar=" "):
        drawlibObj = self.drawlib.objects.assetTexture
        return self.create_drawlibObj(drawlibObj,origin=origin,_additionalData=_additionalData,baseColor=baseColor,palette=palette,filepath=filepath,posov=p1,charFunc=charFunc,autoGenerate=autoGenerate,drawOnCreation=drawOnCreation,creationDrawMode=creationDrawMode,bgChar=bgChar)

    def create_asciiImage(self,imagePath=str,mode="standard",char=None,pc=False,method="lum",invert=False,monochrome=False,width=None,height=None,resampling="lanczos",textureCodec=None,noSafeConv=False,xPos=None,yPos=None,strTxtMethod=False, origin="TL",_additionalData=None,baseColor=None,palette=drawlib.coloring.DrawlibStdPalette,drawOnCreation=False,creationDrawMode=False,bgChar=" "):
        drawlibObj = self.drawlib.imaging.boxImage
        return self.create_drawlibObj(drawlibObj,imagePath=imagePath,mode=mode,char=char,pc=pc,method=method,invert=invert,monochrome=monochrome,width=width,height=height,resampling=resampling,textureCodec=textureCodec,noSafeConv=noSafeConv,xPos=xPos,yPos=yPos,strTxtMethod=strTxtMethod, origin=origin,_additionalData=_additionalData,baseColor=baseColor,palette=palette,drawOnCreation=drawOnCreation,creationDrawMode=creationDrawMode,bgChar=bgChar)
    def create_boxImage(self,imagePath=str,mode="foreground",char=None,monochrome=False,width=None,height=None,resampling="lanczos",method=None,textureCodec=None,noSafeConv=False,xPos=None,yPos=None,strTxtMethod=False, origin="TL",_additionalData=None,baseColor=None,palette=drawlib.coloring.DrawlibStdPalette,drawOnCreation=False,creationDrawMode=False,bgChar=" "):
        drawlibObj = self.drawlib.imaging.boxImage
        return self.create_drawlibObj(drawlibObj,imagePath=imagePath,mode=mode,char=char,monochrome=monochrome,width=width,height=height,resampling=resampling,method=method,textureCodec=textureCodec,noSafeConv=noSafeConv,xPos=xPos,yPos=yPos,strTxtMethod=strTxtMethod, origin=origin,_additionalData=_additionalData,baseColor=baseColor,palette=palette,drawOnCreation=drawOnCreation,creationDrawMode=creationDrawMode,bgChar=bgChar)
