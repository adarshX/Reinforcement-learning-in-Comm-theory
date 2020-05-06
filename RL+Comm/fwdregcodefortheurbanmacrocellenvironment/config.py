# This configuration file is used to declare and initialize global variables

def init():
    
    global total_subch
    global no_users
    global user_obj
    global total_no_users    
    
    total_subch = 0
    no_users = 0    
    total_no_users = 0    

class users:

    def __init__(self):
        self.data = []
        self.id = 0
        self.bs_loc = 0
        self.user_loc = 0
        self.sinrdB = 0
        self.basic_rate = [] 
        self.scheduled_rate = [] 
        self.alloc_subch = []                 