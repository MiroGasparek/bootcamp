# 30 May 2018 Miroslav Gasparek
# Python bootcamp, lesson 39: Basic image quantification with Python

# Import modules
import numpy as np

# Import image processing tools
import skimage.filters
import skimage.io
import skimage.morphology
import skimage.exposure
import skimage.segmentation

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Load the images
im_phase = skimage.io.imread('data/HG105_images/noLac_phase_0004.tif')
im_fl = skimage.io.imread('data/HG105_images/noLac_FITC_0004.tif')

# Display side by side
with sns.axes_style('dark'):
    fig, ax = plt.subplots(1, 2, figsize=(9.5, 8))
    ax[0].imshow(im_phase, cmap=plt.cm.viridis)
    ax[1].imshow(im_fl, cmap=plt.cm.viridis)

# Run a quick median filter through the image

# Structuring element
selem = skimage.morphology.square(3)

# Perform median filter
im_phase_filt = skimage.filters.median(im_phase, selem)
im_fl_filt = skimage.filters.median(im_fl, selem)

# Show the images again
with sns.axes_style('dark'):
    fig, ax = plt.subplots(1, 2, figsize=(9.5, 8))
    ax[0].imshow(im_phase_filt, cmap=plt.cm.viridis)
    ax[1].imshow(im_fl_filt, cmap=plt.cm.viridis)

# We can subtract the undesired background likely caused by
# improper Kohler illumination by Gaussian background subtraction

# Apply a gaussian blur with a 50 pixel radius
im_phase_gauss = skimage.filters.gaussian(im_phase_filt, 50.0)

# Show the two images side-by-side
with sns.axes_style('dark'):
    fig, ax = plt.subplots(1,2, figsize=(9.5, 8))
    ax[0].imshow(im_phase_filt, cmap=plt.cm.viridis)
    ax[1].imshow(im_phase_gauss, cmap=plt.cm.viridis)

# We need to convert input image (uint16) to (float64) type

# Convert the median-filtered phase image to a float64
im_phase_float = skimage.img_as_float(im_phase_filt)

# Subtract our gaussian blurred image from the original
im_phase_sub = im_phase_float - im_phase_gauss

# Show our original image and background subtracted image side-by-side
with sns.axes_style('dark'):
    fig, ax = plt.subplots(1, 2, figsize=(9.5, 8))
    ax[0].imshow(im_phase_float, cmap=plt.cm.viridis)
    ax[1].imshow(im_phase_sub, cmap=plt.cm.viridis)

# Segmenting the bacteria
# As images are represented as NumPy arrayes when loaded, they can be zoomed
# to selecting a certain tuple of pixels (for instance, using np.s_)

# Indices of subimage
slc = np.s_[0:450, 50:500]

# Look at subimage
with sns.axes_style('dark'):
    plt.imshow(im_phase_sub[slc], cmap=plt.cm.gray)

# The dots in the picture are caused by the condensation of the water vapor
# on the glass in front of the CCD of the camera

# They can be removed using total variation filter, which calcualtes local
# derivatives in the image and tries to limite them.

# Perform a Chambolle total variation filter.
im_phase_tv = skimage.restoration.denoise_tv_chambolle(im_phase_sub, weight=0.005)

# Look at result
with sns.axes_style('dark'):
    fig, ax = plt.subplots(1, 2, figsize=(9.5, 8))
    ax[0].imshow(im_phase_filt[slc], cmap=plt.cm.viridis)
    ax[1].imshow(im_phase_tv[slc], cmap=plt.cm.viridis)

# Compute Otsu threshold value for median filtered image
thresh_otsu = skimage.filters.threshold_otsu(im_phase_sub)

# Construct thresholded image
im_bw = im_phase_sub < thresh_otsu

# Display images
with sns.axes_style('dark'):
    fig, ax = plt.subplots(2, 2, figsize=(9.5, 8))
    ax[0,0].imshow(im_phase_sub, cmap=plt.cm.gray)
    ax[0,1].imshow(im_bw, cmap=plt.cm.gray)
    ax[1,0].imshow(im_phase_sub[slc], cmap=plt.cm.gray)
    ax[1,1].imshow(im_bw[slc], cmap=plt.cm.gray)

