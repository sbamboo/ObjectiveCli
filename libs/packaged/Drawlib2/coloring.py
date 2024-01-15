import re

from .libs.stringTags import formatStringTags

DrawlibStdPalette = {
    "f_Black": "90m",
    "b_Black": "100m",
    "f_Red": "91m",
    "b_Red": "101m",
    "f_Green": "92m",
    "b_Green": "102m",
    "f_Yellow": "93m",
    "b_Yellow": "103m",
    "f_Blue": "94m",
    "b_Blue": "104m",
    "f_Magenta": "95m",
    "b_Magenta": "105m",
    "f_Cyan": "96m",
    "b_Cyan": "106m",
    "f_White": "97m",
    "b_White": "107m",
    "f_DarkBlack": "30m",
    "b_DarkBlack": "40m",
    "f_DarkRed": "31m",
    "b_DarkRed": "41m",
    "f_DarkGreen": "32m",
    "b_DarkGreen": "42m",
    "f_DarkYellow": "33m",
    "b_DarkYellow": "43m",
    "f_DarkBlue": "34m",
    "b_DarkBlue": "44m",
    "f_DarkMagenta": "35m",
    "b_DarkMagenta": "45m",
    "f_DarkCyan": "36m",
    "b_DarkCyan": "46m",
    "f_DarkWhite": "37m",
    "b_DarkWhite": "47m"
}

def removeAnsiSequences(inputString):
    # Define a regular expression pattern to match ANSI escape sequences
    ansiPattern = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    # Use re.sub to replace ANSI sequences with an empty string
    cleanedString = ansiPattern.sub('', inputString)
    return cleanedString

# Function to also autoNone if invalid input is given
def autoNoneColor(color,palette):
    if color == None or palette == None or type(palette) != dict:
        return None
    else:
        if palette.get(color) != None:
            val = palette.get(color)
            if "#" in val:
                background = False
                if val.strip().startswith("#!"):
                    background = True
                    val = val.replace("#!","#",1)
                val = val.replace("#","")
                lv = len(val)
                rgb = [int(val[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)]
                val = '{};2;{};{};{}'.format(48 if background else 38, rgb[0],rgb[1],rgb[2]) + "m"
            else:
                return val
        else:
            lowPalette = {}
            for key in palette.keys():
                lowPalette[key.lower()] = palette[key]
            if lowPalette.get(color) != None:
                val = lowPalette.get(color)
                if "#" in val:
                    background = False
                    if val.strip().startswith("#!"):
                        background = True
                        val = val.replace("#!","#",1)
                    val = val.replace("#","")
                    lv = len(val)
                    rgb = [int(val[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)]
                    val = '{};2;{};{};{}'.format(48 if background else 38, rgb[0],rgb[1],rgb[2]) + "m"
                else:
                    return val

class TextObj():
    def __init__(self,text,customTags={}):
        self.stdPalette = DrawlibStdPalette
        self.palette = self.stdPalette
        self.text = text
        self.customTags = customTags
    def setPalette(self,palette):
        self.palette = palette
    def resPalette(self):
        self.palette = self.stdPalette
    def setText(self,text):
        self.text = text
    def setTags(self,tags=dict):
        self.customTags = tags
    def retFormat(self):
        # format stringTags
        return formatStringTags(
            inputText=self.text,
            allowedVariables={},
            customTags=self.customTags
        )
    def __str__(self):
        return self.retFormat()
    def __len__(self):
        return len(removeAnsiSequences(self.__str__()))
    def __getitem__(self,index):
        return removeAnsiSequences(self.__str__())[index]
    def split(self,*args,**kwargs):
        return str(self).split(*args,**kwargs)
    def exprt(self) -> dict:
        return {
            "stdPalette": self.stdPalette,
            "palette": self.palette,
            "text": self.text,
            "customTags": self.customTags
        }
    def imprt(self,data=dict):
        self.stdPalette = data["stdPalette"]
        self.palette = data["palette"]
        self.text = data["text"]
        self.customTags = data["customTags"]