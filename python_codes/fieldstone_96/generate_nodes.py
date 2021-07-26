import numpy as np
from parameters import *

#------------------------------------------------------------------------------

filename='mypoints'
nodesfile=open(filename,"w")

nodesfile.write("%5d %5d %3d %3d\n" %(2*nnt+2*nnr+np_blob+np_moho+np_trans+nnr*nnt,2,0,1))

counter=0
counter_segment=0

segmentfile=open("mysegments","w")

#------------------------------------------------------------------------------
# inner boundary counterclockwise
#------------------------------------------------------------------------------

for i in range (0,nnt):
    angle=np.pi/(nnt-1)*i-np.pi/2
    xi=R_inner*np.cos(angle)
    zi=R_inner*np.sin(angle)
    nodesfile.write("%5d %f %f %3d \n" %(counter+1,xi,zi, 1))
    counter+=1
    if i<nnt-1:
       counter_segment+=1
       segmentfile.write("%5d %5d %5d %5d \n" %(counter_segment,counter,counter+1,1))

#------------------------------------------------------------------------------
# left wall 
#------------------------------------------------------------------------------

for i in range (0,nnr):
    xi=0
    zi=R_inner+(R_outer-R_inner)/nnr*i
    nodesfile.write("%5d %f %f %3d \n" %(counter+1,xi,zi, 2))
    counter+=1
    if i<nnr-1:
       counter_segment+=1
       segmentfile.write("%5d %5d %5d %5d \n" %(counter_segment,counter,counter+1,2))

#------------------------------------------------------------------------------
# outer boundary clockwise
#------------------------------------------------------------------------------

for i in range (0,nnt):
    angle=np.pi/2-np.pi/nnt*i
    xi=R_outer*np.cos(angle)
    zi=R_outer*np.sin(angle)
    nodesfile.write("%5d %f %f %3d \n" %(counter+1,xi,zi, 3))
    counter+=1
    if i<nnt-1:
       counter_segment+=1
       segmentfile.write("%5d %5d %5d %5d \n" %(counter_segment,counter,counter+1,3))


#------------------------------------------------------------------------------
# bottom vertical wall
#------------------------------------------------------------------------------

for i in range (0,nnr):
    xi=0
    zi=-R_outer+(R_outer-R_inner)/nnr*i
    nodesfile.write("%5d %f %f %3d \n" %(counter+1,xi,zi, 4))
    counter+=1
    if i<nnr-1:
       counter_segment+=1
       segmentfile.write("%5d %5d %5d %5d \n" %(counter_segment,counter,counter+1,4))

#------------------------------------------------------------------------------
# blob 
#------------------------------------------------------------------------------

for i in range (0,np_blob):

    angle=-np.pi/2+np.pi/(np_blob-1)*i
    xi=R_blob*np.cos(angle)
    zi=z_blob+R_blob*np.sin(angle)
    nodesfile.write("%5d %f %f %3d \n" %(counter+1,xi,zi, 5))
    counter+=1
    if i<np_blob-1:
       counter_segment+=1
       segmentfile.write("%5d %5d %5d %5d \n" %(counter_segment,counter,counter+1,5))

#------------------------------------------------------------------------------
# moho 
#------------------------------------------------------------------------------

dtheta=np.pi/nnt
for i in range (0,np_moho):
    #angle=np.pi/2-np.pi/np_moho*i
    angle=np.pi/2-(i+0.5)*dtheta
    xi=R_moho*np.cos(angle)
    zi=R_moho*np.sin(angle)
    nodesfile.write("%5d %f %f %3d \n" %(counter+1,xi,zi, 3))
    counter+=1
    if i<np_moho-1:
       counter_segment+=1
       segmentfile.write("%5d %5d %5d %5d \n" %(counter_segment,counter,counter+1,3))

#------------------------------------------------------------------------------
# transition in the mantle 
#------------------------------------------------------------------------------

dtheta=np.pi/nnt
for i in range (0,np_trans):
    #angle=np.pi/2-np.pi/np_trans*i
    angle=np.pi/2-(i+0.5)*dtheta
    xi=R_trans*np.cos(angle)
    zi=R_trans*np.sin(angle)
    nodesfile.write("%5d %f %f %3d \n" %(counter+1,xi,zi, 3))
    counter+=1
    if i<np_trans-1:
       counter_segment+=1
       segmentfile.write("%5d %5d %5d %5d \n" %(counter_segment,counter,counter+1,3))

#------------------------------------------------------------------------------
# bulk nodes
#------------------------------------------------------------------------------

dr=(R_outer-R_inner)/nnr
dtheta=np.pi/nnt
for i in range(0,nnr):
    for j in range(0,nnt): 
        radius=R_inner+(i+0.5)*dr
        angle=np.pi/2-(j+0.5)*dtheta
        xi=radius*np.cos(angle)
        zi=radius*np.sin(angle)
        nodesfile.write("%5d %f %f %3d \n" %(counter+1,xi,zi, 3))

#------------------------------------------------------------------------------

nodesfile.write("%5d %3d \n" %(counter_segment,1))

segmentfile.write("%5d \n" %(1))
segmentfile.write("%5d %e %e \n" %(1,0.1,0.1))

