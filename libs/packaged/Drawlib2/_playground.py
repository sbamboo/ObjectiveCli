# python
import os,sys,subprocess

try:
    from libs.conUtils import *
    from libs.crshpiptools import *
    from libs.stringTags import *
    from assets import *
    from coloring import *
    from consoletools import *
    from core import *
    from dtypes import *
    from fonts import *
    from generators import *
    from imaging import *
    from linedraw import *
    from manip import *
    from objects import *
    from pointGroupAlgorithms import *
    from shapes import *
    from terminal import *
    from version import *
except:
    try:
        from .libs.conUtils import *
        from .libs.crshpiptools import *
        from .libs.stringTags import *
        from .assets import *
        from .coloring import *
        from .consoletools import *
        from .core import *
        from .dtypes import *
        from .fonts import *
        from .generators import *
        from .imaging import *
        from .linedraw import *
        from .manip import *
        from .objects import *
        from .pointGroupAlgorithms import *
        from .shapes import *
        from .terminal import *
        from .version import *
    except:
        try:
            from Drawlib2.libs.conUtils import *
            from Drawlib2.libs.crshpiptools import *
            from Drawlib2.libs.stringTags import *
            from Drawlib2.assets import *
            from Drawlib2.coloring import *
            from Drawlib2.consoletools import *
            from Drawlib2.core import *
            from Drawlib2.dtypes import *
            from Drawlib2.fonts import *
            from Drawlib2.generators import *
            from Drawlib2.imaging import *
            from Drawlib2.linedraw import *
            from Drawlib2.manip import *
            from Drawlib2.objects import *
            from Drawlib2.pointGroupAlgorithms import *
            from Drawlib2.shapes import *
            from Drawlib2.terminal import *
            from Drawlib2.version import *
        except:
            try:
                _parent = os.path.dirname(os.path.abspath(__file__))
                sys.path.append(os.path.abspath(os.path.join(_parent,"..")))
                from Drawlib2.libs.conUtils import *
                from Drawlib2.libs.crshpiptools import *
                from Drawlib2.libs.stringTags import *
                from Drawlib2.assets import *
                from Drawlib2.coloring import *
                from Drawlib2.consoletools import *
                from Drawlib2.core import *
                from Drawlib2.dtypes import *
                from Drawlib2.fonts import *
                from Drawlib2.generators import *
                from Drawlib2.imaging import *
                from Drawlib2.linedraw import *
                from Drawlib2.manip import *
                from Drawlib2.objects import *
                from Drawlib2.pointGroupAlgorithms import *
                from Drawlib2.shapes import *
                from Drawlib2.terminal import *
                from Drawlib2.version import *
            except:
                os.system("")
                print("\033[31mFailed to import drawlib, please make sure playground is either in an approriate folder relative to Drawlib.\033[0m")
                exit()

class RaisingDummyObject:
    '''LimitExec: Dummy object, raises.'''
    # Subscribable
    def __getitem__(self, key):
        raise NameError("Callable '"+key+"' Not found in restricted session.")
    # Callable
    def __call__(self, *args, **kwargs):
        raise NameError()
_print = print
_exit = exit
_str = str
_int = int
_list = list
_dict = dict
_set = set
_float = float
_tuple = tuple
_bool = bool
_range = range
_len = len
_max = max
_min = min
_round = round
_abs = abs
_ord = ord
_chr = chr
globals()['__builtins__'] = RaisingDummyObject()
globals()['__import__'] = RaisingDummyObject()
print = _print
exit = _exit
str = _str
int = _int
list = _list
dict = _dict
set = _set
float = _float
tuple = _tuple
bool = _bool
range = _range
len = _len
max = _max
min = _min
round = _round
abs = _abs
ord = _ord
chr = _chr

_loggbuff = False
_outputObj = None
_monitorProcess = None
_bufferedModes = ["Buffer","Hybrid"]
_logFile = os.path.join(os.path.dirname(os.path.realpath(__file__)),"_playground.tmp")
_monitorScript_1 = os.path.join(os.path.dirname(os.path.realpath(__file__)),"_playground_monitor.py")
_monitorScript_2 = os.path.join(os.path.dirname(os.path.realpath(__file__)),"Drawlib2","_playground_monitor.py")

if os.path.exists(_monitorScript_1):
    _monitorScript = _monitorScript_1
elif os.path.exists(_monitorScript_2):
    _monitorScript = _monitorScript_2
else:
    _monitorScript = None

def getCliHelp():
    print(f"\nUsage: {os.path.basename(sys.executable)} {os.path.basename(__file__)} [--autoMon] [--sizeMon] [--noAutoLink]")
    print("\nAutoMon:\n    Starts any monitor instance in auto mode, meaning it will not wait for input before drawing the buffer. (<outputObj>.clear() won't affect monitor)")
    print("SizeMon:\n    Starts any monitor instance with the size of the buffer.")
    print("NoAutoLink:\n    Won't automaticly link the DrawlibOut instance to its outputObj when the monitor is launched.")
    print("\nInfo:\n    Arguments can be applied even when CLI args aren't avaliable by using '__<argName> =True' when using launchMonitor().\n    Example: launchMonitor(<outputObj>,__sizeMon=True)")

_waitingMonitor = True
if "--autoMon" in sys.argv:
    _waitingMonitor = False
_sizeMonitor = False
if "--sizeMon" in sys.argv:
    _sizeMonitor = True
_nolinkOnMonLaunch = False
if "--noAutoLink" in sys.argv:
    _nolinkOnMonLaunch = True
