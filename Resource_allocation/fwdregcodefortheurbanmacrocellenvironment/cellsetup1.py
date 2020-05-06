# Distribution of users

from cellular_pattern_generator import *
from uniform_random_polygon import *
import pdb

def cellsetup1(no_users):

## cellular pattern settings

    isd = 500

    tier = 3
    no_cells = 37 # No of cells. (tier,value) = (1,7) (2,19) (3,37) (4,61) (5,91)
    no_bdryvrtx = 42 # No of boundary vertices. (tier,value) = (1,12) (2,30) (3,42) (4,54)

    [bs_loc, hexvrtx, allhexvrtx, bdryvrtx, dvrtx] = cellular_pattern_generator(isd, tier, no_cells, no_bdryvrtx)

    # without sectoring
    user_loc = uniform_random_polygon(isd,hexvrtx,no_users)
    
    return bs_loc, user_loc



