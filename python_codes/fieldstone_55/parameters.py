
import numpy as np

Lx=6000e3
Ly=3000e3
d=50e3
h=100e3
eta1=1e21
gamma=100.  #viscosity ratio
drho=100.
L=400e3
theta=60./180.*np.pi
rad=300e3

xL=Lx/2.
yL=Ly-d-h/2

xK=xL-L
yK=yL

xM=xL
yM=yL-rad

xN=xM+(rad-h/2)*np.cos(np.pi/2-theta)
yN=yM+(rad-h/2)*np.sin(np.pi/2-theta) 

xP=xM+(rad+h/2)*np.cos(np.pi/2-theta)
yP=yM+(rad+h/2)*np.sin(np.pi/2-theta) 

xQ=(xN+xP)/2.
yQ=(yN+yP)/2.


np_mid=281
np_perim=640
np_box=64
