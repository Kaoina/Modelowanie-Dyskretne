from PIL import Image
import numpy as np
from scipy.ndimage import grey_closing, grey_opening


def closing_operation(file_path, save_closing_path, size=3):

    image = Image.open(file_path).convert('RGB')
    image_array = np.array(image)

    closing_result = np.zeros_like(image_array)

    for channel in range(3):
        closing_result[:, :, channel] = grey_closing(image_array[:, :, channel], size=size)

    closing_image = Image.fromarray(closing_result, mode='RGB')

    closing_image.save(save_closing_path)





