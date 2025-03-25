import numpy as np

# Interior camera parameters (intrinsic matrix)
# Example: fx, fy are focal lengths, cx, cy are principal point offsets
K = np.array([
    [fx, 0, cx],
    [0, fy, cy],
    [0,  0,  1]
])

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
