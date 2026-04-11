import math

def identity():
    return [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
    ]

def translation(tx, ty):
   return [
   [1, 0, tx],
   [0, 1, ty],
   [0, 0, 1]
   ]
   
def scale(sx, sy):
    return [
    [sx, 0, 0],
    [0, sy, 0],
    [0, 0, 1]
    ]   

def rotation(theta):
    c = math.cos(theta)
    s = math.sin(theta)
    return [
    [c, -s, 0],
    [s, c, 0],
    [0, 0, 1]    
    ]

def new_transformation():
    return identity()