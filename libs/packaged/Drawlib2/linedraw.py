from .core import base_draw,base_fill,base_mdraw
from .coloring import DrawlibStdPalette
from .pointGroupAlgorithms import *
from .tools import capIntsX,capIntsY,resolveClamps,clamp,clampM,clampS,check_clamp,check_clampM,check_clampS,filter_clampM

def move_write_head(x=int,y=int):
    line = "\033[{};{}H".format(x,y)
    print(line)

def fill_terminal(st=str, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False,supressDraw=False):
    base_fill(st,output,baseColor,palette,drawNc,supressDraw=supressDraw)

def draw_point(st=str,x=int,y=int, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False,supressDraw=False,clamps=None,excludeClamped=True):
    if excludeClamped == True:
        if check_clampS(x,y,c=clamps) == False:
            return
    x,y = clampS(x,y,c=clamps)
    base_draw(st,x,y,output,baseColor,palette,drawNc,supressDraw=supressDraw)

def draw_line(st=str,x1=int,y1=int,x2=int,y2=int, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False,supressDraw=False,clamps=None,excludeClamped=True):
    if excludeClamped == False and excludeClamped != "SKIPinclClamp":
        x1,y1,x2,y2 = clampS(x1,y1,x2,y2,c=clamps)
    coords = beethams_line_algorithm(x1,y1,x2,y2)
    if excludeClamped == True:
        coords = filter_clampM(coords,clamps)
    base_mdraw(st,coords,output,baseColor,palette,drawNc,supressDraw=supressDraw)

def draw_triangle_sides(st,s1,s2,s3, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False,supressDraw=False,clamps=None,excludeClamped=True):
    if excludeClamped == False:
        s1,s2,s3 = clampM([s1,s2,s3],clamps)
        clampType = "SKIPinclClamp"
    else:
        clampType = True
    draw_line(st,*s1[0],*s1[1], output,baseColor,palette,drawNc,supressDraw=supressDraw,clamps=clamps,excludeClamped=clampType)
    draw_line(st,*s2[0],*s2[1], output,baseColor,palette,drawNc,supressDraw=supressDraw,clamps=clamps,excludeClamped=clampType)
    draw_line(st,*s3[0],*s3[1], output,baseColor,palette,drawNc,supressDraw=supressDraw,clamps=clamps,excludeClamped=clampType)
def draw_triangle_points(st,p1,p2,p3, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False,supressDraw=False,clamps=None,excludeClamped=True):
    if excludeClamped == False:
        p1,p2,p3 = clampM([p1,p2,p3],clamps)
        clampType = "SKIPinclClamp"
    else:
        clampType = True
    draw_line(st,*p1,*p2, output,baseColor,palette,drawNc,supressDraw=supressDraw,clamps=clamps,excludeClamped=clampType)
    draw_line(st,*p1,*p3, output,baseColor,palette,drawNc,supressDraw=supressDraw,clamps=clamps,excludeClamped=clampType)
    draw_line(st,*p2,*p3, output,baseColor,palette,drawNc,supressDraw=supressDraw,clamps=clamps,excludeClamped=clampType)
def draw_triangle_coords(st,x1,y1,x2,y2,x3,y3, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False,supressDraw=False,clamps=None,excludeClamped=True):
    if excludeClamped == False:
        x1,y1,x2,y2,x3,y3 = clampS(x1,y1,x2,y2,x3,y3,c=clamps)
        clampType = "SKIPinclClamp"
    else:
        clampType = True
    p1 = [x1,y1]
    p2 = [x2,y2]
    p3 = [x3,y3]
    draw_line(st,*p1,*p2, output,baseColor,palette,drawNc,supressDraw=supressDraw,clamps=clamps,excludeClamped=clampType)
    draw_line(st,*p1,*p3, output,baseColor,palette,drawNc,supressDraw=supressDraw,clamps=clamps,excludeClamped=clampType)
    draw_line(st,*p2,*p3, output,baseColor,palette,drawNc,supressDraw=supressDraw,clamps=clamps,excludeClamped=clampType)

def draw_circle(st=str,xM=int,yM=int,r=int, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False,supressDraw=False,clamps=None,excludeClamped=True):
    rigX = xM+r
    lefX = xM-r
    topY = yM+r
    botY = yM-r
    rigX,lefX,topY,botY = clampS(rigX,lefX,topY,botY,c=clamps)
    diam = (r*2)+1
    # CapValues
    capIntsX([xM,rigX,lefX])
    capIntsY([yM,topY,botY])
    # Calculate Coordinates
    coords = beethams_circle_algorithm(xM,yM,r)
    if excludeClamped == True:
        coords = filter_clampM(coords,clamps)
    else:
        coords = clampM(coords,clamps)
    # Draw coordinates
    base_mdraw(st,coords,output,baseColor,palette,drawNc,supressDraw=supressDraw)

def draw_ellipse(char=str,cX=int,cY=int,xRad=int,yRad=int, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False,supressDraw=False,clamps=None,excludeClamped=True):
    rigX = cX+xRad
    lefX = cX-xRad
    topY = cY+yRad
    botY = cY-yRad
    rigX,lefX,topY,botY = clampS(rigX,lefX,topY,botY,c=clamps)
    # CapValues
    capIntsX([cX,rigX,lefX])
    capIntsY([cY,topY,botY])
    # Calculate Coordinates
    coords = beethams_ellipse_algorithm(cX,cY,xRad,yRad)
    if excludeClamped == True:
        coords = filter_clampM(coords,clamps)
    else:
        coords = clampM(coords,clamps)
    # Draw coordinates
    base_mdraw(st,coords,output,baseColor,palette,drawNc,supressDraw=supressDraw)

def draw_quadBezier(char,sX=int,sY=int,cX=int,cY=int,eX=int,eY=int, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False,supressDraw=False,clamps=None,excludeClamped=True):
    sX,sY,cX,cY,eX,eY = clampS(sX,sY,cX,cY,eX,eY,c=clamps)
    # CapValues
    capIntsX([sX,cX,eX])
    capIntsY([sY,cY,eY])
    # Calculate Coordinates
    coords = generate_quadratic_bezier(sX,sY,cX,cY,eX,eY)
    if excludeClamped == True:
        coords = filter_clampM(coords,clamps)
    else:
        coords = clampM(coords,clamps)
    # Draw coordinates
    base_mdraw(st,coords,output,baseColor,palette,drawNc,supressDraw=supressDraw)

def draw_cubicBezier(char,sX=int,sY=int,c1X=int,c1Y=int,c2X=int,c2Y=int,eX=int,eY=int, algorithm="step",modifier=None, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False,supressDraw=False,clamps=None,excludeClamped=True):
    '''
    Alogrithm: "step" or "point"
    Modifier: With step algorithm, def: 0.01; With point algorithm, def: 100
    '''
    sX,sY,c1X,c1Y,c2X,c2Y,eX,eY = clampS(sX,sY,c1X,c1Y,c2X,c2Y,eX,eY,c=clamps)
    # CapValues
    capIntsX([sX,c1X,c2X,eX])
    capIntsY([sY,c1Y,c2Y,eY])
    # Calculate Coordinates
    coords = generate_cubic_bezier(sX, sY, c1X, c1Y, c2X, c2Y, eX, eY, algorithm,modifier)
    if excludeClamped == True:
        coords = filter_clampM(coords,clamps)
    else:
        coords = clampM(coords,clamps)
    # Draw coordinates
    base_mdraw(st,coords,output,baseColor,palette,drawNc,supressDraw=supressDraw)