plt.close('all')
# We only want to have whole bacteria considered, to quantify the fluorescent
# density

# Clear border with 5 pixel buffer
im_bw = skimage.segmentation.clear_border(im_bw, buffer_size=5)

# We need to label the image to see which "islands" of white pixels are bacteria

# Label binary image; background kwarg says value in im_bw to be background
im_labeled, n_labels = skimage.measure.label(im_bw, background=0, return_num=True)

# See resuult (one of the few times it is OK to use rainbow colormap)
with sns.axes_style('dark'):
    plt.imshow(im_labeled, cmap=plt.cm.rainbow)

# Show nubmer of regions
print('Number of individual regions = ', n_labels)

# Out of 24 regions, there are still some 4 of them that are simply noise
# despite of cleaning
# skimage.measure.regionprops() computes the area of each region (and other
# userful statistics)

# Using intensity_image, keyword argument, we can also specify a corresponding
# intensity image, in this case fluorescent image.

# Extract region props
im_props = skimage.measure.regionprops(im_labeled, intensity_image=im_fl_filt)

# Now we need to eliminate regions that are too small to be bacteria

# Show zoomed in image
with sns.axes_style('dark'):
    plt.imshow(im_phase_filt[slc], cmap=plt.cm.gray)

# From the image, it can be estimated that the bacteria are about 30 px long
# and 10 px wide, lets say that cut-off for bacteria is half of it, i. e. 150 px

# Data stored in im_props can be used to clear up the image

# Make a filtered black and white image
im_bw_filt = im_labeled > 0

# Define cut-off size
cutoff = 150

# Loop through image properties and delete small objects
n_regions = 0
for prop in im_props:
    if prop.area < cutoff:
        im_bw_filt[im_labeled==prop.label] = 0
    else:
        n_regions += 1

# Look at result
# with sns.axes_style('dark'):
#     plt.imshow(im_bw_filt, cmap=plt.cm.gray)
#
# # Show number of regions
# print('Number of individual regions = ', n_regions)
#
# # There is an issue of regions with two bacteria
# # Show zoomed in image
# with sns.axes_style('dark'):
#     plt.imshow(im_bw_filt[slc], cmap=plt.cm.gray)


# Try to eliminate cells that are side-by-side and only keep the "lonely" cells.

# Test for bacteria that are side-by-side, versus those that are in line with
# each other, as would be the case for a dividing bacterium
# Use eccentricity measure of the region.

# Eccentricity of the ellipse that has the same second-moments as the region.
# The eccentricity is the ratio of the distance between its minor and major
# axis length

# We only want objects with large eccentricity, say above 0.85

# Loop through image properties and delete small objects and round objects
n_regions = 0
for prop in im_props:
    if prop.area < cutoff or prop.eccentricity < 0.85:
        im_bw_filt[im_labeled==prop.label] = 0
    else:
        n_regions += 1

# Look at result
with sns.axes_style('dark'):
    plt.imshow(im_bw_filt[slc], cmap=plt.cm.gray)

# Show number of regions
print('Number of individual regions, "lonely cells" only = ', n_regions)

# Now compute the summed intensity of all regions

# Initial list of intensities of individual bacteria
int_intensity = []

# Loop through regions and compute integrated intensity of bacteria
for prop in im_props:
    if prop.area > cutoff and prop.eccentricity > 0.8:
        int_intensity.append(prop.area * prop.mean_intensity)

# Convert list to NumPy array
int_intensity = np.array(int_intensity)

# Take a look
print(int_intensity)

# Overlay the fluorescent imagea with the phase contrast image
# Fluorescent color is green and ranging from zero to one

# Build RGB image by stacking grayscale images
im_rgb = np.dstack(3 * [im_phase_filt / im_phase_filt.max()])

# Only show green channel on bacteria
im_rgb[im_bw_filt, 0] = 0
im_rgb[im_bw_filt, 1] = im_fl_filt[im_bw_filt] / im_fl_filt.max()

# Show the result
with sns.axes_style('dark'):
    fig, ax = plt.subplots(1, 2, figsize=(9.5, 8))
    ax[0].imshow(im_rgb)
    ax[1].imshow(im_rgb[slc][:]);

plt.show()
