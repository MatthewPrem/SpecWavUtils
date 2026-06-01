import numpy as np
import pandas as pd

def createLineList(path, writePath=None, mergedLines = ["Hg", "Kr", "Ar", "Xe"], minAmp = 100, minWav = 14000, maxWav=26000):
    data = pd.read_csv(path, delimiter=" ")
    retData = []
    for row in range(len(data)):
        if (data.values[row][1] < minAmp or data.values[row][0] < minWav or data.values[row][0] > maxWav):
            continue
        ion = data.values[row][3][0:2]
        if ion in mergedLines:
            retData.append([f"{ion}I",data.values[row][0],1,data.values[row][2],data.values[row][1],data.values[row][3]])

    if writePath is not None:
        with open(writePath, mode="w") as file:
            file.write(f"| ion |      wave | NIST | Instr | amplitude |       Source |\n")
            text = ""
            for i in range(len(retData)):
                text += f"| {retData[i][0]} | {retData[i][1]:>9.3f} |    1 |{retData[i][3]:>6.0f} | {retData[i][4]:>9.1f} | {retData[i][5]} |\n"
            file.write(text)
    return retData

def loadLineList(path, minIntensity=1):
    dat = pd.read_csv(path, delimiter="|")
    mask = dat.values[:,5]>minIntensity
    return np.array([(dat.values[:,2])[mask], (dat.values[:,5])[mask]])

def flipX(image):
    for i in range(len(image[0])//2):
        tmp = np.copy(image[:,i])
        image[:,i] = image[:,-i-1]
        image[:,-i-1] = tmp

def cropImage(data, y, x, height, width):
    return data[y:y+height,x:x+width]