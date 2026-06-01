import numpy as np
import matplotlib.pyplot as plt
import Util


def displayModel(Image, title="", sigmaHigh=5, sigmaLow=1, normalize = False, w0=1.16236340e+04, a0=1.33788072e-01, mode=None):
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