'''
This module is used as a container for global variables, 
which need to be accessed from both HTPAinterface 
and IMGinterface modules
'''

def init():
    global pixel_line
    pixel_line = [0,0,0]
    global terminate_flag
    terminate_flag = False
    
