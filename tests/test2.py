import os,sys
parent = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(parent,"..","..")))

from ObjectiveCli.baseTypes import Window,wcCanvas

window = Window()
canvas = wcCanvas()
window.bind(wcCanvas)

pointChar = canvas.drawlib.coloring.TextObj("{f.red}█{r}").retFormat()
fillChar  = canvas.drawlib.coloring.TextObj("{f.blue}░{r}").retFormat()

graph = canvas.create_graph("f(x)=(0.5*x)^3",debug=True,xRange=(-10,10),yRange=(-10,10),xFactor=2,assumptionFill=True,pointChar=pointChar,fillChar=fillChar)

canvas.drawObj(graph)

window.term_pause()