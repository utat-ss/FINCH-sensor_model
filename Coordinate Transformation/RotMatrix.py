import numpy as np

# Rotation angles (in radians)
theta_x = np.deg2rad(roll_angle)   # Rotation around x-axis (roll)
theta_y = np.deg2rad(pitch_angle)  # Rotation around y-axis (pitch)
theta_z = np.deg2rad(yaw_angle)    # Rotation around z-axis (yaw)

# Rotation matrices
R_x = np.array([[1, 0, 0],
                [0, np.cos(theta_x), -np.sin(theta_x)],
                [0, np.sin(theta_x), np.cos(theta_x)]])

R_y = np.array([[np.cos(theta_y), 0, np.sin(theta_y)],
                [0, 1, 0],
                [-np.sin(theta_y), 0, np.cos(theta_y)]])

R_z = np.array([[np.cos(theta_z), -np.sin(theta_z), 0],
                [np.sin(theta_z), np.cos(theta_z), 0],
                [0, 0, 1]])

# Full rotation matrix
R = R_z @ R_y @ R_x
print("Rotation matrix R:", R)
