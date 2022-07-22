# histogram specification
import numpy as np
import cv2
import sys
from matplotlib import pyplot as plt
import time as time
import os

startTime = time.time()


def NormCDF(inCDF):
    cdf = inCDF
    cdf_m = np.ma.masked_equal(cdf,0)
    cdf_m = 255*((cdf_m - cdf_m.min())/float((cdf_m.max()-cdf_m.min())))
    cdf = np.ma.filled(cdf_m,0).astype('uint8')
    return cdf

def MakeHist(vector, bins):
    hist = np.copy(bins)
    hist = np.array(hist, dtype=float)
    for val in bins:
        hist[val] = vector[vector == val].shape[0]/float((vector.shape[0]))
    return hist


def ComputeHistogramSpecification(SourceData, DestData, histBins, name=''):
    # this code will attempt to map SourceHist onto DestHist
    # it does this baed on Histogram Specification looking for the 
    # optimal lookup within the CDF of each
    # it takes as input a stack of SourceData and DestData, and histBins
    
    SourceData = 255.*((SourceData - SourceData.min())/ float((SourceData.max() - SourceData.min())))
    DestData = 255.*((DestData - DestData.min())/ float((DestData.max() - DestData.min())))
    SourceData = np.rint(SourceData)
    DestData = np.rint(DestData)
    levels = histBins

    # take a random sample of N values from the original source data
    # from with the histogram matching is performed.
    # this dramatically reduces computation time 
    SampleSize = 10000
    SourceSample = np.random.choice(SourceData,SampleSize)
    DestSample = np.random.choice(DestData, SampleSize)
    SourceHist = MakeHist(SourceSample, histBins)
    DestHist = MakeHist(DestSample, histBins)
    # SourceHist = MakeHist(SourceData, histBins)
    # DestHist = MakeHist(DestData, histBins)
    elapsedTime = (time.time() - startTime)
    # print '    %.3f seconds elapsed make first Hist'%elapsedTime

    # compute the CDFs
    SourceCDF = []
    DestCDF = []
    nPixels = float(sum(SourceHist))
    for k in range(1, len(levels)+1):
        SourceCDF.append(float(sum(SourceHist[:k])) / nPixels)
        DestCDF.append(float(sum(DestHist[:k])) / nPixels)
    SourceCDF = np.array(SourceCDF)
    DestCDF = np.array(DestCDF)
    SourceCDF = NormCDF(SourceCDF)
    DestCDF = NormCDF(DestCDF)
    elapsedTime = (time.time() - startTime)
    # print '    %.3f seconds elapsed get CDFs'%elapsedTime

    counter = 0
    newMapping = []
    for i in SourceCDF:
        limitLevels = np.abs(DestCDF - i)
        newLevel = np.argmin(limitLevels)
        newMapping.append(newLevel)
        counter += 1
    mappingLookup = np.vstack((levels, newMapping)).T 
    # print '\n Mapping Lookup'
    # print mappingLookup
    elapsedTime = (time.time() - startTime)
    # print '    %.3f seconds elapsed get Mapping'%elapsedTime

    # apply the mapping to the hist
    newHist = []
    for k in levels:
        lookupVal = mappingLookup[(mappingLookup[:,1] == k)][:,0]
        mappedvals = SourceHist[lookupVal]
        mappedSum = np.sum(mappedvals)
        newHist.append(mappedSum)
    newHist = np.array(newHist)
    elapsedTime = (time.time() - startTime)
    # print '    %.3f seconds elapsed make new hist'%elapsedTime

    # compute the CDFs
    newCDF = []
    for k in range(1, len(levels)+1):
        newCDF.append(float(sum(newHist[:k])) / nPixels)
    newCDF = np.array(newCDF)
    newCDF = NormCDF(newCDF)
    elapsedTime = (time.time() - startTime)
    # print '    %.3f seconds elapsed make new CDF'%elapsedTime

    #show Hist Error
    histError = 100*(newHist - DestHist)/nPixels
    elapsedTime = (time.time() - startTime)
    # print '    %.3f seconds elapsed compute error'%elapsedTime

    #attempt to use the new mappings to correct the original data
    newData = np.copy(SourceData)
    for row in mappingLookup:
        newData[SourceData == row[0]] = row[1]
    FinalHist = MakeHist(newData, histBins)
    elapsedTime = (time.time() - startTime)
    # print '    %.3f seconds elapsed final mapping'%elapsedTime
    # All the plotting fun!
    # # plot the histograms
    # # build the figure
    fig, axes = plt.subplots(nrows=6, ncols=1, figsize=(5,8))
    fig.subplots_adjust(hspace=0.6)
    axes[0].plot(levels, SourceHist, 'b')
    axes[0].plot(levels, DestHist, 'r')
    axes[0].set_title('Original Histograms')
    axes[1].plot(levels, SourceCDF, 'b')
    axes[1].plot(levels, DestCDF, 'r')
    axes[1].set_title('Original CDFs')
    axes[2].plot(levels, newHist, 'b')
    axes[2].plot(levels, DestHist, 'r')
    axes[2].set_title('Matched Histogram')
    axes[3].plot(levels, newCDF, 'b')
    axes[3].plot(levels, DestCDF, 'r')
    axes[3].set_title('Matched CDFs')
    axes[4].plot(levels, histError, 'k-')
    axes[4].set_title('Histogram Error Percent')
    axes[5].plot(levels, FinalHist, 'b')
    axes[5].plot(levels, DestHist, 'r')
    axes[5].set_title('Remapped Histogram')
    # plt.show()
    # fig.savefig('HistSpec_v1_%s.PNG'%name, dpi=150)

    return newData, fig

