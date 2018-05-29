# 29 May 2018 Miroslav Gasparek
# Python bootcamp, lesson 38: Image processing with Python

# Import modules
import numpy as np

# Import image processing tools
import skimage.filters
import skimage.io
import skimage.morphology
import skimage.exposure

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Image segmentation

# Load the phase contrast image.
im_phase = skimage.io.imread('data/bsub_100x_phase.tif')

# Display the image, set Seaborn style 'dark' to avoid grid lines
# with sns.axes_style('dark'):
#     skimage.io.imshow(im_phase)

# The weird image will be displayed due to being 12-bit camera instead of 16 bit

# Display image so that it is divided by maximum range of scale
# with sns.axes_style('dark'):
#     skimage.io.imshow(im_phase / im_phase.max())


# Alternatively, matplotlib's image viewing function can be used
# which automatically adjusts the image. We need to specify the colormap
# to look at it
with sns.axes_style('dark'):
    # Generate subplots
    fig, ax = plt.subplots(2,2, figsize=(8,6))

    # Display various Look-Up Tables
    ax[0,0].imshow(im_phase, cmap=plt.cm.gray)
    ax[0,1].imshow(im_phase, cmap=plt.cm.RdBu_r)
    ax[1,0].imshow(im_phase, cmap=plt.cm.viridis)
    ax[1,1].imshow(im_phase, cmap =plt.cm.copper)

plt.close()
# Get the histogram of the image to see the trends in pixels
hist_phase, bins_phase = skimage.exposure.histogram(im_phase)

# Usematplotlib to make a pretty plot of histogram data
fig2 = plt.figure(2)
plt.fill_between(bins_phase, hist_phase, alpha=0.5)

# Label axes
plt.xlabel('pixel value')
plt.ylabel('count')

plt.close()

# The histogram shows the value at which the pixels can be distinguished between
# the peak corresponding to the background and the very small peak around 200
# corresponding to bacteria. The threshold can be set to 300

# Use matplotlib to make a pretty plot of histogram data
fig3 = plt.figure(3)
plt.fill_between(bins_phase, hist_phase, alpha=0.5)
plt.plot([300, 300], [0, 35000], linestyle='-', marker='None', color='red')

# Label axes
plt.xlabel('pixel value')
plt.ylabel('count')

plt.close()

# Threshold value, as obtained by eye(balling)
thresh_phase = 350

# Generate athresholded image
im_phase_bw = im_phase < thresh_phase

# To overlay the images in order to have a good view, we will make an RGB image
# and saturate the green channel where the thresholded image is whie

# Build RGB image by stacking grayscale images
im_phase_rgb = np.dstack(3 * [im_phase / np.max(im_phase)])

# Saturate green channe whereever there are white pixels in thresh image
im_phase_rgb[im_phase_bw, 1] = 1.0

# Show the result
fig4 = plt.figure(4)
with sns.axes_style('dark'):
    plt.imshow(im_phase_rgb)

plt.close(fig4)

# This shows that we did OK job in finding the bacteria, but there are still
# some reminscent light dots/noise around the cells. Also the labelling of bacteria
# in the middle of colonies is not very effective - due to the halo of high intensity
# signal near boundaries of the bacteria

# Using the CFP channel
# Load image
im_cfp = skimage.io.imread('data/bsub_100x_CFP.tif')

# Display the image
fig5 = plt.figure(5)
with sns.axes_style('dark'):
    plt.imshow(im_cfp, cmap=plt.cm.gray)

plt.close(fig5)

# Display image with the viridis (default) color map
fig6 = plt.figure(6)
with sns.axes_style('dark'):
    plt.imshow(im_cfp, cmap=plt.cm.viridis)

    # Add in a color bar
    plt.colorbar()

plt.close()
# Apparently, the bacteria are typically brighter than the background, which
# is very uniform

# The background is noisy, therefore we have some bad pixels
# Display bad pixels
fig7 = plt.figure(7)
with sns.axes_style('dark'):
    plt.imshow(im_cfp[150:250, 450:550] / im_cfp.max(), cmap=plt.cm.viridis)

