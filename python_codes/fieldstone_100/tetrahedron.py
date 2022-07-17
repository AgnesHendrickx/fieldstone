import numpy as np
from numpy import linalg as LA
import numba
from numba import jit

xx=0
yy=1
zz=2

Ggrav=6.6743e-11

# np.cross not supported by numba at the time of writing
# so I replaced it by my function

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
@jit(nopython=True)
def my_cross(u,v):
    w=np.zeros(3,dtype=np.float64)
    w[0]=u[1]*v[2]-u[2]*v[1]
    w[1]=u[2]*v[0]-u[0]*v[2]
    w[2]=u[0]*v[1]-u[1]*v[0]
    return w

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

@jit(nopython=True)
def compute_face_edge_normal(vec_nface,pt_start,pt_end,pt_midface,name):
    #pt_start,pt_end are the vertices making the edge
    pt_mid=0.5*(pt_start+pt_end)
    vec_l=pt_end-pt_start
    #vec_n=np.empty(3)
    #det=vec_nface[yy]*vec_l[zz]-vec_nface[zz]*vec_l[yy]
    #vec_n[xx]=1
    #vec_n[yy]=(-vec_l[zz]*vec_nface[xx]+vec_nface[zz]*vec_l[xx] )/det
    #vec_n[zz]=(+vec_l[yy]*vec_nface[xx]-vec_nface[yy]*vec_l[xx] )/det
    vec_n=my_cross(vec_nface,vec_l) 
    
    vec_n/=LA.norm(vec_n,2)
    #print('in',np.dot(vec_n,vec_nface))
    #print('in',np.dot(vec_n,vec_l))
    vec_n*=np.sign(np.dot(vec_n,pt_mid-pt_midface))
    #export_vector_to_vtu(pt_mid,vec_n,name)
    return vec_n

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

