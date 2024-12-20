from PIL import Image
import numpy as np


def grayscale2binary(img:np.ndarray, threshold:float = 0.7):
    if(len(img.shape)==3):
        img = img[:,:,1]
    
    if((img.dtype) in (int, np.uint8, np.uint16)):
        img = img/255
    
    (h,w) = img.shape[0:2]

    bin_img = np.zeros((h,w), dtype=np.uint8)

    for index, x in np.ndenumerate(img):
        if x < threshold:
            bin_img[index] = 0
        else:
            bin_img[index] = 1
    return bin_img

def rgb2binary(  img:np.ndarray,
                 threshold_red:float = 0.7,
                 threshold_green:float = 0.7,
                 threshold_blue:float = 0.7):
    
    rgb = np.asanyarray(img)
    r = rgb[:,:,0]
    g = rgb[:,:,1]
    b = rgb[:,:,2]

    r_bin = grayscale2binary(r,threshold_red)
    g_bin = grayscale2binary(g,threshold_green)
    b_bin = grayscale2binary(b,threshold_blue)

    sum = r_bin + g_bin + b_bin
    sum = (sum >= 1.0) * 1.0

    return np.dstack((sum,sum,sum)).astype(np.uint8) * 255

def ycbcr2binary(  img:np.ndarray,
                 threshold_Y:float = 0.7,
                 threshold_Cb:float = 0.7,
                 threshold_Cr:float = 0.7):

    return rgb2binary(img, threshold_Y, threshold_Cb, threshold_Cr)

def openAsBinary( src:str):
    with Image.open(src) as im:
        rgb = np.asanyarray(im)
        b = rgb[:,:,1]
        b3 = np.dstack((b,b,b))
        return b

def transformBinaryImage(img:np.ndarray, transformation:str, kernelSize:int, outOfBorderPixelValue:int=0):
    OUT_OF_BORDER_VALUE = np.uint8(outOfBorderPixelValue)
    if not len(img.shape) == 2 : binImage = img[:,:,1]
    else: binImage = img
     # reduce image dimention to two
    (h,w) = binImage.shape
    processedBinaryImage = np.zeros((h,w), dtype=np.uint8) # check type
    kernelRadius = int((kernelSize-1)/2)
    paddedImage = np.full((h+kernelSize-1,w+kernelSize-1), OUT_OF_BORDER_VALUE, dtype=np.uint8)
    paddedImage[kernelRadius:-kernelRadius,kernelRadius:-kernelRadius] = binImage

    match transformation:
        case 'Dilation':
            paddedImage = paddedImage == 255
            for (x,y), value in np.ndenumerate(binImage):
                if np.any(paddedImage[x:x+kernelSize, y:y+kernelSize]):
                    processedBinaryImage[x,y] = 255
        case 'Erosion':
            paddedImage = paddedImage == 0
            for (x,y), value in np.ndenumerate(binImage):
                if np.any(paddedImage[x:x+kernelSize, y:y+kernelSize]):
                    processedBinaryImage[x,y] = 0
                else:
                    processedBinaryImage[x,y] = 255
        case 'Opening':
            paddedImage_ero = paddedImage == 0
            for (x,y), value in np.ndenumerate(binImage):
                if np.any(paddedImage_ero[x:x+kernelSize, y:y+kernelSize]):
                    processedBinaryImage[x,y] = 0
                else:
                    processedBinaryImage[x,y] = 255

            paddedImage[kernelRadius:-kernelRadius,kernelRadius:-kernelRadius] = processedBinaryImage
            paddedImage_dil = paddedImage == 255
            for (x,y), value in np.ndenumerate(binImage):
                if np.any(paddedImage_dil[x:x+kernelSize, y:y+kernelSize]):
                    processedBinaryImage[x,y] = 255
                else:
                    processedBinaryImage[x,y] = 0
        case 'Closing':
            paddedImage_dil = paddedImage == 255
            for (x,y), value in np.ndenumerate(binImage):
                if np.any(paddedImage_dil[x:x+kernelSize, y:y+kernelSize]):
                    processedBinaryImage[x,y] = 255

            paddedImage[kernelRadius:-kernelRadius,kernelRadius:-kernelRadius] = processedBinaryImage
            paddedImage_ero = paddedImage == 0
            for (x,y), value in np.ndenumerate(binImage):
                if np.any(paddedImage_ero[x:x+kernelSize, y:y+kernelSize]):
                    processedBinaryImage[x,y] = 0
                else:
                    processedBinaryImage[x,y] = 255
        case _:
            pass
    
    return np.dstack((processedBinaryImage,processedBinaryImage,processedBinaryImage))

def HitOrMiss(img:np.ndarray, kernel:np.ndarray, outOfBorderPixelValue:int=0):
    OUT_OF_BORDER_VALUE = np.uint8(outOfBorderPixelValue)
    if not len(img.shape) == 2 : binImage = img[:,:,1]
    else: binImage = img
    (h,w) = binImage.shape
    processedBinaryImage = np.zeros((h,w), dtype=np.uint8)
    kernelSize = kernel.shape[0]
    kernelRadius = int((kernelSize-1)/2)
    paddedImage = np.full((h+kernelSize-1,w+kernelSize-1), OUT_OF_BORDER_VALUE, dtype=np.uint8)
    paddedImage[kernelRadius:-kernelRadius,kernelRadius:-kernelRadius] = binImage

    anyValueKernelMask = kernel == 2 
    for (x,y), value in np.ndenumerate(binImage):
        if np.all((paddedImage[x:x+kernelSize, y:y+kernelSize]==kernel) + anyValueKernelMask):
            processedBinaryImage[x,y] = 255
       
    return np.dstack((processedBinaryImage,processedBinaryImage,processedBinaryImage))

def CombineImages(imgs):
    imgs2d = []

    for img in imgs:
        imgs2d.append(img[:,:,1])
    finalImage = np.zeros(imgs2d[0].shape, dtype=np.uint8)
    for img in imgs2d:
        for (x,y), value in np.ndenumerate(img):
            if value == 255:
                finalImage[x,y] = 255
    return np.dstack((finalImage,finalImage,finalImage))