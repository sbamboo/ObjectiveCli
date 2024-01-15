import os,json

_parent = os.path.dirname(os.path.abspath(__file__))

_libJson_1 = os.path.join(_parent, 'lib.json')
_libJson_2 = os.path.join(_parent, 'Drawlib2', 'lib.json')

if os.path.exists(_libJson_1):
    _libJson = _libJson_1
elif os.path.exists(_libJson_2):
    _libJson = _libJson_2
else:
    raise Exception('lib.json not found!')

_versionData = json.loads(open(_libJson,'r').read())

def getInfo():
    return _versionData

def hasVersion(ver_numerical=None,ver_id=None):
    if ver_numerical == None and ver_id == None:
        raise ValueError("Please provide either ver_numeral or ver_id!")
    elif ver_numerical != None and ver_id != None:
        raise ValueError("Please provide either ver_numeral or ver_id!")
    else:
        _verNum = _versionData["libInfo"]["version"]
        _verId = _versionData["libInfo"]["vid"]
        if ver_numerical != None:
            if type(ver_numerical) != str:
                raise TypeError("ver_numerical must be str!")
            if ver_numerical == _verNum:
                return True
            else:
                return False
        elif ver_id != None:
            if type(ver_id) != int:
                raise TypeError("ver_id must be int!")
            if ver_id == _verId:
                return True
            else:
                return False