from trig_utility import *
def uniform_random_polygon(isd, hexvrtx, no_users):

    radius_c = (isd*1.0)/np.sqrt(3) # radius of the circumscribing circle of hexagon

    count = 0 # keeps count of no of successful user locations deployed randomly inside polygon
    user_pts = []    

    while(count < no_users): 
        
        diff = no_users - count

        r = 0
        theta = 0
        x = [] 
        y = []
        p = []

        r = (np.random.uniform(0, 1, diff)) * radius_c
        theta = (np.random.uniform(0, 1, diff)) * 2*np.pi    
        for idx in range(diff):
            [x, y] = pol2cart(theta[idx], r[idx])
            p.append(x + 1j*y)

        for i in range(diff):
            #!!!!
            # use contains_points
            #IN = inpolygon(real(p[i]), imag(p[i]), real(hexvrtx), imag(hexvrtx))
            #if(IN == 1):
            count = count + 1
            user_pts.append(p[i])

    user_pts = np.array(user_pts)
    user_pts = user_pts * 10000.0
    user_pts = np.round(user_pts)
    user_pts = user_pts/10000.0
    
    return user_pts     

