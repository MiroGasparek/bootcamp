# 14 July 2018 Miroslav Gasparek
# Python bootcamp, lesson 40: Image processing practice with Python

# Import numerical modules
import numpy as np
import scipy.optimize

# Import modules for plotting
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# Modules for image processing
import skimage.io
import skimage.morphology
import skimage.segmentation
import skimage.measure

# Modules for interacting with our file system
import os
import glob

##### Problem 5.1: Growth curves from a movie
### a)

# Load the images into a tuple whose index corresponds to the frame number.
# Usually data validataion would be needed to make sure there
# are no skipped frames

# Initialize list of images
ims = []

# Read each image into memory using glob, which can use asterix to match
# multiple characters in the name
for fname in glob.glob('data/bacterial_growth/bacillus_*.tif'):
    ims.append(skimage.io.imread(fname))

# Store it as a tuple so it does not get messed
ims = tuple(ims)

# Number of images
# print('There are ', len(ims), 'images.')

# Display few images
with sns.axes_style('dark'):
    fig1, ax1 = plt.subplots(2, 2, figsize=(9, 10))
    ax1[0,0].imshow(ims[0], cmap=plt.cm.gray)
    ax1[0,1].imshow(ims[15], cmap=plt.cm.gray)
    ax1[1,0].imshow(ims[30], cmap=plt.cm.gray)
    ax1[1,1].imshow(ims[45], cmap=plt.cm.gray)

### b)

# Initialize list of thresholded images
ims_bw = [None] * len(ims)

# Threshold the images
for i, im in enumerate (ims):
    thresh = skimage.filters.threshold_otsu(im)
    ims_bw[i] = im > thresh

# Take a look at the result
with sns.axes_style('dark'):
    fig2, ax2 = plt.subplots(2, 2, figsize=(9, 10))
    ax2[0,0].imshow(ims_bw[0], cmap=plt.cm.gray)
    ax2[0,1].imshow(ims_bw[15], cmap=plt.cm.gray)
    ax2[1,0].imshow(ims_bw[30], cmap=plt.cm.gray)
    ax2[1,1].imshow(ims_bw[45], cmap=plt.cm.gray)

### c) Show representative image from the stack of images
# (with segmentation overlayed in green)

# Let's pick the iamge [40] to overaly the segmentation
# From README file, the interpixel distance is 64.5 nm
# The scale bar is going to be 10/0.0645 = 155 pixels long.
# It will be inserted in the lower right corner

# Image used and normalized
im = np.copy(ims[40]).astype(float)
im /= im.max()

# Burn scale bar
im[800:810, 400:455] = 1.0

# Build RGB image by stacking grayscale images
im_rgb = np.dstack(3 * [im / im.max()])

# Saturate red channel wherever there are white pixels in thresh image
im_rgb[ims_bw[40], 1] = 1.0

# Show the results
fig3 = plt.figure(3)
with sns.axes_style('dark'):
    plt.imshow(im_rgb)

# The segmentation overshoots the bacteria
# We can try 'adaptive thresholding' on subimages of one image
# We do 51 x 51 array spanning a width of one bacterium, to avoid the issue
# of thresholding within a single bacterium (adaptive thresholding needs
# off-image block size)

# Adaptive thresholding itself returns an array of Booleans

# Initialize list of thresholded images
ims_bw = [None] * len(ims)

# Threshold the images
for i, im in enumerate(ims):
    ims_bw[i] = skimage.filters.threshold_adaptive(im, 51)

# Image to be used and normalized
im = np.copy(ims[40]).astype(float)
im /= im.max()

# Burn scale bar
im[800:810, 400:455] = 1.0

# Build RGB image by stacking grayscale images
im_rgb = np.dstack(3 * [im / im.max()])

# Saturate red channel wherever there are white pixels in thresh image
im_rgb[ims_bw[40], 1] = 1.0

# Show the result
fig4 = plt.figure(4)
with sns.axes_style('dark'):
    plt.imshow(im_rgb)

# The background is now messed up, so pixels that are unity only in both adaptive
# and Otsu thresholding could be included

# Initialize list of thresholded images
ims_bw = [None] * len(ims)

# Threshold the images
for i, im in enumerate(ims):
    thresh_otsu = skimage.filters.threshold_otsu(im)
    im_bw = im > thresh_otsu
    ims_bw[i] = np.logical_and(skimage.filters.threshold_adaptive(im,51), im_bw)

# Image used and normalized
im = np.copy(ims[40]).astype(float)
im /= im.max()

# Burn scale bar
im[800:810, 400:455] = 1.0

# Build RGB image by stacking greyscale images
im_rgb = np.dstack(3 * [im / im.max()])

# Saturate red channel wherever there are white pixels in thresh image
im_rgb[ims_bw[40], 1] = 1.0

# Show the result
fig5 = plt.figure(5)
with sns.axes_style('dark'):
    plt.imshow(im_rgb)

### d) Plotting of the growth curve for the colony

# To get the growth curve, we can plot the total bacterial area on y-axis vs.
# time on x-axis
# To get the total area, we compute the number of bacterial pixels by the pixel
# area, which is (64.5 nm)^2 = 4160.25 nm^2

# We have one frame every 15 min

# Compute pixel area
pixel_area = 0.0645**2

# Get total bacterial areae
bac_area = np.empty(len(ims_bw))
for i, im_bw in enumerate(ims_bw):
    bac_area[i] = im_bw.sum() * pixel_area

# Get time in units of hours
t = 0.25 * np.arange(len(ims_bw))

# Plot the result
# fig6 = plt.figure(6)
plt.plot(t, bac_area, marker='.', linestyle='', markersize=10)
plt.xlabel('time (hours)')
plt.ylabel('bacterial area (µm$^2$)')

### e) Perform the regression on the growth curve

# We assume exponential growth b(t) = b_0 * exp(t/tau)

# Defin the fit function
def exp_growth(t, log_b_0, log_tau):
    """ Exponential growth with log arguments."""
    return np.exp(log_b_0) * np.exp(t/np.exp(log_tau))

# Initial guess
p0 = np.log(np.array([5.0, 12.0]))

# Perform the curve fit
log_p, _ = scipy.optimize.curve_fit(exp_growth, t, bac_area, p0)

# Pull out and print parameters
print("""
b_0 = {0:.2f} sq. µm
 τ = {1:.2f} hours
""".format(*tuple(np.exp(log_p))))

# Generate smooth curve
t_smooth = np.linspace(0, t.max(), 200)
y_smooth = exp_growth(t_smooth, *tuple(log_p))

# Make smooth plot and plot data
fig7 = plt.figure(7)
plt.plot(t_smooth, y_smooth, marker='None', linestyle='-', color='gray')
plt.plot(t, bac_area, marker='.', linestyle='', markersize=10)
plt.xlabel('time (hours)')
plt.ylabel('bacterial area (µm$^2$)')
