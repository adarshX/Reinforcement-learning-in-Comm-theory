# LTE Rel. 9: simulate basic rate for each user per resource block

import numpy as np
import scipy.io as sio
import config
import pdb
from config import * 
from cellsetup1 import cellsetup1
from cellsetup2 import cellsetup2
import random
import time

config.init()

################################### Inputs #######################################

# no of users
config.no_users = 8

# no of subchannels
config.total_subch = 8

###################################################################################

# Transmit power
PtdBm = 46
Pt = (np.power(10, (PtdBm/10.0))) * 0.001 # Power for MBS
Psub = Pt/100.0

## create user objects
config.user_obj = []
for ii in range(config.no_users):
    config.user_obj.append(users())    

## set user IDs
for ii in range(config.no_users):
    config.user_obj[ii].id = ii

# deploy users in the cell
[bs_loc, user_loc] = cellsetup1(config.no_users)

for ii in range(config.no_users):
    config.user_obj[ii].bs_loc = bs_loc
    config.user_obj[ii].user_loc = user_loc[ii]

basic_rate = cellsetup2(bs_loc, user_loc, Psub)