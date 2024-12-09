from PIL import Image
import numpy as np

src = "media\\Lenna.png"

with Image.open(src) as im:
    ycbcr = im.convert('YCbCr')
    rgb = np.asanyarray(im)
    print(rgb.shape)
    print(rgb[:,:,0])
    
    