@jit(nopython=True)
def compute_gravity_at_point_th(pt_1,pt_2,pt_3,pt_4,pt_M,rho0):
    # pt1,2,3,4,M: arrays containing x,y,z coordinates

    #---step1---
    # order 12 or 21 does not matter much:
    # these are used to compute the normal to faces.
    # and later only the norm is used.

    vec_l1=np.zeros(3,dtype=np.float64)
    vec_l2=np.zeros(3,dtype=np.float64)
    vec_l3=np.zeros(3,dtype=np.float64)
    vec_l4=np.zeros(3,dtype=np.float64)
    vec_l5=np.zeros(3,dtype=np.float64)
    vec_l6=np.zeros(3,dtype=np.float64)

    vec_l1 = pt_2-pt_1
    vec_l2 = pt_3-pt_1
    vec_l3 = pt_4-pt_1
    vec_l4 = pt_3-pt_2
    vec_l5 = pt_4-pt_2
    vec_l6 = pt_4-pt_3

    l1 = LA.norm(vec_l1,2)
    l2 = LA.norm(vec_l2,2)
    l3 = LA.norm(vec_l3,2)
    l4 = LA.norm(vec_l4,2)
    l5 = LA.norm(vec_l5,2)
    l6 = LA.norm(vec_l6,2)

    #---step2------------------------------------------------------------------

    vec_r1=np.zeros(3,dtype=np.float64)
    vec_r2=np.zeros(3,dtype=np.float64)
    vec_r3=np.zeros(3,dtype=np.float64)
    vec_r4=np.zeros(3,dtype=np.float64)

    vec_r1 = pt_1-pt_M 
    vec_r2 = pt_2-pt_M 
    vec_r3 = pt_3-pt_M 
    vec_r4 = pt_4-pt_M 

    #export_vector_to_vtu(pt_M,vec_r1,'vec_r1')
    #export_vector_to_vtu(pt_M,vec_r2,'vec_r2')
    #export_vector_to_vtu(pt_M,vec_r3,'vec_r3')
    #export_vector_to_vtu(pt_M,vec_r4,'vec_r4')

    r1=LA.norm(vec_r1,2)
    r2=LA.norm(vec_r2,2)
    r3=LA.norm(vec_r3,2)
    r4=LA.norm(vec_r4,2)
 
    #---step3---compute normal vectors to faces

    pt_midA=np.zeros(3,dtype=np.float64)
    pt_midB=np.zeros(3,dtype=np.float64)
    pt_midC=np.zeros(3,dtype=np.float64)
    pt_midD=np.zeros(3,dtype=np.float64)

    pt_midA = (pt_1+pt_2+pt_3)/3
    pt_midB = (pt_1+pt_3+pt_4)/3
    pt_midC = (pt_1+pt_4+pt_2)/3 
    pt_midD = (pt_2+pt_4+pt_3)/3

    vec_nA=np.zeros(3,dtype=np.float64)
    vec_nB=np.zeros(3,dtype=np.float64)
    vec_nC=np.zeros(3,dtype=np.float64)
    vec_nD=np.zeros(3,dtype=np.float64)

    #vec_nA = np.cross(vec_l1,vec_l2)
    #vec_nB = np.cross(vec_l2,vec_l3)
    #vec_nC = np.cross(vec_l3,vec_l1)
    #vec_nD = np.cross(vec_l5,vec_l4)

    vec_nA = my_cross(vec_l1,vec_l2)
    vec_nB = my_cross(vec_l2,vec_l3)
    vec_nC = my_cross(vec_l3,vec_l1)
    vec_nD = my_cross(vec_l5,vec_l4)

    vec_nA /=LA.norm(vec_nA,2)
    vec_nB /=LA.norm(vec_nB,2)
    vec_nC /=LA.norm(vec_nC,2)
    vec_nD /=LA.norm(vec_nD,2)

    #export_vector_to_vtu(pt_midA,vec_nA,'faceA_normal')
    #export_vector_to_vtu(pt_midB,vec_nB,'faceB_normal')
    #export_vector_to_vtu(pt_midC,vec_nC,'faceC_normal')
    #export_vector_to_vtu(pt_midD,vec_nD,'faceD_normal')

    #---step4------------------------------------------------------------------

    mat_FA=np.zeros((3,3),dtype=np.float64)
    mat_FB=np.zeros((3,3),dtype=np.float64)
    mat_FC=np.zeros((3,3),dtype=np.float64)
    mat_FD=np.zeros((3,3),dtype=np.float64)

    mat_FA = np.outer(vec_nA,vec_nA)
    mat_FB = np.outer(vec_nB,vec_nB)
    mat_FC = np.outer(vec_nC,vec_nC)
    mat_FD = np.outer(vec_nD,vec_nD)

    #---step5---solid angles---------------------------------------------------

    num=np.dot(vec_r1,my_cross(vec_r2,vec_r3))
    denom=(r1*r2*r3+\
          r1*np.dot(vec_r2,vec_r3)+\
          r2*np.dot(vec_r3,vec_r1)+\
          r3*np.dot(vec_r1,vec_r2))
    wA = 2*np.arctan2(num,denom)

    num= np.dot(vec_r1,my_cross(vec_r3,vec_r4))
    denom=(r1*r3*r4+\
          r1*np.dot(vec_r3,vec_r4)+\
          r3*np.dot(vec_r4,vec_r1)+\
          r4*np.dot(vec_r1,vec_r3))
    wB = 2*np.arctan2(num,denom)

    num= np.dot(vec_r1,my_cross(vec_r4,vec_r2))
    denom=(r1*r4*r2+\
           r1*np.dot(vec_r4,vec_r2)+\
           r4*np.dot(vec_r2,vec_r1)+\
           r2*np.dot(vec_r1,vec_r4))
    wC=2*np.arctan2(num,denom)

    num=np.dot(vec_r2,my_cross(vec_r4,vec_r3))
    denom=(r2*r4*r3+
           r2*np.dot(vec_r4,vec_r3)+
           r4*np.dot(vec_r3,vec_r2)+
           r3*np.dot(vec_r2,vec_r4))
    wD=2*np.arctan2(num,denom)

    #---step6------------------------------------------------------------------

    vec_rA = pt_midA-pt_M
    vec_rB = pt_midB-pt_M
    vec_rC = pt_midC-pt_M 
    vec_rD = pt_midD-pt_M

    #export_vector_to_vtu(pt_M,vec_rA,'vec_rA')
    #export_vector_to_vtu(pt_M,vec_rB,'vec_rB')
    #export_vector_to_vtu(pt_M,vec_rC,'vec_rC')
    #export_vector_to_vtu(pt_M,vec_rD,'vec_rD')

    #---step7------------------------------------------------------------------

    vec_gf=np.zeros(3,dtype=np.float64)

    vec_gf=wA*np.dot(mat_FA,vec_rA) +\
           wB*np.dot(mat_FB,vec_rB) +\
           wC*np.dot(mat_FC,vec_rC) +\
           wD*np.dot(mat_FD,vec_rD) 
    vec_gf*=Ggrav*rho0

    #---step 8-----------------------------------------------------------------

    vec_nA12=np.zeros(3,dtype=np.float64)
    vec_nA23=np.zeros(3,dtype=np.float64)
    vec_nA13=np.zeros(3,dtype=np.float64)

    vec_nB13=np.zeros(3,dtype=np.float64)
    vec_nB34=np.zeros(3,dtype=np.float64)
    vec_nB14=np.zeros(3,dtype=np.float64)

    vec_nC14=np.zeros(3,dtype=np.float64)
    vec_nC24=np.zeros(3,dtype=np.float64)
    vec_nC12=np.zeros(3,dtype=np.float64)

    vec_nD24=np.zeros(3,dtype=np.float64)
    vec_nD34=np.zeros(3,dtype=np.float64)
    vec_nD23=np.zeros(3,dtype=np.float64)

    vec_nA12 = compute_face_edge_normal(vec_nA,pt_1,pt_2,pt_midA,'faceA_n12')
    vec_nA23 = compute_face_edge_normal(vec_nA,pt_2,pt_3,pt_midA,'faceA_n23')
    vec_nA13 = compute_face_edge_normal(vec_nA,pt_3,pt_1,pt_midA,'faceA_n31')

    vec_nB13 = compute_face_edge_normal(vec_nB,pt_1,pt_3,pt_midB,'faceB_n13')
    vec_nB34 = compute_face_edge_normal(vec_nB,pt_3,pt_4,pt_midB,'faceB_n34')
    vec_nB14 = compute_face_edge_normal(vec_nB,pt_4,pt_1,pt_midB,'faceB_n41')

    vec_nC14 = compute_face_edge_normal(vec_nC,pt_1,pt_4,pt_midC,'faceC_n14')
    vec_nC24 = compute_face_edge_normal(vec_nC,pt_4,pt_2,pt_midC,'faceC_n42')
    vec_nC12 = compute_face_edge_normal(vec_nC,pt_2,pt_1,pt_midC,'faceC_n21')

    vec_nD24 = compute_face_edge_normal(vec_nD,pt_2,pt_4,pt_midD,'faceD_n24')
    vec_nD34 = compute_face_edge_normal(vec_nD,pt_4,pt_3,pt_midD,'faceD_n43')
    vec_nD23 = compute_face_edge_normal(vec_nD,pt_3,pt_2,pt_midD,'faceD_n32')

    #---step 9-----------------------------------------------------------------
    # one can check these matrices are indeed symmetric as 
    # explained in section 2.1.8

    mat_E12=np.zeros((3,3),dtype=np.float64)
    mat_E13=np.zeros((3,3),dtype=np.float64)
    mat_E14=np.zeros((3,3),dtype=np.float64)
    mat_E23=np.zeros((3,3),dtype=np.float64)
    mat_E24=np.zeros((3,3),dtype=np.float64)
    mat_E34=np.zeros((3,3),dtype=np.float64)

    mat_E12=np.outer(vec_nA,vec_nA12)+np.outer(vec_nC,vec_nC12) #edge 12(1) belongs to A & C
    mat_E13=np.outer(vec_nA,vec_nA13)+np.outer(vec_nB,vec_nB13) #edge 13(2) belongs to A & B
    mat_E14=np.outer(vec_nB,vec_nB14)+np.outer(vec_nC,vec_nC14) #edge 14(3) belongs to B & C
    mat_E23=np.outer(vec_nA,vec_nA23)+np.outer(vec_nD,vec_nD23) #edge 23(4) belongs to A & D
    mat_E24=np.outer(vec_nC,vec_nC24)+np.outer(vec_nD,vec_nD24) #edge 24(5) belongs to C & D
    mat_E34=np.outer(vec_nB,vec_nB34)+np.outer(vec_nD,vec_nD34) #edge 34(6) belongs to B & D

    #---step 10---potential of each edge---------------------------------------

    L12=np.log((r1+r2+l1)/(r1+r2-l1))
    L13=np.log((r1+r3+l2)/(r1+r3-l2))
    L14=np.log((r1+r4+l3)/(r1+r4-l3))
    L23=np.log((r2+r3+l4)/(r2+r3-l4))
    L24=np.log((r2+r4+l5)/(r2+r4-l5))
    L34=np.log((r3+r4+l6)/(r3+r4-l6))

    if np.abs(r1+r2-l1)/l1<1e-10:
       L12=0
    if np.abs(r1+r3-l2)/l2<1e-10:
       L13=0
    if np.abs(r1+r4-l3)/l3<1e-10:
       L14=0
    if np.abs(r2+r3-l4)/l4<1e-10:
       L23=0
    if np.abs(r2+r4-l5)/l5<1e-10:
       L24=0
    if np.abs(r3+r4-l6)/l6<1e-10:
       L34=0

    #---step 11---vector from M to any point on edge---------------------------
    # we choose the middle of the edge

    vec_r12=np.zeros(3,dtype=np.float64)
    vec_r13=np.zeros(3,dtype=np.float64)
    vec_r14=np.zeros(3,dtype=np.float64)
    vec_r23=np.zeros(3,dtype=np.float64)
    vec_r24=np.zeros(3,dtype=np.float64)
    vec_r34=np.zeros(3,dtype=np.float64)

    vec_r12 = 0.5*(pt_1+pt_2)-pt_M
    vec_r13 = 0.5*(pt_1+pt_3)-pt_M
    vec_r14 = 0.5*(pt_1+pt_4)-pt_M
    vec_r23 = 0.5*(pt_2+pt_3)-pt_M
    vec_r24 = 0.5*(pt_2+pt_4)-pt_M
    vec_r34 = 0.5*(pt_3+pt_4)-pt_M

    #export_vector_to_vtu(pt_M,vec_r12,'vec_r12')
    #export_vector_to_vtu(pt_M,vec_r13,'vec_r13')
    #export_vector_to_vtu(pt_M,vec_r14,'vec_r14')
    #export_vector_to_vtu(pt_M,vec_r23,'vec_r23')
    #export_vector_to_vtu(pt_M,vec_r24,'vec_r24')
    #export_vector_to_vtu(pt_M,vec_r34,'vec_r34')

    #---step 12----------------------------------------------------------------

    vec_ge=np.zeros(3,dtype=np.float64)

    vec_ge=L12*np.dot(mat_E12,vec_r12)+\
           L13*np.dot(mat_E13,vec_r13)+\
           L14*np.dot(mat_E14,vec_r14)+\
           L23*np.dot(mat_E23,vec_r23)+\
           L24*np.dot(mat_E24,vec_r24)+\
           L34*np.dot(mat_E34,vec_r34) 
    vec_ge*=Ggrav*rho0

    #---step 13----------------------------------------------------------------

    U_e=L12*np.dot(vec_r12,np.dot(mat_E12,vec_r12))+\
        L13*np.dot(vec_r13,np.dot(mat_E13,vec_r13))+\
        L14*np.dot(vec_r14,np.dot(mat_E14,vec_r14))+\
        L23*np.dot(vec_r23,np.dot(mat_E23,vec_r23))+\
        L24*np.dot(vec_r24,np.dot(mat_E24,vec_r24))+\
        L34*np.dot(vec_r34,np.dot(mat_E34,vec_r34)) 
    U_e*=0.5*Ggrav*rho0

    U_f=wA*np.dot(vec_rA,np.dot(mat_FA,vec_rA))+ \
        wB*np.dot(vec_rB,np.dot(mat_FB,vec_rB))+ \
        wC*np.dot(vec_rC,np.dot(mat_FC,vec_rC))+ \
        wD*np.dot(vec_rD,np.dot(mat_FD,vec_rD))
    U_f*=0.5*Ggrav*rho0

    U=U_e-U_f

    vec_g =-vec_ge+vec_gf

    #print('vec_ge',vec_ge[xx],vec_ge[yy],vec_ge[zz])
    #print('vec_gf',vec_gf[xx],vec_gf[yy],vec_gf[zz])
    #print('U_e',U_e)
    #print('U_f',U_f)
    #print('U  ',U)

    return vec_g,U

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

