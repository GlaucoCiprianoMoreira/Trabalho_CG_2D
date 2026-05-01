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

def multiply(A, B):
    result = [[0,0,0],[0,0,0],[0,0,0]]

    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] += A[i][k] * B[k][j]

    return result

def apply(point, M):
    x, y = point

    px = M[0][0]*x + M[0][1]*y + M[0][2]
    py = M[1][0]*x + M[1][1]*y + M[1][2]

    return int(px), int(py)