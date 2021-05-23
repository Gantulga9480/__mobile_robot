from PIL import Image
import numpy as np
img_w, img_h = 200, 200
data = np.zeros((img_h, img_w, 3), dtype=np.uint8)
data[100, 100] = [255, 0, 0]
img = Image.fromarray(data, 'RGB')
img.save('test.png')
img.show()
