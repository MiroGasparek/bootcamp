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


##### Problem 5.2: Filter, extract, rinse, repeat

# We first copy in the image segmentation functions from the previous
# image processing practice session

def cell_segmenter(im, thresh='otsu', radius=20.0, image_mode='phase',
                   area_bounds=(0,1e7), ecc_bounds=(0, 1)):
    """
    This function segments a given image via thresholding and returns a labeled 
    segmentation mask.
    
    Parameters
    ----------
    im : 2d-array
        Image to be segmented. This may be of either float or
        integer data type.
    thresh : int, float, or 'otsu'
        Value used during thresholding operation. This can either be a value 
        (`int` or `float`) or 'otsu'. If 'otsu', the threshold value will be 
        determined automatically using Otsu's thresholding method.
    radius : float
        Radius for gaussian blur for background subtraction. Default 
        value is 20.
    image_mode : 'phase' or 'fluorescence'
        Mode of microscopy used to capture the image. If 'phase', objects
        with intensity values *lower* than the provided threshold will be
        selected. If `fluorescence`, values *greater* than the provided 
        threshold will be selected. Default value is 'phase'.
    area_bounds : tuple of ints.
        Range of areas of acceptable objects. This should be provided in units 
        of square pixels.
    ecc_bounds : tuple of floats
        Range of eccentricity values of acceptable objects. These values should
        range between 0.0 and 1.0.
        
    Returns
    -------
    im_labeled : 2d-array, int
        Labeled segmentation mask.
    """
     
    # Apply a median filter to remove hot pixels.
    med_selem = skimage.morphology.square(3)
    im_filt = skimage.filters.median(im, selem=med_selem)
   
    # Perform gaussian subtraction
    im_sub = bg_subtract(im_filt, radius)
    
    # Determine the thresholding method.
    if thresh is 'otsu':
        thresh = skimage.filters.threshold_otsu(im_sub)

    # Determine the image mode and apply threshold.
    if image_mode is 'phase':
        im_thresh = im_sub < thresh
    elif image_mode is 'fluorescence':
        im_thresh = im_sub > thresh
    else:
        raise ValueError("image mode not recognized. Must be 'phase' "
                          + " or 'fluorescence'")
       
    # Label the objects.
    im_label = skimage.measure.label(im_thresh)

    # Apply the area and eccentricity bounds. 
    im_filt = area_ecc_filter(im_label, area_bounds, ecc_bounds)
    
    # Remove objects touching the border.
    im_border = skimage.segmentation.clear_border(im_filt, buffer_size=5)
    
    # Relabel the image.
    im_border = im_border > 0 
    im_label = skimage.measure.label(im_border)
    
    return im_label


def bg_subtract(im, radius):
    """
    Subtracts a gaussian blurred image from itself smoothing uneven 
    illumination.
    
    Parameters
    ----------
    im : 2d-array
        Image to be subtracted
    radius : int or float
        Radius of gaussian blur
    
    Returns
    -------
    im_sub : 2d-array, float
        Background subtracted image.
    """
    
    # Apply the gaussian filter.
    im_filt = skimage.filters.gaussian(im, radius)
    
    # Ensure the original image is a float
    if np.max(im) > 1.0:
        im = skimage.img_as_float(im)
    
    im_sub = im - im_filt
    
    return  im_sub


def area_ecc_filter(im, area_bounds, ecc_bounds):
    """
    Filters objects in an image based on their areas.
    
    Parameters
    ----------
    im : 2d-array, int
        Labeled segmentation mask to be filtered. 
    area_bounds : tuple of ints
        Range of areas in which acceptable objects exist. This should be 
        provided in units of square pixels.
    ecc_bounds : tuple of floats 
        Range of eccentricities in which acceptable objects exist.
        This should be provided on the range of 0 to 1.0.
        
    Returns
    -------
    im_relab : 2d-array, int
        The relabeled, filtered image.
    """
 
    # Extract the region props of the objects. 
    props = skimage.measure.regionprops(im)
    
    # Extract the areas and labels.
    areas = np.array([prop.area for prop in props])
    eccs = np.array([prop.eccentricity for prop in props])
    labels = np.array([prop.label for prop in props])

    # Make an empty image to add the approved cells.
    im_approved = np.zeros_like(im)
    
    # Threshold the objects based on area and eccentricity
    for i, _ in enumerate(areas):
        if areas[i] > area_bounds[0] and areas[i] < area_bounds[1]\
            and eccs[i] > ecc_bounds[0] and eccs[i] < ecc_bounds[1]:
                im_approved += im==labels[i]
   
    # Relabel the image.
    im_filt = skimage.measure.label(im_approved > 0)
    return im_filt