plt.close()
# We will filter out the bad pixels using a median filter
# We have to construct a filtering mask using skimage.morphology module

# Make the structuring element
selem = skimage.morphology.square(3)

# Perform the median filter
im_cfp_filt = skimage.filters.median(im_cfp, selem)

# Show filtered image with the viridis Look-Up Table
fig8 = plt.figure(8)
with sns.axes_style('dark'):
    plt.imshow(im_cfp_filt, cmap=plt.cm.viridis)
    plt.colorbar()

plt.close()

# Apparently, some of the cells are very bright compared with others
# also, the colorbar has changed, and noise was eliminated too

# Plot another histogram of the filtered image and see the thresholds
hist_cfp, bins_cfp = skimage.exposure.histogram(im_cfp_filt)

# Use matplotlib to make a pretty plot of histogram data
fig9 = plt.figure(9)
plt.fill_between(bins_cfp, hist_cfp, alpha=0.5)
plt.plot([115, 115], [0, 50000], 'r-')

# Label axes
plt.xlabel('pixel value')
plt.ylabel('count')

plt.close()

# Threshold value obtained by eye(balling) from the thresholded image
thresh_cfp = 120

# Generate thresholded image
im_cfp_bw = im_cfp_filt > thresh_cfp

# Display phase and thresholded image
with sns.axes_style('dark'):
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].imshow(im_cfp_filt, cmap=plt.cm.gray)
    ax[1].imshow(im_cfp_bw, cmap=plt.cm.gray)

plt.close()

# Let's try to overlap the images
# Build RGB image by stacking grayscale images
im_cfp_rgb = np.dstack(3 * [im_cfp_filt / im_cfp_filt.max()])

# Saturate red channel wherever there are white pixels in thresh image
im_cfp_rgb[im_cfp_bw, 1] = 1.0

# Show the result
with sns.axes_style('dark'):
    plt.imshow(im_cfp_rgb)

plt.close()

# Otsu's method for thresholding

# Compute Otsu thresholds for phase and cfp
thresh_phase_otsu = skimage.filters.threshold_otsu(im_phase)
thresh_cfp_otsu = skimage.filters.threshold_otsu(im_cfp_filt)

# Compare results to eyeballing it
print('Phase be eye: ', thresh_phase, 'CFP by eye: ', thresh_cfp)
print('Phase by Otsu ', thresh_phase_otsu,
        'CFP by Otsu: ', thresh_cfp_otsu)

# There is a big difference if Otsu method is applied to the phase image
# It is because the Otsu method assumes a bimodal distribution of pixels
# Phase image has a long tail on the log scale
# Always check if automated thresholding works well!

# Plot the histograms together.
plt.fill_between(bins_phase, np.log10(hist_phase), alpha=0.5)
plt.fill_between(bins_cfp, np.log10(hist_cfp), alpha=0.5,
                 color=sns.color_palette()[1])
plt.plot([thresh_phase_otsu, thresh_phase_otsu], [0, 6], 'b-')
plt.plot([thresh_cfp_otsu, thresh_cfp_otsu], [0, 6], 'g-')
plt.legend(('phase', 'CFP'), loc='upper right')

# Label axes
plt.xlabel('pixel value')
plt.ylabel('log$_{10}$ count')

plt.show()

# Determining the bacterial area
# To determine the bacterial area, we simply sum up the pixel values of
# the thresholded image

# Compute bacterial area
bacterial_area_pix = im_cfp_bw.sum()

# Print out the result
print('bacterial area = ', bacterial_area_pix, 'pixels')

# The interpixel distance for this setup is 0.0636 um, so bacterial areas
# can be computed

# Define interpixel distance
interpix_dist = 0.063 # microns

# Compute bacterial area
bacterial_area_micron = bacterial_area_pix * interpix_dist**2

# Print total area
print('bacterial area = ', bacterial_area_micron, 'square microns')
