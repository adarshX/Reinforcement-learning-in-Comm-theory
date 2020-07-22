import cmath
import numpy as np
import pdb
from trig_utility import *

def cellular_pattern_generator(isd, tier, no_cells, no_bdryvrtx):    

    ## Tier-1 clustering
    xd = [] 
    yd = []
    zd = []
    theta1 = np.pi/3 # fixed quantity for hexagonal pattern

    bs_loc = []
    bs_loc.append(0)

    for i in range(6): 
        [x, y] = pol2cart((i+1)*theta1, isd)
        xd.append(np.round(x))
        yd.append(np.round(y))
        zd.append(np.round(x) + 1j* np.round(y))
        bs_loc.append(np.round(x) + 1j* np.round(y))

    zb = zd
    

    ## Tier >= 2 clustering   
    for i in range(2,tier+1):
        for jj in range(6*(i-1)):
            
            for k in range(6):                
                x = np.real(zb[jj]) + np.real(zd[k])
                y = np.imag(zb[jj]) + np.imag(zd[k])                
                bs_loc = np.append(bs_loc, (np.round(x) + 1j* np.round(y)))                    
        
        bs_loc = np.unique(bs_loc)
              
        # identify boundary points after every level
        zb = []                 
        sort_ind = np.argsort(np.round(np.absolute(bs_loc)))[::-1]
        bs_loc_sorted = bs_loc[sort_ind]

        zb = bs_loc_sorted[0:6*i]        
        zb = np.unique(zb)
        

   
    # To find the vertices of a hexagon having the center (0,0)   
    theta2 = np.pi/6 # (angle subtended by a regular hexagon)/2, a fixed quantity
    hexvrtx = []
    for i in range(6):         
        hexvrtx.append(isd/np.sqrt(3) * complex(np.cos(theta2), np.sin(theta2))) # hexvrtx = vertices of hexagon
        theta2 = theta2 + np.pi/3 # pi/3 = angle subtended by a regular hexagon

    # remove insignificant figures    
    hexvrtx = np.array(hexvrtx)
    hexvrtx = hexvrtx * 10000.0
    hexvrtx = np.round(hexvrtx)
    hexvrtx = hexvrtx/10000.0

    ## To find vertices along the boundary
    allhexvrtx = []
    for i in range(no_cells):
        for j in range(6):                        
            allhexvrtx.append(hexvrtx[j] + bs_loc[i]) # allhexvrtx = set of all hexagon cell vertices
            

    # remove redundant points
    allhexvrtx = np.array(allhexvrtx)
    allhexvrtx = allhexvrtx * 10000.0
    allhexvrtx = np.round(allhexvrtx)
    allhexvrtx = allhexvrtx/10000.0    
    allhexvrtx = np.unique(allhexvrtx)

    ## Extract boundary vertices
    bdryvrtx1 = np.sort(allhexvrtx)[::-1]
    bdryvrtx = bdryvrtx1[0:no_bdryvrtx] # bdryvrtx = boundary vertices (irregular order)

    # Arrange boundary vertices in an order along the contour
    a = np.angle(bdryvrtx, deg=True)
    ord = np.argsort(a)
    bdryvrtx = bdryvrtx[ord] # bdryvrtx = boundary vertices (along the contour)

    ## To find directional vertices of a sectored hexgaon centered at (0,0)
    dvrtx = [] #np.zeros(3)
    for i in range(3):
        [p1, p2] = pol2cart(theta1, isd/2)
        theta1 = theta1 + 2*np.pi/3
        dvrtx.append(complex(p1, p2)) 

    return bs_loc, hexvrtx, allhexvrtx, bdryvrtx, dvrtx 
