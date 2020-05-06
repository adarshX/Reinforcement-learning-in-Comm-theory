#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import scipy.io as sio
import config
import pdb
from config import *
from cellsetup1 import cellsetup1
from cellsetup2 import cellsetup2
import random
import time
from collections import deque

config.init()


# In[20]:


class RA:
    def __init__(self,num_users,num_subch,num_timeslots):
        self.encoding_rates = [100,300,600,1200,3000,5000]
        self.num_enc_rates = len(self.encoding_rates)
        self.num_users = num_users
        self.num_subch = num_subch
        self.num_timeslots = num_timeslots
        self.T_ura = 3000
        self.T_dra = 3000
        self.user_rates_indices = np.zeros(self.num_users,dtype= int) 
        self.user_rates = np.zeros(self.num_users)
        self.rebuff_indicator = np.zeros(self.num_users,dtype=int)
        self.throughput = np.zeros(self.num_users)
        self.bits_buffer = np.zeros(self.num_users)
        self.allocated_rates = np.zeros(self.num_users)
        self.allocated_channels = np.ones(self.num_users)
        self.throughput_buffer = deque()
        self.pb_timer = np.zeros(num_users,dtype= int)
        self.rebuff_timer = np.zeros(num_users,dtype= int)
    
    ### rate_adaptation
    def rate_adaptation(self):
        for i in range(self.num_users):
            ### check if in rebuffering state
            if self.bits_buffer[i] <= 0: ### into rebuffering state
                self.pb_timer[i] = 0
                self.bits_buffer[i] = 0
                self.rebuff_indicator[i] = 1
                self.rebuff_timer[i] = self.rebuff_timer[i] + 1000
                if self.rebuff_timer[i] == self.T_dra:
                    self.user_rates_indices[i] = 0
                    self.rebuff_timer[i] = 0
            else:
                if self.rebuff_indicator[i] == 1:
                    self.rebuff_indicator[i] = 0
                    if self.user_rates_indices[i] > 0:
                        self.user_rates_indices[i] = self.user_rates_indices[i] - 1
                    self.rebuff_timer[i] = 0
                elif self.rebuff_indicator[i] == 0:
                    if self.pb_timer[i] == self.T_ura and self.user_rates_indices[i] < self.num_enc_rates-1:
                        self.pb_timer[i] = 0
                        self.user_rates_indices[i] = self.user_rates_indices[i] + 1
                self.pb_timer[i] = self.pb_timer[i] + 1000 
    ### get user encoding rates
    def get_user_rates(self):
        for i in range(self.num_users):
            self.user_rates[i] = self.encoding_rates[self.user_rates_indices[i]]
    
    ### allocates the sub channels to each user
    def resource_alloc(self):
        try:
            fraction = (1/self.avg_throughput)/(np.sum(1/self.avg_throughput))
#             fraction = np.ones(self.num_users)/self.num_users
            self.allocated_channels = np.round(self.num_subch*fraction)
            if np.sum(self.allocated_channels) < self.num_subch:
                least_priv = np.argmin(self.avg_throughput)
                self.allocated_channels[least_priv] = self.allocated_channels[least_priv] + self.num_subch - np.sum(self.allocated_channels)
        except:
            print("division by zero")
    ### get average throughput
    def get_throughput(self):
        self.throughput = self.allocated_rates
        if len(self.throughput_buffer) == self.num_timeslots:
            self.throughput_buffer.popleft()
        self.throughput_buffer.append(self.throughput)
        self.avg_throughput = np.mean(np.array(self.throughput_buffer),axis=0)
    ### does the basic rate allocation for every user
    def get_basic_rate(self):
        config.no_users = self.num_users
        # no of subchannels
        config.total_subch = self.num_subch
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

        self.allocated_rates = np.array(cellsetup2(bs_loc, user_loc, Psub))/1000.0
    
    ### the main training function
    def main_func(self,vid_length):
        for i in range(1,vid_length+1):
            if i%100 == 0:
                self.get_basic_rate() ### get rates of all users
                self.get_throughput()
                self.resource_alloc()
                self.effective_rates = (self.allocated_rates)*(self.allocated_channels)
                self.bits_buffer = self.bits_buffer + self.effective_rates*0.1
            if i%1000 == 0:
                #### check rebuffering and do rate adaptation ####
                self.get_user_rates()
                self.bits_buffer = self.bits_buffer - self.user_rates
                self.rate_adaptation()


# In[21]:


ra = RA(8,8,4)
ra.main_func(120000)
ra.allocated_channels


# In[22]:


ra.user_rates_indices


# In[23]:


ra.avg_throughput


# In[ ]:


np.floor(ra.allocated_channels)


# In[ ]:


ra = RA(8,8,4)
ra.main_func(120000)
ra.allocated_channels


# In[ ]:


ra.user_rates_indices

