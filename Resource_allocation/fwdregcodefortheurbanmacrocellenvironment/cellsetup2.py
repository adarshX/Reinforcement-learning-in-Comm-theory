# Basic Rate calculation with shadowing without sectoring
import cmath
import numpy as np
import pdb
from sinrdB_calculate import sinrdB_calculate
from SINR_MCS_mapping import SINR_MCS_mapping

def cellsetup2(bs_loc, user_loc, Psub):

    ## System settings
    slow_fading_factor = 10 # higher, more slow is the fading

    # no of cells considered
    no_cells = 37

    # Noise power
    noise_power = 2.2661e-15

    # Subchannels
    # no_subch = 100 # total no of subchannels per cell
    # no_sect_subch = no_total_subch/3 # no of subchannels per sector
    # (assuming equal number of subchannels per sector)

    # Miscelleneous system parameters (constant)
    sc_ofdm = 12 # no of OFDM subcarriers per subchannel bandwidth
    sy_ofdm = 14 # no of OFDM symbols per subframe
    T_subframe = 1e-3 # subframe duration
    rate_subch = sc_ofdm*sy_ofdm/(T_subframe*1.0) # rate of each subchannel = 168kbps
    # linkrate = rate_subch*no_total_subch # link rate = (rate at each subchannel)*(no of subchannels)

    ## Effective loss due to pathloss, shadowing etc.

    # Losses
    ptnlossdB = 20 # Penetration loss
    cablelossdB = 2 # Cable loss
    shadowing_fixed = 0 # 1 = constant shadowing gain, 0 = varying shadowing (slow fading channel)

    # effective loss
    efflossdB = ptnlossdB + cablelossdB # without shadowing

    # shadowing
    sinrdB = 0
    eff = 0    
    basicrate = 0

    # shadowing
    if(shadowing_fixed == 1): # fixed shadowing gain
        shadowingdB = 0
    else:    
        if(slow_fading_factor > 1):
            shadowingdB1 = 10 * np.random.randn(slow_fading_factor, no_cells)
            shadowingdB = np.mean(shadowingdB1, axis=0)
        else:
            shadowingdB = 10 * np.random.randn(slow_fading_factor, no_cells)    

    # effective loss
    efflossdB = shadowingdB + efflossdB    

    # SINR calculation. Here the user is always connectd to the BS (0,0)
    sinrdB = sinrdB_calculate(user_loc, bs_loc, Psub, noise_power, efflossdB)
   
    ## Rate calculation at each user location using sinr

    # sinrdB to efficiency(bits/symbol) mapping - method-1
    [CQI, eff] = SINR_MCS_mapping(sinrdB)
    basicrate = [item*rate_subch for item in eff] # eff*rate_subch

    return basicrate