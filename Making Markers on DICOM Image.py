# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 23:03:09 2023

@author: Sevgi
"""
import pydicom
import matplotlib.pyplot as plt
import numpy as np

from pydicom.pixel_data_handlers.util import apply_modality_lut

# Loading the wanted DICOM image for making spot dots.
dicom_file_path = 'mrıscan.dcm' #write the file name that chosen.
dicom_image = pydicom.dcmread(dicom_file_path)

# Decompressing
if dicom_image.file_meta.TransferSyntaxUID.is_compressed:
    dicom_image.decompress(handler_name=None)


pixel_data = dicom_image.pixel_array

#For seperate markers and the original DICOM image, using pixel
rgba_image = np.zeros((pixel_data.shape[0], pixel_data.shape[1], 4), dtype=np.uint8)

# Define the colors with transparency 
mark_color = (255, 255, 0, 80)  # Light yellow ?% 
mark_color1 = (255, 10, 210, 80)  # Light cyan ?% transparency

# Defining the areas within axes.
x_start = 475
y_start = 90
width = 80
height = 250
rgba_image[y_start:y_start + height, x_start:x_start + width, :] = mark_color

x_start1 = 90
y_start1 = 105
width1 = 150
height1 = 80
rgba_image[y_start1:y_start1 + height1, x_start1:x_start1 + width1, :] = mark_color1

#blending variations of DICOM and markers transparency.
composite_image = np.copy(pixel_data)
alpha = rgba_image[:, :, 3] / 255.0


for c in range(3):  
    composite_image[y_start:y_start + height, x_start:x_start + width, c] = (
        (1 - alpha[y_start:y_start + height, x_start:x_start + width]) * composite_image[y_start:y_start + height, x_start:x_start + width, c] +
        alpha[y_start:y_start + height, x_start:x_start + width] * rgba_image[y_start:y_start + height, x_start:x_start + width, c]
    ).astype(np.uint8)

for c in range(3):  
    composite_image[y_start1:y_start1 + height1, x_start1:x_start1 + width1, c] = (
        (1 - alpha[y_start1:y_start1 + height1, x_start1:x_start1 + width1]) * composite_image[y_start1:y_start1 + height1, x_start1:x_start1 + width1, c] +
        alpha[y_start1:y_start1 + height1, x_start1:x_start1 + width1] * rgba_image[y_start1:y_start1 + height1, x_start1:x_start1 + width1, c]
    ).astype(np.uint8)

# Display the composite image with markers
plt.imshow(composite_image, cmap='gray')
plt.title('DICOM Image with Markers')
plt.axis('datas')
plt.show()