def export_tetrahedron_to_vtu(pt_1,pt_2,pt_3,pt_4,name):
    vtufile=open(name+'.vtu',"w")
    vtufile.write("<VTKFile type='UnstructuredGrid' version='0.1' byte_order='BigEndian'> \n")
    vtufile.write("<UnstructuredGrid> \n")
    vtufile.write("<Piece NumberOfPoints=' %5d ' NumberOfCells=' %5d '> \n" %(4,1))
    vtufile.write("<Points> \n")
    vtufile.write("<DataArray type='Float32' NumberOfComponents='3' Format='ascii'> \n")
    vtufile.write("%10e %10e %10e \n" %(pt_1[0],pt_1[1],pt_1[2]))
    vtufile.write("%10e %10e %10e \n" %(pt_2[0],pt_2[1],pt_2[2]))
    vtufile.write("%10e %10e %10e \n" %(pt_3[0],pt_3[1],pt_3[2]))
    vtufile.write("%10e %10e %10e \n" %(pt_4[0],pt_4[1],pt_4[2]))
    vtufile.write("</DataArray>\n")
    vtufile.write("</Points> \n")
    vtufile.write("<Cells>\n")
    vtufile.write("<DataArray type='Int32' Name='connectivity' Format='ascii'> \n")
    vtufile.write("%d %d %d %d\n" %(0,1,2,3))
    vtufile.write("</DataArray>\n")
    vtufile.write("<DataArray type='Int32' Name='offsets' Format='ascii'> \n")
    vtufile.write("%d \n" %(4))
    vtufile.write("</DataArray>\n")
    vtufile.write("<DataArray type='Int32' Name='types' Format='ascii'>\n")
    vtufile.write("%d \n" %10)
    vtufile.write("</DataArray>\n")
    vtufile.write("</Cells>\n")
    vtufile.write("</Piece>\n")
    vtufile.write("</UnstructuredGrid>\n")
    vtufile.write("</VTKFile>\n")
    vtufile.close()

