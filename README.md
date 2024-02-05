# Solar-cell-detection-through-sementic-segmentation
 Let's dive into more detail for each step:

1. **Image Loading:**
   - The code begins by loading a TIFF image using the `imageio` library, storing the pixel values in the variable `image`.

2. **Color Segmentation:**
   - Color segmentation involves isolating specific colors within an image.
   - `lower_light_creme` and `upper_dark_brown` define a color range in terms of RGB values.
   - The `mask` is created using `numpy` operations to identify pixels in the specified color range.
   - A new image, `light_creme_to_dark_brown_pixels`, is created by applying the mask to the original image. This isolates pixels with colors within the specified range.

3. **Saving Segmented Pixels to Image:**
   - The segmented pixel data is saved to a new TIFF image (`light_creme_to_dark_brown_segmented.tif`) using the `imageio.imwrite` function.

4. **Extracting Geospatial Information:**
   - The `rasterio` library is used to open the original TIFF image and extract geospatial information.
   - The transformation matrix (`transform`) and pixel coordinates (`rows` and `cols`) are obtained.

5. **Saving Latitude and Longitude Information:**
   - Latitude and longitude coordinates are derived from pixel coordinates using the transformation matrix.
   - The coordinates are then saved to a CSV file (`lat_lon_coordinates.csv`) for future use.

6. **DBSCAN Clustering Function:**
   - A function named `clustering` is defined to perform Density-Based Spatial Clustering of Applications with Noise (DBSCAN) on geographic coordinates.
   - The CSV data with latitude and longitude information is loaded into a Pandas DataFrame.
   - The DBSCAN model is instantiated with parameters `epsilon` (maximum distance between two samples for one to be considered in the neighborhood of the other) and `min_samples` (the number of samples in a neighborhood for a point to be considered a core point).
   - The DBSCAN model is fitted to the coordinates, and a new 'cluster' column is added to the DataFrame, assigning cluster labels to each data point.
   - Noise points are assigned a cluster label of -1.

7. **Cleaning Data from Noise:**
   - Data points labeled as -1 (indicating noise) are removed from the DataFrame.
   - The cleaned data is saved to a new CSV file (`cleaned_data.csv`) containing only valid data points.

8. **Function Execution:**
   - Finally, the `clustering` function is called with the previously saved latitude and longitude coordinates (`lat_lon_coordinates.csv`). The function performs DBSCAN clustering, removes noise, and saves the cleaned data to a new CSV file.