# 1) Get list of all of the iamge files in data/HG105_images/

# Define the directory where the iamges are.
data_dir = 'data/HG105_images/'

# List the daat files using os.
files = os.listdir(data_dir)

# Separate images based on phase or fluorescence
# Make empty lists for the phase and fluorescence images.
# phase_ims, fluo_ims = [], []
# 
# # Loop through all of the file names in files and separate them appropriately.
# for _, f in enumerate(files):
#     if 'phase' in f.lower():
#         phase_ims.append(f)
#     if 'fitc' in f.lower():
#         fluo_ims.append(f)
# 
# # Sort both so they are in he same order
# phase_ims.sort()
# fluo_ims.sort()

# Another way to do this separation is to use glob.glob, which returns the list of 
# paths that match a given pattern

# Glob the phase and fluo globs.
phase_glob = glob.glob(data_dir + '*phase*.tif')
fluo_glob = glob.glob(data_dir + '*FITC*.tif')

# Output also gave us entire relative path. This is an important distinction

# Instantiate an empty list for the mean pixel intensity of each cell
mean_ints = []

# Do the same for the areas
areas = []

# Define area and eccentricity bounds for the segmentation function
ip_dist = 0.0636 # in units of um per pixel
area_bounds = (0.5/ip_dist**2, 4/ip_dist**2)
ecc_bounds = (0.8, 1.0)

# Loop through all images
for p, f in zip(phase_glob, fluo_glob):
    # Load the phase image
    phase_im = skimage.io.imread(p)
    
    # Perform the segmentation
    phase_seg = cell_segmenter(phase_im, image_mode='phase',
                                area_bounds=area_bounds, ecc_bounds=ecc_bounds)
    
    # Load the fluoresecence image
    fluo_im = skimage.io.imread(f)
    
    # Compute the region properties
    props = skimage.measure.regionprops(phase_seg, intensity_image=fluo_im)
    
    # Add them to the storage list
    for prop in props:
        mean_ints.append(prop.mean_intensity)
        areas.append(prop.area * ip_dist**2)

# Convert the lsit to mupy arrays for simplicity
mean_ints = np.array(mean_ints)
areas = np.array(areas)

# To check if things work properly
# Convert the phase image to a float and make a copy
phase_float = phase_im / phase_im.max()
phase_float_copy = np.copy(phase_float)

# Mark where the segmentation mask is True on the phase image
phase_float_copy[phase_seg > 0] = 0.8

# Color the segmented cells in red
merge = np.dstack((phase_float_copy, phase_float, phase_float))

# Display image
with sns.axes_style('dark'):
    plt.imshow(merge)
    
# Print the total number of cells 
print("Segmented and analyzed {num} cells!".format(num=len(mean_ints)))

# Look at the ECDFs of the mean intesities and areas
# Define the ECDF function

def ecdf(data):
    """ Compute x, y values for an empirical distribution function."""
    x = np.sort(data)
    y = np.arange(1, len(data)+1) / len(data)
    return x, y

# Generate the ECDFs for the intensities and areas
means_sort, means_ecdf = ecdf(mean_ints)
areas_sort, areas_ecdf = ecdf(areas)

# Plotting 
fig2, ax2 = plt.subplots(1, 2, figsize=(9,5))
ax2[0].plot(means_sort, means_ecdf, '.')
ax2[0].set_xlabel('mean intensities')
ax2[0].set_ylabel('ECDF')
ax2[1].plot(areas_sort, areas_ecdf, '.')
ax2[1].set_xlabel('cell areas (µm$^2$)')

plt.close('all')
# Let's do some bootstrapping 

# Set the number of repetitions
n_rep = 1000000

# Instantiate a vector to hold the bootstrap means
bs_means = np.empty(n_rep)

# Loop through and re-sampe
for i in range(n_rep):
    bs_resample = np.random.choice(mean_ints, replace=True, size=len(mean_ints))
    bs_means[i] = np.mean(bs_resample)

# Let's plot the ECDF
bs_means_sorted, bs_ecdf = ecdf(bs_means)

fig3 = plt.figure(3)
plt.plot(bs_means_sorted, bs_ecdf, '.')
plt.margins(0.02)
plt.xlabel('bootstrapped mean intensities')
plt.ylabel('ECDF')

fig3.show()

# Compute the 97.5% and 2.5% percentiles
percs = np.percentile(bs_means, [2.5, 97.5])

print('95% of our bootstrapped means lie between {0:.2f} and {1:.2f}.'.format(percs[0], percs[1]))