#------------------------------------------------------------------------------

def export_hexahedron_to_vtu(pt_1,pt_2,pt_3,pt_4,pt_5,pt_6,pt_7,pt_8,name):
    vtufile=open(name+'.vtu',"w")
    vtufile.write("<VTKFile type='UnstructuredGrid' version='0.1' byte_order='BigEndian'> \n")
    vtufile.write("<UnstructuredGrid> \n")
    vtufile.write("<Piece NumberOfPoints=' %5d ' NumberOfCells=' %5d '> \n" %(8,1))
    vtufile.write("<Points> \n")
    vtufile.write("<DataArray type='Float32' NumberOfComponents='3' Format='ascii'> \n")
    vtufile.write("%10e %10e %10e \n" %(pt_1[0],pt_1[1],pt_1[2]))
    vtufile.write("%10e %10e %10e \n" %(pt_2[0],pt_2[1],pt_2[2]))
    vtufile.write("%10e %10e %10e \n" %(pt_3[0],pt_3[1],pt_3[2]))
    vtufile.write("%10e %10e %10e \n" %(pt_4[0],pt_4[1],pt_4[2]))
    vtufile.write("%10e %10e %10e \n" %(pt_5[0],pt_5[1],pt_5[2]))
    vtufile.write("%10e %10e %10e \n" %(pt_6[0],pt_6[1],pt_6[2]))
    vtufile.write("%10e %10e %10e \n" %(pt_7[0],pt_7[1],pt_7[2]))
    vtufile.write("%10e %10e %10e \n" %(pt_8[0],pt_8[1],pt_8[2]))
    vtufile.write("</DataArray>\n")
    vtufile.write("</Points> \n")
    vtufile.write("<Cells>\n")
    vtufile.write("<DataArray type='Int32' Name='connectivity' Format='ascii'> \n")
    vtufile.write("%d %d %d %d %d %d %d %d\n" %(0,1,2,3,4,5,6,7))
    vtufile.write("</DataArray>\n")
    vtufile.write("<DataArray type='Int32' Name='offsets' Format='ascii'> \n")
    vtufile.write("%d \n" %(8))
    vtufile.write("</DataArray>\n")
    vtufile.write("<DataArray type='Int32' Name='types' Format='ascii'>\n")
    vtufile.write("%d \n" %12)
    vtufile.write("</DataArray>\n")
    vtufile.write("</Cells>\n")
    vtufile.write("</Piece>\n")
    vtufile.write("</UnstructuredGrid>\n")
    vtufile.write("</VTKFile>\n")
    vtufile.close()





