import numpy as np
import matplotlib.pyplot as plt
import Util
from scipy.interpolate import CubicSpline

def wavToPixel(wavelength, w0=1.16236340e+04, a0=1.33788072e-01, round=True):
    if not round:
        return (wavelength-w0)*a0
    else:
        return int(np.round((wavelength-w0)*a0))
def pixelToWav(pixel, w, a):
    return pixel/a+w
    
def absResid(data, model):
    return np.sum(np.abs(data-model))

def calcModel(lines, arrLen, w0, s, width=2.5, offset=0, power=5):
    model=np.zeros(arrLen)
    xs = np.arange(0, arrLen)
    for l in lines:
        x0 = wavToPixel(l[1], w0, a0=s)
        model += LorentzLine(xs, x0, l[4], 2.5, 0, 5)
    return model

def updateLinearFit(event, updatefig, line, lines, model):
    model *= 0
    xs = np.arange(0, len(model))
    for l in lines:
        x0 = wavToPixel(l[1], w0=event.ydata, a0=event.xdata)
        model += LorentzLine(xs, x0, l[4], 2.5, 0, 5)
    line.set_ydata(model/np.max(model))
    updatefig.canvas.draw()
    updatefig.canvas.flush_events()

def calcLinearFit(data, lines, minW0, maxW0, minScale, maxScale, resW = 200, resS = 200, viewPlots = True):
    params = np.zeros((int(resW), int(resS)))
    xs = np.arange(0, len(data))
    ws = np.linspace(minW0, maxW0, int(resW))
    ses = np.linspace(minScale, maxScale, int(resS))
    for w in range(len(ws)):
        for s in range(len(ses)):
            model = np.zeros_like(data)
            for l in lines:
                x0 = wavToPixel(l[1], w0=ws[w], a0=ses[s])
                model += LorentzLine(xs, x0, l[4], 2.5, 0, 5)
            params[w,s] = absResid(data/np.max(data), model/np.max(model))
    loc = np.argmin(params)
    wBest = ws[loc//resS]
    sBest = ses[loc%resS]
    if viewPlots:
        fig1, ax1 = plt.subplots(1,1)
        mask = np.logical_not(np.isnan(params))
        img = ax1.imshow(params, vmin=np.min(params[mask]), vmax=np.max(params[mask]), extent=[minScale, maxScale, maxW0, minW0])
        fig1.colorbar(img)
        ax1.plot(sBest, wBest, "rx")
        ax1.set_xlabel("Scale value (Pixels/Angstrom)")
        ax1.set_xlabel("Starting wavelength (A)")
        ax1.set_aspect("auto")

        fig2, ax2 = plt.subplots(1,1)
        ax2.plot(data/np.max(data), label="data")
        model = np.zeros_like(data)
        for l in lines:
            x0 = wavToPixel(l[1], w0=wBest, a0=sBest)
            model += LorentzLine(xs, x0, l[4], 2.5, 0, 5)
        line, = ax2.plot(model/np.max(model), label="model")
        ax2.legend()
        ax2.set_xlabel("Wavelength (A)")
        ax2.set_ylabel("Normalized Intensity")
        cid = fig1.canvas.mpl_connect('button_press_event', lambda e: updateLinearFit(e, fig2, line, lines, model))


    
    return wBest, sBest 


def continuum(I, medRange=20, thresh=7, maxRun=10, debug=False):
    res = I[1:]-I[0:-1]
    res[0:-1] = (res[0:-1] + res[1:])/2 #blur somewhat to increase SNR
    inc = res>thresh
    dec = res<-thresh
    plateau = np.logical_and(res<thresh, res>-thresh)

    contMask = np.logical_not(np.isnan(res))
    rising = False
    runLength = 0
    for i in range(len(res)):
        if inc[i]:
            contMask[i]=False
            rising=True
            runLength=0
        if dec[i]:
            contMask[i]=False
            rising=False
        if rising:
            contMask[i]=False
            runLength+=1
            if runLength>maxRun:
                rising=False
    
    med = I[:-1][contMask]
    tmp = np.copy(med)
    for i in range(len(med)):
        med[i] = np.median(tmp[np.max([0,i-medRange]):np.min([len(med)-1,i+medRange])])

    index = np.arange(len(I)-1)
    interp = CubicSpline(index[contMask], med)

    if debug:
        fig, ax = plt.subplots(3,1, figsize=(6,7))
        
        ax[0].plot(index,I[:-1], ".")
        ax[1].plot(index[plateau],res[plateau], ".", color="black")
        ax[1].plot(index[inc],res[inc], ".", color="blue")
        ax[1].plot(index[dec],res[dec], ".", color="red")
        ax[1].plot(index[contMask],res[contMask], ".", color="green")
        ax[2].plot(index[contMask], I[:-1][contMask])
        ax[2].plot(index[contMask], med)
        ax[2].plot(index, interp(index))
    return interp
    
def convert2Dto1D(data2D, y1, y2):
    return np.average(data2D[y1:y2,:], axis=0)

def gaussLine(x, pos, A, width, offset, power):
    return A*np.exp(-np.abs(x-pos)**power/(width**power))+offset

def gaussWidthToFWHM(width, power):
    return 2*width*(-np.log(1/2))**(1/power)

def LorentzLine(x, pos, A, width, offset, power):
    return A/(1+np.abs((x-pos)/width)**power)+offset

def LorentzWidthToFWHM(width):
    return 2*width