def ImageTransform(input1, input2, destOutput, reflectance_target = 'no'):
    if reflectance_target == 'no':
        img1 = cv2.imread(input1)
        img2 = cv2.imread(input2)
        img1HSV = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        h1,s1,v1 = cv2.split(img1HSV)
        v1 = v1.ravel()

        img2HSV = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        h2,s2,v2 = cv2.split(img2HSV)
        v2 = v2.ravel()

        elapsedTime = (time.time() - startTime)
        # print '%.3f seconds elapsed setup'%elapsedTime

        histBins = range(256)

        SourceData = v1  # is the first one that will be changed
        DestData = v2     # is the second that gets changed into
        v1_new, fig_v1 = ComputeHistogramSpecification(SourceData, DestData, histBins)
        # outfig3 = sys.argv[1].split('.JPG')[0] + '_hist_HSV_V.PNG'
        # fig_v1.savefig(outfig3, dpi=150)
        elapsedTime = (time.time() - startTime)
        # print '%.3f seconds elapsed v1'%elapsedTime

        v1_new = v1_new.reshape((img2.shape[0], img2.shape[1]))

        HSV1_new = img1HSV.copy()
        HSV1_new[:,:,2] = v1_new
        BGR1_new = cv2.cvtColor(HSV1_new, cv2.COLOR_HSV2BGR)
    
        if ".JPG" in os.path.basename(input1):
            outName = destOutput + os.path.basename(input1).split('.JPG')[0] + '_HSV_V_fixed.JPG'

        if ".tif" in os.path.basename(input1):
            outName = destOutput + os.path.basename(input1).split('.tif')[0] + '_HSV_V_fixed.tif'

        cv2.imwrite(outName, BGR1_new,[int(cv2.IMWRITE_JPEG_QUALITY),100])

    if reflectance_target == 'yes':
        img1 = cv2.imread(input1)
        img1HSV = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        BGR1_new = cv2.cvtColor(img1HSV, cv2.COLOR_HSV2BGR)
        if ".JPG" in os.path.basename(input1):
            outName = destOutput + os.path.basename(input1).split('.JPG')[0] + '_HSV_V_fixed.JPG'
        if ".tif" in os.path.basename(input1):
            outName = destOutput + os.path.basename(input1).split('.tif')[0] + '_HSV_V_fixed.tif'
        cv2.imwrite(outName, BGR1_new,[int(cv2.IMWRITE_JPEG_QUALITY),100])
        

    elapsedTime = (time.time() - startTime)
    # print '%.3f seconds elapsed total'%elapsedTime
    
if __name__ == '__main__':
    ImageTransform(sys.argv[1], sys.argv[2], sys.argv[3],sys.argv[4])