if "--help" in sys.argv or "-h" in sys.argv or "--h" in sys.argv or "-help" in sys.argv:
    getCliHelp()
    exit()

_playground_internal_python_org_exit = exit
def _texit():
    global _monitorProcess
    if _monitorProcess != None:
        _monitorProcess.terminate()
        _monitorProcess = None
    if os.path.exists(_logFile): os.remove(_logFile)
    clear()
    _playground_internal_python_org_exit()
exit = _texit

def launchMonitor(out=object,__autoMon=None,__sizeMon=None,__noAutoLink=None):
    global _loggbuff,_outputObj,_monitorProcess
    if __autoMon != None and __autoMon == True:
        _i_waitingMonitor = False
    else:
        _i_waitingMonitor = _waitingMonitor
    _i_sizeMonitor = _sizeMonitor if __sizeMon == None else __sizeMon
    _i_nolinkOnMonLaunch = _nolinkOnMonLaunch if __noAutoLink == None else __noAutoLink
    if out.mode not in _bufferedModes:
        print(f"\033[31mCan't launch monitor for non-buffered output.\033[0m")
        return
    if _monitorScript == None:
        print(f"\033[31mCan't launch monitor, monitor script not found.\033[0m")
        return
    _loggbuff = True
    _outputObj = out
    if _i_nolinkOnMonLaunch == False:
        try:
            out._link()
        except: pass
    _sname = str(_outputObj).replace("<","@a").replace(">","@b").replace(" ","@s").replace("'","@q").replace('"','@d')
    _pargs = [sys.executable, _monitorScript, "-oname",_sname, "-wmon",str(_i_waitingMonitor), "-omode",str(_outputObj.mode)]
    if _outputObj.linked != None:
        _bsname = str(_outputObj.linked.buffer).replace("<","@a").replace(">","@b").replace(" ","@s").replace("'","@q").replace('"','@d')
        _pargs.extend(["-buffOname",_bsname])
    if _i_sizeMonitor == True:
        _width, _height = out.getsize()
        _pargs.extend(["-xdim",str(_width), "-ydim",str(_height)])
    _monitorProcess = subprocess.Popen(_pargs, creationflags=subprocess.CREATE_NEW_CONSOLE)

def fillMonitor(out=object,char=" "):
    global _outputObj
    if out == None:
        if _outputObj != None:
            print(f"\033[31mCan't fill non-launched monitor, use launchMonitor(<outputObj>) first.\033[0m")
            return
        else:
            try:
                _outputObj.linked.buffer.fill(char)
            except:
                print(f"\033[31mCan't fill without buffer on output, either its a non-buffered obj or it's not linked.\033[0m")
                return
    else:
        try:
            out.linked.buffer.fill(char)
        except:
            print(f"\033[31mCan't fill without buffer on output, either its a non-buffered obj or it's not linked.\033[0m")
            return

def killMonitor(*args,**kwargs):
    global _monitorProcess
    if _monitorProcess != None:
        _monitorProcess.terminate()
        _monitorProcess = None
    else:
        print(f"\033[31mCan't kill non-launched monitor, use launchMonitor(<outputObj>) first.\033[0m")
        return

width = os.get_terminal_size()[0]

x,y = 0,os.get_terminal_size()[1]
prefix = "Drawlib > "

setConTitle("Drawlib Playground! (v0)")
clear()

print("Welcome to drawlib playground!")
print("Press ENTER to contine and once inside write 'exit()' to exit.")
print("\033[3m\033[90mYou can use \033[23mlaunchMonitor(<outputObj>)\033[3m to view buffered outputs memory,")
print('and \033[23mfillMonitor(<outputObj>,<char=" ">)\033[3m to fill the buffer with a char,')
print('aswell as \033[23mkillMonitor(<optional:outputObj>)\033[3m to kill the monitor.\033[23m\033[0m')
print("-"*width)
try:
    if input("ENTER/stCmd > ") == "exit()": _texit()
except KeyboardInterrupt: _texit()
clear()

while True:
    reset_write_head()
    debug = False
    try:
        draw(x,y," "*width)
        _inp = inputAtPos(x,y,prefix)
        _t = _inp.split(":")
        _t.pop(-1)
        if len(_t) == 1: _t = _t[0] + ":"
        else:
            _t = ":".join(_t)
        if "deb:" in _t:
            debug = True
            _inp = _inp.replace("deb:","",1).strip()
        if "clr:" in _t:
            clear()
            _inp = _inp.replace("clr:","",1).strip()
        if "ins:" in _t:
            _inp = _inp.replace("ins:","",1).strip()
            _inp = "print(" + _inp + ")"
        if "inss:" in _t:
            _inp = _inp.replace("inss:","",1).strip()
            _inp = "print('" + _inp + "')"
        if "insd:" in _t:
            _inp = _inp.replace("insd:","",1).strip()
            _inp = 'print("' + _inp + '")'
    except KeyboardInterrupt: _texit()
    try: exec(_inp)
    except Exception as e:
        if debug == True:
            print(f"\033[31mInvalid input: '{_inp}'\033[0m\n{e}")
        else:
            print(f"\033[31mInvalid input: '{_inp}'\033[0m")
    if _loggbuff == True and _outputObj != None:
        if _outputObj.mode in _bufferedModes:
            if "launchMonitor(" in _inp and ";" not in _inp: pass
            else:
                if _outputObj.linked != None:
                    open(_logFile,'w').write( json.dumps( _outputObj.linked.buffer.buffer ) )