import os,time

from .core import vw,vh,ConsoleOutput,CellOpOutofBounds,base_mdraw
from .linedraw import draw_point,draw_line
from .coloring import TextObj,DrawlibStdPalette
from .libs.conUtils import getConSize,setConSize,clear,pause
from .pointGroupAlgorithms import beethams_line_algorithm

def draw_info(width,height,cw,ch,output,stripAnsi,draw_cross=True):
    if ch < 15 or cw < 56:
        msg = None
        _amsg = f"Console To Smal! Min:(X={width},Y={height})"
        if cw < 8:
            msg = "!"
        elif cw >= len(_amsg):
            msg = _amsg
        elif cw >= 18:
            msg = "Console To Small!"
        elif cw >= 8:
            msg = "To Small"
        clear()
        draw_point(msg,0,0,output,drawNc=True)
    else:
        # Ansi free
        if stripAnsi:
            clear()
            print(f"Console to small! Current:(X={cw},Y={ch}) Min:(X={width},Y={height}) Pls resize!")
        # Colored
        else:
            corner = TextObj("{f.darkyellow}{b.yellow}#{r}").retFormat()
            cross = "."
            note = TextObj("Console to smal:").retFormat()
            info = TextObj("Align {f.yellow}yellow{r} with console corners by resizing console.").retFormat()
            os.system("") # windows ansi fix
            #curW,curH = output.getsize()
            #curW -= 1
            #curH -= 1
            #output.fill(" ",xRange=[0,curW],yRange=[0,round(height/2)-1])
            #output.fill(" ",xRange=[0,curW],yRange=[round(height/2)+1,curH])
            #output.fill(" ",xRange=[len(info),curW],yRange=[round(height/2),round(height/2)])
            #output.fill(" ")
            clear()
            try:
                capW = min(cw,width)
                capH = min(ch,height)
                clamps = [[0,capW],[0,capH]]
                # draw info
                draw_point(note,0,round(height/2)-1, output,drawNc=True,supressDraw=True)
                draw_point(info,0,round(height/2), output,drawNc=True,supressDraw=True)
                # draw cross
                if draw_cross == True:
                    draw_line(cross, 2,2, width-2,height-1, output, clamps=clamps,drawNc=True,supressDraw=True)
                    draw_line(cross, 2,height-1, width-2,2, output, clamps=clamps,drawNc=True,supressDraw=True)
                # draw corners
                draw_line(corner, 0,0, 5,0, output, clamps=clamps,drawNc=True,supressDraw=True)
                draw_line(corner, 0,0, 0,2, output, clamps=clamps,drawNc=True,supressDraw=True)
                draw_line(corner, width-5,0, width,0, output, clamps=clamps,drawNc=True,supressDraw=True)
                draw_line(corner, width,0, width,2, output, clamps=clamps,drawNc=True,supressDraw=True)
                draw_line(corner, 0,height, 5,height, output, clamps=clamps,drawNc=True,supressDraw=True)
                draw_line(corner, 0,height, 0,height-2, output, clamps=clamps,drawNc=True,supressDraw=True)
                draw_line(corner, width-5,height, width,height, output, clamps=clamps,drawNc=True,supressDraw=True)
                draw_line(corner, width,height, width,height-2, output, clamps=clamps,drawNc=True,supressDraw=True)
                # draw info
                draw_point(note,0,round(height/2)-1, output,drawNc=True,supressDraw=True)
                draw_point(info,0,round(height/2), output,drawNc=True,supressDraw=True)
            except CellOpOutofBounds: pass
            output.draw()

def sizeAssist(width=int,height=int,output=object,stripAnsi=False,updateDelaySec=0.1):
    try:
        if output.linked.buffer.buffer == None:
            output.linked.buffer.create()
    except: pass
    while getConSize()[0] < width or getConSize()[1] < height:
        cw,ch = getConSize()
        try:
            draw_info(width,height,cw,ch,output,stripAnsi)
        except KeyboardInterrupt:
            break
        # Slow down refresh rate
        try:
            if isinstance(output.linked, ConsoleOutput):
                output.linked.conSize = getConSize()
            else:
                output.linked.buffer.bufferSize = getConSize()
                output.linked.buffer.clear()
        except: pass
        time.sleep(updateDelaySec)
    cw,ch = getConSize()
    if stripAnsi == False:
        draw_info(width,height,cw,ch,output,stripAnsi,draw_cross=False)
        draw_point("Console resized correctly!                             ",0,round(height/2)-1, output,drawNc=True)
        draw_point("Press any key to continue...                           ",0,round(height/2), output,drawNc=True)
    else:
        print("Console resized correctly!")
        print("Press any key to continue...")
    pause()
    clear()