import numpy as np

duration = 10
dt = 0.01

nz_gyro = 10
nz_accel = 2

A = np.array([[1, 0], 
              [0, 1]])
B = np.array([[1, dt, 0, 0], 
              [0, 0, 1, dt]])

C = np.array([[dt, 0], [0, dt]])

u = np.array([[0],[0],[0],[0]])

x_init = np.array([0], [0])

x = x_init
x_hat = x_init

iter = 0

while iter <= duration:
    
    iter += dt