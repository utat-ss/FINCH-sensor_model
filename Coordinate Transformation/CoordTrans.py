import numpy as np

# Interior camera parameters (intrinsic matrix) obtained from the calibration
# Example: fx, fy are focal lengths, cx, cy are principal point offsets
fx, fy = 1.8214e+4, 1.8204e+04
cx, cy = 3.1802e+03, 2.3473e+03

K = np.array([
    [fx, 0, cx],
    [0, fy, cy],
    [0,  0,  1]
])

# Exterior camera parameters obtained from the calibration
r11 = 0.7220
r12 = 0.6904
r13 = 0.0462
r21 = -0.5244
r22 =  0.5023
r23 =  0.6875
r31 =  0.4514
r32 = -0.5206
r33 =  0.7247

tx =  -194.0879
ty =  -28.7300
tz =  1507.4

# Exterior camera parameters (rotation and translation)
# Rotation matrix (3x3)
R = np.array([
    [r11, r12, r13],
    [r21, r22, r23],
    [r31, r32, r33]
])

# Translation vector (3x1)
T = np.array([tx, ty, tz])

# Combine rotation and translation into a 3x4 matrix
RT = np.hstack((R, T.reshape(-1, 1)))

# X, Y, Z coordinates are picked randomly, as defined below:
# Pick the checkerboard corner at row=2, col=3 (0‐based), with square_size=25 mm:
square_size = 25.0  # each square is 25 mm on a side
row_index = 2 # i = 2
col_index = 3 # j = 3
X = col_index * square_size # = 3 * 25 = 75 mm
Y = row_index * square_size # = 2 * 25 = 50 mm
Z = 0.0 # board is flat, so Z=0 for any corner

# 3D point in world coordinates
X_world = np.array([X, Y, Z, 1])  # Homogeneous coordinates

#TODO: Need to define the intrinsic and extrinsic parameters
# fx, fy, cx, cy, r11, r12, r13, r21, r22, r23, r31, r32, r33, tx, ty, tz
# Need to find the R matrix and T vector from the given rotation and translation values
# Need to builf the K matrix from the given intrinsic parameters

# BELOW IS THE USAGE OF THE COORDDINATE TRANSFORMATION
# Project the 3D point to the image plane
x_image_homogeneous = K @ RT @ X_world

# Normalize to get the 2D image coordinates
x_image = x_image_homogeneous[:2] / x_image_homogeneous[2]
print("2D Image coordinates:", x_image)
