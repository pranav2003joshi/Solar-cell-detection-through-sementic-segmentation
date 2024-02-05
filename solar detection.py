import imageio
import numpy as np
import rasterio
import pandas as pd
from sklearn.cluster import DBSCAN

# Load your TIFF image
image_path = 'trimbak_road.tiff'  # Replace with your TIFF image path
image = imageio.imread(image_path)

# Define the lower and upper bounds for the light creme to dark brown range
lower_light_creme = np.array([30,40,55])
upper_dark_brown = np.array([40,50,65])

# Create a mask that selects pixels within the specified range
mask = np.all(np.logical_and(lower_light_creme <= image, image <= upper_dark_brown), axis=-1)

# Apply the mask to the original image to isolate the colors in the specified range
light_creme_to_dark_brown_pixels = np.zeros_like(image)
light_creme_to_dark_brown_pixels[mask] = image[mask]

# Save the segmented pixels to an image file
output_path = 'light_creme_to_dark_brown_segmented.tif'
imageio.imwrite(output_path, light_creme_to_dark_brown_pixels, format='TIFF')

print("Segmented pixels in the light creme to dark brown range saved to", output_path)

# Extract geospatial information (latitude and longitude)
with rasterio.open(image_path) as src:
    # Get the transformation matrix
    transform = src.transform

    # Get the coordinates of the pixels in the mask
    rows, cols = np.where(mask)

    # Convert pixel coordinates to geographic coordinates (latitude and longitude)
    lon, lat = rasterio.transform.xy(transform, rows, cols)

# Now, you can save the latitude and longitude information to a CSV or text file
with open('lat_lon_coordinates.csv', 'w') as f:
    f.write('Latitude,Longitude\n')
    for lat, lon in zip(lat, lon):
        f.write(f'{lat},{lon}\n')

print("Latitude and Longitude coordinates saved to lat_lon_coordinates.csv")
def clustering(input_data):
    # Load your CSV data into a DataFrame
    data = pd.read_csv(input_data)

    # Assuming your CSV contains 'latitude' and 'longitude' columns
    coordinates = data[['Latitude', 'Longitude']]

    # Define the DBSCAN model
    epsilon = 0.0008 # Adjust this value based on the spatial density of your data
    min_samples = 30 # Adjust this value based on your data and the level of noise you want to eliminate
    dbscan = DBSCAN(eps=epsilon, min_samples=min_samples)

    # Fit the DBSCAN model to your data
    data['cluster'] = dbscan.fit_predict(coordinates)

    # Noise points will have a cluster label of -1, and valid points will have a positive integer cluster label

    # Save the data with noise points removed to a new CSV file
    cleaned_data = data[data['cluster'] != -1]
    cleaned_data.to_csv('cleaned_data.csv', index=False)

clustering('lat_lon_coordinates.csv')


