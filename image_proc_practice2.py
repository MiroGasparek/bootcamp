# 14 July 2018 Miroslav Gasparek
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
        (`int` or `float`) or 'otsu'. If 'otsu', the threshold value will be
        determined automatically using Otsu's thresholding method.
    radius : float
        Radius for gaussian blur for background subtraction. Default value
        is 20.
    image_mode : 'phase' or 'fluorescence'
        Mode of microscopy used to capture the image. If 'phase', objects with
        intensity values *lower* than the provided threshold will be selected.
        If `fluorescence`, values *greater* than the provided threshold will be
        selected. Default value is 'phase'.
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
        raise ValueError("image mode not recognized. Must be 'phase'"
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
        Range of eccentricities in which acceptable objects exist. This should be
        provided on the range of 0 to 1.0.

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
    print(np.sum(im_approved))
    im_filt = skimage.measure.label(im_approved > 0)

    return im_filt


# Load an E. coli test image.
ecoli = skimage.io.imread('data/HG105_images/noLac_phase_0004.tif')

# Using my knowledge of biology, we can draw some bounds.
# Using the information in the problem statement, we know
# the interpixel distance.
ip_dist = 0.0636  # in units of µm per pixel.
area_bounds = (1/ip_dist**2, 10.0/ip_dist**2)
ecc_bounds = (0.8, 1.0)  # they are certainly not spheres.

# Pass all images through our function.
ecoli_seg = cell_segmenter(ecoli, area_bounds=area_bounds, ecc_bounds=ecc_bounds)

# Extract and store the mean and total fluorescence intensities for each cell
# in a single image in an array of pandas DataFrame

# Load the fluorescence image.
ecoli_yfp = skimage.io.imread('data/HG105_images/noLac_FITC_0004.tif')

# Compute the regionproperties of our fluorescence image.
props = skimage.measure.regionprops(ecoli_seg, intensity_image = ecoli_yfp)

# Extract the mean intensities
mean_int = np.array([prop.mean_intensity for prop in props])

# We will start with a simple histogram
f1 = plt.figure(1)
plt.hist(mean_int)
plt.xlabel('mean pixel intensity')
plt.ylabel('count')

# To eliminate the bias, check ethe ECDF.
def ecdf(data):
    """ Compute x, y values for an empirical distribution function."""
    x = np.sort(data)
    y = np.arange(1,len(data)+1) / len(data)
    return x, y

# Compute the ECDF for the glow-y cells.
intensities, ECDF = ecdf(mean_int)

# Plotting
f2 = plt.figure(2)
plt.plot(intensities, ECDF, marker ='.', linestyle='none')
plt.xlabel('intensities')
plt.ylabel('ECDF')

# Define the number of repetitions.
n_reps = 100000

# Initialize the replicates
bootstrap_means = np.empty(n_reps)

# Compute the replicates. Each bootstrap is plotted
for i in range(n_reps):
    resample = np.random.choice(mean_int, replace=True, size=len(mean_int))
    bootstrap_means[i] = np.mean(resample)

# Compute the ECDF
bs_means, bs_ECDF = ecdf(bootstrap_means)

# Plot the ECDF
f3 = plt.figure(3)
plt.plot(bs_means, bs_ECDF, marker='.', linestyle='none')
plt.xlabel('mean of bootstrapped intensities')
plt.ylabel('ECDF')
plt.margins(0.02)

# Compute the 95% confidence interval
percs = np.percentile(bootstrap_means, [97.5, 2.5])
print("""
The 97.5% and the 2.5% of the bootstrapped data are {0:.3f}
and {1:.3f}, respectively.
""".format(percs[0], percs[1]))
