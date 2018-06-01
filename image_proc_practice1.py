# 01 June 2018 Miroslav Gasparek
# Python bootcamp, lesson 40: Image processing practice with Python

# Import modules
import numpy as np

import matplotlib.pyplot as plt

import scipy.ndimage
import skimage.io
import skimage.segmentation
import skimage.morphology

# Import some pretty Seaborn settings
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)


### Practice 1
# Writing custom segmentation function

# Requirements:
#   1. Correct for "hot" or "bad" pixels in an image.
#   2. Correct for uneven illumination.
#   3. Perform a thresholding operation.
#   4. Remove bacteria or objects near/touching the image border.
#   5. Remove objects that are too large (or too small) to be bacteria.
#   6. Remove improperly segmented cells.
#   7. Return a labeled segmentation mask.

####
def cell_segmenter(im, thresh='otsu', radius=20.0, image_mode='phase',
                    area_bounds=(0,1e7), ecc_bounds=(0, 1)):
    """
    This function segments a given image via thresholding and returns
    a labeled segmentation mask.

    Parameters
    ----------
    im : 2d-array
        Image to be segmented. This may be of either float or integer
        data type.
    thresh : int, float, or 'otsu'
        Value used during thresholding operation. This can either be a value
        ('int' or 'float') or 'otsu', the threshold value will be
        determined automatically using Otsu's thresholding method.
    radius : float
        Radius for gaussian blur for background subtractino. Default value
        is 20.
    image_mode : 'phase' or 'fluorescence'
        Mode of microsocopy used to capture the image. If 'phase', objects with
        intensity values *lower* than the provided threshold will be selected.
        If 'fluorescence', values *greater* than the provided threshold will be
        selected. Default value is 'phase'.
    area_bounds : tuple of ints.
        Range of areas of acceptable objects. This should be probided in units
        of square pixels.
    eec_bounds : tuple of floats
        Range of eccentricity values of acceptable objects. These values should
        range between 0.0 and 1.0.

    Returns
    -------
    im_labeled : 2d-array, int
        Labeled segmentation mask.
    """

    # Apply a median filter to remove hot pixels
    med_selem = skimage.morphology.square(3)
    im_filt = skimage.filters.median(im, selem=med_selem)

    # Perform gaussian subtraction
    im_sub = bg_subtract(im_filt, radius)

    # Determine the thresholding method
    if thresh is 'otsu':
        thresh = skimage.filters.threshold_otsu(im_sub)

    # Determine the image mode and apply threshold
    if image_mode is 'phase':
        im_thresh = im_sub < thresh
    elif image_mode is 'fluorescence':
        im_thresh = im_sub > thresh
    else:
        raise ValueError("Image mode not recognized. Must be 'phase'"
                         + "or 'fluorescence'.")
    # Label the objects
    im_label = skimage.measure.label(im_thresh)

    # Apply the area and eccentricity bounds
    im_filt = area_ecc_filter(im_label, area_bounds, ecc_bounds)

    # Remove objects touching the border
    im_border = skimage.segmentation.clear_border(im_filt, buffer_size=5)

    # Relabel the image
    im_border = im_border > 0
    im_label = skimage.measure.label(im_border)

    return im_label

def bg_subtract(im, radius):
    """
    Subtracts a gaussian blurred image from itself, smoothing uneven
    illumination.

    Parameters
    -----------
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

    return im_sub

def area_ecc_filter(im, area_bounds, ecc_bounds):
    """
    Filters objects in an image, based on their areas.

    Parameters
    ----------
    im : 2d-array, int
        Labeled segmentation mask to be filtered.
    area_bounds : tuple of ints
        Range of areas in which acceptable objects exist. This should be
        provided in units of square pixels.
    ecc_bounds : tuple of floats
        Range of eccentricities in which acceptable objects exist. This should be
        provided on the range of 0 to 1.0.

    Returns
    --------
    im_relab : 2d-array, list
        The relabeled, filtered image.
    """

    # Extract the region props of the objects
    props = skimage.measure.regionprops(im)

    # Extract the areas and labels
    areas = np.array([prop.area for prop in props])
    eccs = np.array([prop.eccentricity for prop in props])
    labels = np.array([prop.label for prop in props])

    # Make an empty image to add the approved cells
    im_approved = np.zeros_like(im)

    # Threshold the objects based on area and eccentricity
    for i, _ in enumerate(areas):
        if areas[i] > area_bounds[0] and areas[i] < area_bounds[1]\
            and eccs[i] > ecc_bounds[0] and eccs[i] < ecc_bounds[1]:
                im_approved += im==labels[i]

    # Relabel the image
    print(np.sum(im_approved))
    im_filt = skimage.measure.label(im_approved > 0)

    return im_filt

# A few functions were used to keep the code modular
# Filtering functions will make application of area and eccentricity bounds
# easier especially if they are ato be used in the future

# Function 'cell_segmenter()' calls the two filtering functions we wrote above

# Try the functions out
ecoli = skimage.io.imread('data/HG105_images/noLac_phase_0004.tif')
bsub_phase = skimage.io.imread('data/bsub_100x_phase.tif')
bsub_fluo = skimage.io.imread('data/bsub_100x_cfp.tif')

# Using the knowledge of biology, some bounds can be drawn
# Using the information in the problem statement, we know
# the interpixel distance
ip_dist = 0.0636 # in units of microns per pixel
area_bounds = (1/ip_dist**2, 10.0/ip_dist**2)
ecc_bounds = (0.8, 1.0) # they are certainly not spheres

# Pass all images through the function
ecoli_seg = cell_segmenter(ecoli, area_bounds=area_bounds, ecc_bounds=ecc_bounds)
bsub_phase_seg = cell_segmenter(bsub_phase, image_mode='phase',
                                area_bounds=area_bounds, ecc_bounds=ecc_bounds)
bsub_fluo_seg = cell_segmenter(bsub_fluo, image_mode='fluorescence',
                                area_bounds=area_bounds, ecc_bounds=ecc_bounds)

# We can make merged images to see how well the objects were segemented
# This would be hard to see on the Bacillus fluorescence image directly, so
# we will take a look at the fluorescence segmentation on the corresponding
# phase image

# Make the two phase images as floates and copy them
ecoli_float = ecoli / ecoli.max()
bsub_float = bsub_phase / bsub_phase.max()
ecoli_copy = np.copy(ecoli_float)
bsub_copy = np.copy(bsub_float)
bsub_copy2 = np.copy(bsub_float)

# Mark the segmented bacteria on the copied images
ecoli_copy[ecoli_seg > 0] = 0.8
bsub_copy[bsub_phase_seg > 0] = 0.8
bsub_copy2[bsub_fluo_seg > 0] = 0.8

# Merge them into RGB images
ecoli_merge = np.dstack((ecoli_copy, ecoli_float, ecoli_float))
bsub_phase_merge = np.dstack((bsub_copy, bsub_float, bsub_float))
bsub_fluo_merge = np.dstack((bsub_copy2, bsub_float, bsub_float))

# Plot the images
with sns.axes_style('dark'):
    fig, ax = plt.subplots(3, 1, figsize=(5,9))
    ax[0].imshow(ecoli_merge)
    ax[0].set_title('E. coli phase segmentation')
    ax[1].imshow(bsub_phase_merge)
    ax[1].set_title('B. subtilis phase segmentation')
    ax[2].imshow(bsub_fluo_merge)
    ax[2].set_title('B. subtilis fluorescence segmentation')
    plt.tight_layout()
