import os,json,argparse

from libs.conUtils import clear,pause,setConTitle,setConSize
from terminal import draw

parser = argparse.ArgumentParser(description='Playground monitor')
parser.add_argument('-oname',type=str,help="Name of outputObj")
parser.add_argument('-omode',type=str,help="Mode of outputObj")
parser.add_argument('-wmon',type=str,help="Takes 'True' or 'False' if monitor should wait for inp.")
parser.add_argument('-xdim',type=str,help="Width of monitor window.")
parser.add_argument('-ydim',type=str,help="Height of monitor window.")
parser.add_argument('-buffOname',type=str,help="Name of the outputObj's buffer object.")
args = parser.parse_args()

_waiting = args.wmon == "True"
_sized = False
if args.xdim != None and args.ydim != None:
    setConSize(int(args.xdim),int(args.ydim))
    _sized = True

_uname = args.oname.replace("@a","^<").replace("@b","^>").replace("@s"," ").replace("@q","'").replace("@d",'"')
_title = "Drawlib Playground ^| Buffer Monitor"
if _uname != "": _title += f" for {_uname}"
if args.omode != "" and args.omode != None: _title += f' (mode="{args.omode}")'
if _waiting and not _sized: _title += " ^| waiting:True"
elif _waiting and _sized:  _title += f" ^| waiting:True, sized:{args.xdim}x{args.ydim}"
elif not _waiting and _sized: _title += f" ^| sized:{args.xdim}x{args.ydim}"
setConTitle(_title+" ^| q=CTRL+C")

_logFile = os.path.join(os.path.dirname(os.path.realpath(__file__)),"_playground.tmp")

_hasRecivedFirstInput = False

os.system("")

_pspec_uname_str = _uname.replace("^<","").replace("^>","").split(" object at ")
_pspec_uname_str = "\n    Type: "+_pspec_uname_str[0]+"\n    Addr: "+_pspec_uname_str[1]
if args.buffOname != "" and args.buffOname != None:
    _buffOname = args.buffOname.replace("@a","<").replace("@b",">").replace("@s"," ").replace("@q","'").replace("@d",'"')
    _pspec_uname_str += "\n    BufferObj: "+_buffOname

_conSize = os.get_terminal_size()

print("Waiting for playground to output buffer content...")
print("When the first command is executed in playground you will get a live view of the buffer here, press Ctrl+C to exit.")
print("-"*os.get_terminal_size()[0])
print(f"  MonitorMode: Waiting" if _waiting else "  MonitorMode: Auto")
print(f"  ShowingObj: {_pspec_uname_str}" if _uname != "" else "  ShowingObj: <Unknown>")
print(f"  Mode: {args.omode}" if args.omode != "" and args.omode != None else "  Mode: <Unknown>")
print(f"  Size: {args.xdim}x{args.ydim}" if args.xdim != None and args.ydim != None else "  Size: <UnSpecified>")
print("-"*_conSize[0])

while True:
    try:
        if os.path.exists(_logFile):
            if _hasRecivedFirstInput == False:
                clear()
                _hasRecivedFirstInput = True
            if _waiting: clear()
            data = json.loads(open(_logFile,'r').read())
            for line in data:
                yi = line
                line = data[str(line)]
                for cell in line:
                    xi = cell
                    cell = line[str(cell)]
                    if int(xi) <= _conSize[0] and int(yi) <= _conSize[1]:
                        draw(xi,yi,cell)
            if _waiting: os.remove(_logFile)
    except KeyboardInterrupt:
        try:
            if os.path.exists(_logFile): os.remove(_logFile)
        except: pass
    except PermissionError: pass
    except Exception as e:
        if "Expecting value" not in str(e):
            print("Ex: "+str(e))
            pause()