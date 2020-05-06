# function returns sinr in dB given at specified user locations.
# assumes that the user is always associated to the central BS
import numpy as np
import pdb

#function sinrdB = sinrdB_calculate(user_loc,bs_loc,Psub,noise_power,efflossdB)
def sinrdB_calculate(user_loc, bs_loc, Psub, noise_power, efflossdB):

    sinrdB = []
    AGdB = 15 # antenna gain (fixed)

    for item in user_loc:

        x = np.real(item) #real(p)
        y = np.imag(item) #imag(p)

        # compute the distance between the user point and each of 37 BS    
        dd = np.sqrt(np.square(np.real(bs_loc) - x) + np.square(np.imag(bs_loc) - y)) # dd = 37-length vector       
        dd = [item if item >= 35 else 35 for item in dd]
        #dd(dd<35) = 35
        dd = np.array(dd)

        # Calculate Path-Loss                
        pldB = 128.1 + 37.6*np.log10(dd/1000.0)
        
        # Total loss
        total_gaindB = AGdB - (pldB + efflossdB)
        rx_gain = np.power(10, (total_gaindB/10.0)) 
        rx_power = Psub*rx_gain        

        # Signal power        
        signal_power = rx_power[18] # user associated always to the BS at (0,0)

        # Interference power    
        intf_power = sum(rx_power) - signal_power # interference power is only from respective sector

        # SINR calculation at each user point    
        sinr = signal_power/(intf_power+noise_power) # SINR calculation for the point
        sinrdB.append(10*np.log10(sinr)) # SINR in dB    
        
    
    return sinrdB
