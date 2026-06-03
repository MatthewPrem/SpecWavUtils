import numpy as np
import matplotlib.pyplot as plt
import Util


def display2DSpec(Image, title="", sigmaHigh=5, sigmaLow=1, normalize = False, w0=1.16236340e+04, a0=1.33788072e-01):
    """
    Function for displaying a 2D model spectrum.

    Args:
        Image(2D array): The intensity data that you wish to display.
        title(string, optional): The title that will be given to the drawn plot. Default: Empty string (no title).
        sigmaHigh(float, optional): The high cut point for the linear remapping stretch that will be applied. Given in standard deviations away from the median value. Default: 5
        sigmaLow(float, optional): The low cut point for the linear remapping steetcht that will be applied. Given in standard deviations away from the median value. Default: 1
        normalize(boolean, optional): Should the image be normalized between the minimum and maximum values instead of having a standard deviation-derived linear stretch? Default: False. If set to True, the sigma parameters are ignored.
        w0(float, optional): The wavelength of the first pixel in Angstroms. If not given, defaults to value for vph300 HK.
        a0(float, optional): The linear scale factor in pixels per Angstrom. If not given, defaults to value for vph300 HK.
    """
    plt.figure()
    maxWav = w0+Image.shape[1]/a0#+Image.shape[0]**2*parameters["wB"]+Image.shape[0]**3*parameters["wC"]
    if normalize:
        norm = Image/np.max(Image[np.logical_not(np.isnan(Image))])
        image = plt.imshow(norm, vmin=0, vmax=1, interpolation="nearest", extent=[w0, maxWav, 0, Image.shape[0]])
    else:
        middle = np.median(Image)
        stdev = np.std(Image)
        vMax = np.max(Image)
        vMin = np.min(Image)
        if sigmaHigh > 0:
            vMax = middle+sigmaHigh*stdev
        if sigmaLow > 0:
            vMin=middle-sigmaLow*stdev
        image = plt.imshow(Image, vmin=vMin, vmax=vMax, interpolation="nearest", extent=[w0, maxWav, 0, Image.shape[0]])
    plt.colorbar(image)
    plt.xlabel("Spectral position (Angstroms)")
    plt.ylabel("Spatial position (Px)")
    plt.title(title)
    plt.gca().set_aspect("auto")
    plt.tight_layout()

def flipX(image):
    """
    Utility function to mirror an image along its X-direction (across the Y-axis). The argument is modified in-place.

    Args:
        image(2D array): The image data to be flipped.
    """
    for i in range(len(image[0])//2):
        tmp = np.copy(image[:,i])
        image[:,i] = image[:,-i-1]
        image[:,-i-1] = tmp

def flipY(image):
    """
    Utility function to mirror an image along its Y-direction (across the X-axis). The argument is modified in-place.

    Args:
        image(2D array): The image data to be flipped.
    """
    for i in range(len(image)//2):
        tmp = np.copy(image[i,:])
        image[i,:] = image[-i-1,:]
        image[-i-1,:] = tmp

def cropImage(data, y, x, height, width):
    """
    Utility function to crop an image. The result is returned as a data view to the sub-section of the original array.

    Args:
        data(2D array): The image data to be cropped.
        y(int): The starting row of the crop (the top when visualizing)
        x(int): The starting column of the crop (the left when visualizing)
        height(int): The height of the cropped image in pixels.
        width(int): The width of the cropped image in pixels.
    """
    return data[y:y+height,x:x+width]