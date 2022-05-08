'''
This module is used as a container for global variables, 
which need to be accessed from both HTPAinterface 
and IMGinterface modules
'''
import numpy 

def init():
    global temp_array
    temp_array = 0
    global terminate_flag
    terminate_flag = False
    
