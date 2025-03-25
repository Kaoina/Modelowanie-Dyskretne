from PIL import Image


def display_image(narrow_path, pixelized_path, scale_factor=5):
    image = Image.open(narrow_path)

    new_width = image.width // scale_factor
    new_height = image.height // scale_factor
    scaled_image = image.resize((new_width, new_height), Image.Resampling.NEAREST)

    upscaled_image = scaled_image.resize((image.width, image.height), Image.Resampling.NEAREST)

    upscaled_image.save(pixelized_path)

    return upscaled_image
