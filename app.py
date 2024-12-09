from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import utils
import myWidgets
import numpy as np
from tkinter.filedialog import askopenfilename

# Root window nad notebook 
root = Tk()
rootNotebook = ttk.Notebook(root)
rootNotebook.pack(pady=10, expand=True)

mainframe = ttk.Frame(rootNotebook, padding=10)
mainframe.grid(column=0, row=0)

secondaryFrame = ttk.Frame(rootNotebook, padding=10)

# root.grid_columnconfigure(0, weight=1)
# root.grid_rowconfigure(0,weight=1)
# root.geometry("1000x700")

# widget functions
def changeSize(*args):
    newGridSize = int(kernelSize.get())
    kernelChoiseGrid.resize(newGridSize)

def chooseImageFile(*args):
    filename = askopenfilename()
    img = ImageTk.PhotoImage(Image.open(filename))
    imgLabel.config(image=img)
    imgLabel.image=img


# variables
img = ''
kernelSize = StringVar()
kernelSize.set('3')

# widgets 
imgFrame = ttk.Frame(mainframe, padding=10)
optFrame = ttk.Frame(mainframe, padding=10)

selectFileButton = ttk.Button(optFrame, text="Select image", command=chooseImageFile)
kernelChoiseFrame = ttk.Labelframe(optFrame, text="Kernel" ,padding=10)
kernelSizeSpinbox = ttk.Spinbox(kernelChoiseFrame, from_=3, to=15, increment=2, textvariable=kernelSize, command=changeSize)
kernelChoiseGrid = myWidgets.KernelPickerGrid(kernelChoiseFrame, 3, background='gray50' )

imgLabel = ttk.Label(imgFrame, text='No image to display')
imgLabel.pack()

# widgets layout 
imgFrame.grid(column=0, row=0)
optFrame.grid(column=1, row=0, sticky=N)

selectFileButton.grid(column=0, row=0)
kernelSizeSpinbox.grid(column=0, row=0, sticky=W)
kernelChoiseFrame.grid(column=0,row=1)
kernelChoiseGrid.grid(column=0,row=1)

imgLabel.grid(column=0, row=0)
# imgLabel['image'] = img


# # imgGrid = ttk.Frame(mainframe, padding=10).grid(column=2, row=1)
# img_tmp = Image.open(askopenfilename())
# img_tmp = ImageTk.PhotoImage(img_tmp)
# # imgLabel = ttk.Label(imgGrid)
# # imgLabel.grid(column=1, row=1)
# # status1['image'] = img
# imgLabel['image'] = img_tmp
# # filename = askopenfilename()



# s = ttk.Style()
# s.configure('My.TFrame', background='red')
# optGrid = ttk.Frame(mainframe, padding=10, style='My.TFrame', height=100, width=100)



# kernelChoiseFrame = ttk.Labelframe(optGrid, text="Kernel" ,padding=10).grid(column=1,row=1)
# spinval = StringVar()
# kernelSize = ttk.Spinbox(kernelChoiseFrame, from_=3, to=15, textvariable=spinval).grid(row=1, column=1)




# label = ttk.Label(mainframe, text="test", width=10)
# label.grid(column=1, row=1)
# ttk.Label(mainframe, text="test2", width=10).grid(column=1, row=2)

# canvas = Canvas(mainframe, width=100, height=100, background='red').grid(column=1, row=3)

# t = Image.open("lena.png")
# imageRaw = utils.openAsBinary("lena.png")
# img = ImageTk.PhotoImage(image=Image.fromarray(utils.openAsBinary("lena.png")))

# imageLabel = ttk.Label(mainframe, text="test", width=10)
# imageLabel.grid(column=2, row=1, rowspan=3)
# imageLabel["image"] = img
rootNotebook.add(mainframe, text="Binary Image Processing")
rootNotebook.add(secondaryFrame, text="Convert color to binary")
root.mainloop()