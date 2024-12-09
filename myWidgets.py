from PIL import ImageTk
import PIL
import PIL.Image
import numpy as np
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askopenfilename
import utils
import copy
from dataclasses import dataclass



class KernelPickerGrid(Canvas):
    KERNEL_SELECTOR_CELL_SIZE = 20
    KERNEL_SELECTOR_CELL_PADDING = int(KERNEL_SELECTOR_CELL_SIZE*0.1)
    CANVAS_BACKGROUND_COLOR = 'gray50'
    
    def __init__(self, parent, gridSize, **kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.config(background=self.CANVAS_BACKGROUND_COLOR)

        self.gridSize = gridSize
        self.gridArray = np.full((self.gridSize,self.gridSize), 2, dtype=np.uint8)
        
        
        self.bind('<Button-1>', self.selectCell)

        self.resize(self.gridSize)
    
    def selectCell(self,event):
        # 255 -> 1
        # 0 -> 0
        # 2 -> any
        x=int(event.x / self.KERNEL_SELECTOR_CELL_SIZE)
        y=int(event.y / self.KERNEL_SELECTOR_CELL_SIZE)
        if x >= self.gridSize or y >= self.gridSize: return

        match self.gridArray[x,y]:
            case 2:
                self.gridArray[x,y]=255
            case 255:
                self.gridArray[x,y]=0
            case 0:
                self.gridArray[x,y]=2
        self.drawGrid()

    def resize(self, newGridSize):
        newSize = self.KERNEL_SELECTOR_CELL_SIZE * newGridSize
        self.gridSize = newGridSize
        self.gridArray = np.full((self.gridSize,self.gridSize), 2, dtype=np.uint8)
        self.config(width=newSize+1, height=newSize+1)
        self.drawGrid()
    
    def drawGrid(self):
        self.delete("all")
        middle = int((self.gridSize-1)/2)
        for (x,y), v in np.ndenumerate(self.gridArray):
            cell_start_x = int(x * self.KERNEL_SELECTOR_CELL_SIZE)
            cell_start_y = int(y * self.KERNEL_SELECTOR_CELL_SIZE)

            rec_start_x = cell_start_x + self.KERNEL_SELECTOR_CELL_PADDING + 1
            rec_start_y = cell_start_y + self.KERNEL_SELECTOR_CELL_PADDING + 1
            rec_end_x = rec_start_x + self.KERNEL_SELECTOR_CELL_SIZE - self.KERNEL_SELECTOR_CELL_PADDING
            rec_end_y = rec_start_y + self.KERNEL_SELECTOR_CELL_SIZE - self.KERNEL_SELECTOR_CELL_PADDING
            selected_1 = v == 255
            selected_0 = v == 0

            self.create_rectangle(  rec_start_x, rec_start_y, rec_end_x, rec_end_y,
                                    fill= 'white' if selected_1 else 'black' if selected_0 else self.CANVAS_BACKGROUND_COLOR,
                                    width=1)
            if((x,y) == (middle, middle)):
                self.create_oval(rec_start_x+2, rec_start_y+2, rec_end_x-2, rec_end_y-2,
                                 outline='red')

    def getKernel(self):
        return self.gridArray

class BinaryImageProcessingMainFrame(ttk.Frame):

    @dataclass
    class HistoryElement:
        label: ttk.Label
        transformName: str
        img: PIL.Image


    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        # history
        self.appliedTransforms = []

        # variables
        self.customKernelSize = StringVar()
        self.customKernelSize.set('3')
        self.transformationKernelSize = StringVar()
        self.transformationKernelSize.set('3')

        transformations = ('Dilation', 'Erosion', 'Opening', 'Closing') # 'Thinning', 'Thickening'
        self.choosenTransform = StringVar()

        # widgets 
        imgFrame = ttk.Frame(self, padding=10)
        optFrame = ttk.Frame(self, padding=10)
        historyBaseFrame = ttk.Frame(self, padding=10)
        self.historyFrame = ttk.LabelFrame(historyBaseFrame, text='history')

        selectFileButton = ttk.Button(optFrame, text="Select image", command=self.chooseImageFile)
        standardTransformationFrame = ttk.LabelFrame(optFrame, text="classic transformations", padding=10)
        transformationSizeInfoLabel = ttk.Label(standardTransformationFrame, text='Kernel size:')
        transformationSizeSpinbox = ttk.Spinbox(standardTransformationFrame, from_=3, to=15, increment=2, textvariable=self.transformationKernelSize)
        transformationsCombobox = ttk.Combobox(standardTransformationFrame, textvariable=self.choosenTransform, state= "readonly",takefocus=False)
        transformationsCombobox['values'] = transformations
        transformationApplyButton = ttk.Button(standardTransformationFrame, text='Apply', command=self.transform)

        customKernelChoiseFrame = ttk.Labelframe(optFrame, text="Hit-or-Miss" ,padding=10)
        customKernelSizeSpinbox = ttk.Spinbox(customKernelChoiseFrame, from_=3, to=15, increment=2, textvariable=self.customKernelSize, command=self.changeSize)
        self.customKernelChoiseGrid = KernelPickerGrid(customKernelChoiseFrame, 3)
        customKernelApplyButton = ttk.Button(customKernelChoiseFrame, text='Apply', command=self.transformCustom)
        infoLabel = ttk.Label(optFrame, text="black = 0\nwhite = 1")

        self.imgLabel = ttk.Label(imgFrame, text='No image to display')
        self.imgLabel.pack()

        historyGoBackButton = ttk.Button(historyBaseFrame, text="Undo", command=self.undoTransformation)

        # widgets layout 
        imgFrame.grid(column=0, row=0)
        optFrame.grid(column=1, row=0, sticky=N)
        historyBaseFrame.grid(column=2, row=0, sticky=N)
        


        infoLabel.grid(column=0,row=0)
        selectFileButton.grid(column=0, row=1)
        standardTransformationFrame.grid(column=0, row=2, sticky=W)
        transformationsCombobox.grid(column=0,row=0)
        transformationSizeInfoLabel.grid(column=0, row=1)
        transformationSizeSpinbox.grid(column=0,row=2)
        transformationApplyButton.grid(column=0,row=3)
        customKernelChoiseFrame.grid(column=0,row=3)
        customKernelSizeSpinbox.grid(column=0, row=0, sticky=W)
        self.customKernelChoiseGrid.grid(column=0,row=1)
        customKernelApplyButton.grid(column=0,row=2)
        
        historyGoBackButton.grid(column=0,row=0, sticky=N)
        self.historyFrame.grid(column=0,row=1, sticky=N)
        

        self.imgLabel.grid(column=0, row=0)



    ########## widget functions ##########

    def changeSize(self, *args):
        newGridSize = int(self.customKernelSize.get())
        self.customKernelChoiseGrid.resize(newGridSize)

    def chooseImageFile(self, *args):
        filename = askopenfilename()
        try:
            pilImg = PIL.Image.open(filename)
            img = ImageTk.PhotoImage(pilImg)
        except:
            return
        self.setImage(img, pilImg, "Image loaded")
    
    def setImage(self, img, pilImage, log="Transform"):
        self.pilImage = pilImage
        self.imgLabel.config(image=img)
        self.imgLabel.image=img
        self.addToHistory(log,self.pilImage)
    
    def transform(self):
        kernelSize = int(self.transformationKernelSize.get())
        transformedImage = utils.transformBinaryImage(np.asanyarray(self.pilImage),
                                                                    self.choosenTransform.get(),
                                                                    kernelSize)
        pilImg = PIL.Image.fromarray(transformedImage)
        self.setImage(ImageTk.PhotoImage(pilImg), pilImg, self.choosenTransform.get() + f" {kernelSize}x{kernelSize}")
    
    def transformCustom(self):
        kernel = self.customKernelChoiseGrid.getKernel()
        transformedImage = utils.HitOrMiss(np.asanyarray(self.pilImage),kernel=kernel)
        pilImg = PIL.Image.fromarray(transformedImage)
        kernel.shape[0]
        self.setImage(ImageTk.PhotoImage(pilImg), pilImg, f"Hit-or-Miss {kernel.shape[0]}x{kernel.shape[0]}")    
    
    def addToHistory(self, transformName, img):
        label = ttk.Label(self.historyFrame, text=f"{len(self.appliedTransforms)+1}. {transformName}")
        label.pack(side="top", fill="x")
        self.appliedTransforms.append(self.HistoryElement(label, transformName, img))
    
    def undoTransformation(self):
        if len(self.appliedTransforms) > 1:
            tmp = self.appliedTransforms.pop()
            self.pilImage = self.appliedTransforms[-1].img
            img = ImageTk.PhotoImage(self.pilImage)
            self.imgLabel.config(image=img)
            self.imgLabel.image=img
            tmp.label.destroy()






class ColorToBinaryConversionFrame(ttk.Frame):
    COLOR_CHANNEL_SCALE_LENGTH = 100
    COLOR_CHANNEL_DEFAULT_VALUE = 0.7

    def __init__(self, parent, imgProcessingFrame:BinaryImageProcessingMainFrame, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.imgProcessingFrame = imgProcessingFrame

        # variables
        self.isImageLoaded = False
        self.colorModels = ('RGB', 'YCbCr')
        self.colorModelsInfo = {'RGB':('R','G','B'), 'YCbCr':('Y', 'Cb', 'Cr')}
        self.colorModelsVar = StringVar()
        self.channel_1_value = StringVar()
        self.channel_2_value = StringVar()
        self.channel_3_value = StringVar()
        self.colorModelsVar.set(self.colorModels[0])        
        self.channel_1_value.set(self.COLOR_CHANNEL_DEFAULT_VALUE)
        self.channel_2_value.set(self.COLOR_CHANNEL_DEFAULT_VALUE)
        self.channel_3_value.set(self.COLOR_CHANNEL_DEFAULT_VALUE)

        # widgets 
        imgFrame = ttk.Frame(self, padding=10)
        optFrame = ttk.Frame(self, padding=10)
        selectFileButton = ttk.Button(optFrame, text="Select image", command=self.chooseImageFile)
        self.imgLabel = ttk.Label(imgFrame, text='No image to display')
        conversionControlFrame = LabelFrame(optFrame, text='Colors')

        colorModelCombobox = ttk.Combobox(conversionControlFrame, textvariable=self.colorModelsVar, state= "readonly",takefocus=False)
        colorModelCombobox['values'] = self.colorModels
        colorChanelChoiceFrame = ttk.Frame(conversionControlFrame, width=250, height=90)
        channel_1_Scale = ttk.Scale(colorChanelChoiceFrame, length=self.COLOR_CHANNEL_SCALE_LENGTH, from_=0.0, to=1.0, variable=self.channel_1_value)
        channel_2_Scale = ttk.Scale(colorChanelChoiceFrame, length=self.COLOR_CHANNEL_SCALE_LENGTH, from_=0.0, to=1.0, variable=self.channel_2_value)
        channel_3_Scale = ttk.Scale(colorChanelChoiceFrame, length=self.COLOR_CHANNEL_SCALE_LENGTH, from_=0.0, to=1.0, variable=self.channel_3_value)
        channel_1_ValueLabel = ttk.Label(colorChanelChoiceFrame, textvariable=self.channel_1_value)
        channel_2_ValueLabel = ttk.Label(colorChanelChoiceFrame, textvariable=self.channel_2_value)
        channel_3_ValueLabel = ttk.Label(colorChanelChoiceFrame, textvariable=self.channel_3_value)
        self.channel_1_InfoLabel = ttk.Label(colorChanelChoiceFrame)
        self.channel_2_InfoLabel = ttk.Label(colorChanelChoiceFrame)
        self.channel_3_InfoLabel = ttk.Label(colorChanelChoiceFrame)

        infoLabel = ttk.Label(optFrame, text="black = 0\nwhite = 1")
        chooseImageForProcessingButton = ttk.Button(optFrame, text='Choose this image for processing', command=self.setImageForProcessing)

        # widgets layout 
        imgFrame.grid(column=0, row=0)
        optFrame.grid(column=1, row=0, sticky=N)

        infoLabel.grid(column=0, row=0)
        selectFileButton.grid(column=0, row=1)
        conversionControlFrame.grid(column=0,row=2)
        colorModelCombobox.current(0)
        colorModelCombobox.grid(row=0,column=0)
        colorChanelChoiceFrame.grid(row=1,column=0)
        colorChanelChoiceFrame.grid_propagate(False)
        self.channel_1_InfoLabel.grid(row=0,column=0, sticky=W)
        channel_1_Scale.grid         (row=0,column=1, sticky=W)
        channel_1_ValueLabel.grid    (row=0,column=2, sticky=W)
        self.channel_2_InfoLabel.grid(row=1,column=0, sticky=W)
        channel_2_Scale.grid         (row=1,column=1, sticky=W)
        channel_2_ValueLabel.grid    (row=1,column=2, sticky=W)
        self.channel_3_InfoLabel.grid(row=2,column=0, sticky=W)
        channel_3_Scale.grid         (row=2,column=1, sticky=W)
        channel_3_ValueLabel.grid    (row=2,column=2, sticky=W)
        chooseImageForProcessingButton.grid(row=3,column=0)

        self.imgLabel.grid(column=0, row=0, sticky=N)

        # bindings
        colorModelCombobox.bind('<<ComboboxSelected>>', self.changeColorChanel)
        channel_1_Scale.bind("<ButtonRelease-1>", self.processImage)
        channel_2_Scale.bind("<ButtonRelease-1>", self.processImage)
        channel_3_Scale.bind("<ButtonRelease-1>", self.processImage)
        self.changeColorChanel()

    def chooseImageFile(self, *args):
        filename = askopenfilename()
        try:
            self.imgOriginal = PIL.Image.open(filename)
            self.imgToProcess = copy.copy(self.imgOriginal)
            img = ImageTk.PhotoImage(self.imgOriginal)
            self.isImageLoaded = True
        except:
            return
        self.imgLabel.config(image=img)
        self.imgLabel.image=img
    
    def changeColorChanel(self, *args):
        colorChannelNames = self.colorModelsInfo[self.colorModelsVar.get()]
        self.channel_1_InfoLabel.config(text=colorChannelNames[0])
        self.channel_2_InfoLabel.config(text=colorChannelNames[1])
        self.channel_3_InfoLabel.config(text=colorChannelNames[2])
        if self.isImageLoaded:
            self.imgToProcess = self.imgOriginal.convert(self.colorModelsVar.get())
        self.processImage()
    
    def processImage(self, *args):
        if self.isImageLoaded:
            imgArray = np.asanyarray(self.imgToProcess)
            imgProcessed = utils.rgb2binary(imgArray,
                                            float(self.channel_1_value.get()),
                                            float(self.channel_2_value.get()),
                                            float(self.channel_3_value.get()))
            pilImg = PIL.Image.fromarray(imgProcessed)
            img = ImageTk.PhotoImage(pilImg)
            print(imgProcessed[0:11,0,0])
            self.pilImage = pilImg
            self.imgLabel.config(image=img)
            self.imgLabel.image=img
    
    def setImageForProcessing(self,*args):
        self.imgProcessingFrame.setImage(self.imgLabel.image, self.pilImage, "Converted Image loaded")

        




# class ImageConversionControlsFrame(ttk.LabelFrame):
#     COLOR_CHANNEL_SCALE_LENGTH = 100
#     COLOR_CHANNEL_DEFAULT_VALUE = 0.7

#     def __init__(self, parent, **kwargs):
#         ttk.LabelFrame.__init__(self, parent, **kwargs)
        
#         self.colorModels = ('RGB', 'YCbCr')
#         self.colorModelsInfo = {'RGB':('R','G','B'), 'YCbCr':('Y', 'Cb', 'Cr')}

#         self.colorModelsVar = StringVar()
#         self.colorModelsVar.set(self.colorModels[0])
#         self.channel_1_value = StringVar()
#         self.channel_2_value = StringVar()
#         self.channel_3_value = StringVar()
#         self.channel_1_value.set(self.COLOR_CHANNEL_DEFAULT_VALUE)
#         self.channel_2_value.set(self.COLOR_CHANNEL_DEFAULT_VALUE)
#         self.channel_3_value.set(self.COLOR_CHANNEL_DEFAULT_VALUE)


#         colorModelCombobox = ttk.Combobox(self, textvariable=self.colorModelsVar, state= "readonly",takefocus=False)
#         colorModelCombobox['values'] = self.colorModels
#         colorChanelChoiceFrame = ttk.Frame(self, width=250, height=90)
#         channel_1_Scale = ttk.Scale(colorChanelChoiceFrame, length=self.COLOR_CHANNEL_SCALE_LENGTH, from_=0.0, to=1.0, variable=self.channel_1_value)
#         channel_2_Scale = ttk.Scale(colorChanelChoiceFrame, length=self.COLOR_CHANNEL_SCALE_LENGTH, from_=0.0, to=1.0, variable=self.channel_2_value)
#         channel_3_Scale = ttk.Scale(colorChanelChoiceFrame, length=self.COLOR_CHANNEL_SCALE_LENGTH, from_=0.0, to=1.0, variable=self.channel_3_value)
#         channel_1_ValueLabel = ttk.Label(colorChanelChoiceFrame, textvariable=self.channel_1_value)
#         channel_2_ValueLabel = ttk.Label(colorChanelChoiceFrame, textvariable=self.channel_2_value)
#         channel_3_ValueLabel = ttk.Label(colorChanelChoiceFrame, textvariable=self.channel_3_value)
#         self.channel_1_InfoLabel = ttk.Label(colorChanelChoiceFrame)
#         self.channel_2_InfoLabel = ttk.Label(colorChanelChoiceFrame)
#         self.channel_3_InfoLabel = ttk.Label(colorChanelChoiceFrame)
        
#         colorModelCombobox.current(0)
#         colorModelCombobox.grid(row=0,column=0)
#         colorChanelChoiceFrame.grid(row=1,column=0)
#         colorChanelChoiceFrame.grid_propagate(False)
#         self.channel_1_InfoLabel.grid(row=0,column=0, sticky=W)
#         channel_1_Scale.grid         (row=0,column=1, sticky=W)
#         channel_1_ValueLabel.grid    (row=0,column=2, sticky=W)
#         self.channel_2_InfoLabel.grid(row=1,column=0, sticky=W)
#         channel_2_Scale.grid         (row=1,column=1, sticky=W)
#         channel_2_ValueLabel.grid    (row=1,column=2, sticky=W)
#         self.channel_3_InfoLabel.grid(row=2,column=0, sticky=W)
#         channel_3_Scale.grid         (row=2,column=1, sticky=W)
#         channel_3_ValueLabel.grid    (row=2,column=2, sticky=W)

#         colorModelCombobox.bind('<<ComboboxSelected>>', self.changeColorChanel)
#         channel_1_Scale.bind("<ButtonRelease-1>", self.processImage)
#         channel_2_Scale.bind("<ButtonRelease-1>", self.processImage)
#         channel_3_Scale.bind("<ButtonRelease-1>", self.processImage)
#         self.changeColorChanel()

#     def changeColorChanel(self, *args):
#         colorChannelNames = self.colorModelsInfo[self.colorModelsVar.get()]
#         self.channel_1_InfoLabel.config(text=colorChannelNames[0])
#         self.channel_2_InfoLabel.config(text=colorChannelNames[1])
#         self.channel_3_InfoLabel.config(text=colorChannelNames[2])
    
#     def processImage(self, *args):
#         print(1)



