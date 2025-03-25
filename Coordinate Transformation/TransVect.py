import numpy as np

# Constants for WGS84
a = 6378137.0  # Semi-major axis (meters)
e = 0.08181919  # Eccentricity

def gps_to_ecef(lat, lon, alt):
    """
    Convert GPS coordinates (latitude, longitude, altitude) to ECEF coordinates.
    
    lat: Latitude in degrees
    lon: Longitude in degrees
    alt: Altitude in meters
    
    Returns: (X, Y, Z) in ECEF coordinates (meters)
    """
    # Convert latitude and longitude to radians
    lat = np.deg2rad(lat)
    lon = np.deg2rad(lon)
    
    # Radius of curvature in the prime vertical
    N = a / np.sqrt(1 - e**2 * np.sin(lat)**2)
    
    # ECEF coordinates
    X = (N + alt) * np.cos(lat) * np.cos(lon)
    Y = (N + alt) * np.cos(lat) * np.sin(lon)
    Z = (N * (1 - e**2) + alt) * np.sin(lat)
    
    return X, Y, Z

# Example: Satellite GPS coordinates
satellite_lat = 40.748817  # Latitude in degrees
satellite_lon = -73.985428  # Longitude in degrees
satellite_alt = 550000  # Altitude in meters (example satellite height)

# Convert satellite GPS to ECEF
sat_X, sat_Y, sat_Z = gps_to_ecef(satellite_lat, satellite_lon, satellite_alt)
print(f"Satellite ECEF Coordinates: X={sat_X}, Y={sat_Y}, Z={sat_Z}")

# Example: Ground control point GPS coordinates
gcp_lat = 40.748817  # Latitude in degrees
gcp_lon = -73.985428  # Longitude in degrees
gcp_alt = 10  # Altitude in meters (ground level)

# Convert ground control point GPS to ECEF
gcp_X, gcp_Y, gcp_Z = gps_to_ecef(gcp_lat, gcp_lon, gcp_alt)
print(f"GCP ECEF Coordinates: X={gcp_X}, Y={gcp_Y}, Z={gcp_Z}")



## Calculating the Transformation Vector

# Calculate the translation vector (relative position of satellite to the ground control point)
T = np.array([sat_X - gcp_X, sat_Y - gcp_Y, sat_Z - gcp_Z])
print("Translation vector T (relative to GCP):", T)
