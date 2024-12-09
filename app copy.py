from tkinter import *
from tkinter import ttk
import myWidgets

# Root window nad notebook 
root = Tk()
rootNotebook = ttk.Notebook(root)
rootNotebook.pack(pady=10, expand=True)

mainframe = myWidgets.BinaryImageProcessingMainFrame(rootNotebook, padding=10)
mainframe.grid(column=0, row=0)

secondaryFrame = myWidgets.ColorToBinaryConversionFrame(rootNotebook, mainframe, padding=10)
secondaryFrame.grid(column=0, row=0)


rootNotebook.add(mainframe, text="Binary Image Processing")
rootNotebook.add(secondaryFrame, text="Convert color to binary")
root.mainloop()