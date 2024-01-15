import os,sys
parent = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(parent,"..","..")))

from ObjectiveCli.libs.packaged import Drawlib2 as drawlib

print(drawlib.version.getInfo())