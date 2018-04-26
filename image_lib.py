from PIL import Image, ImageOps, ImageChops

########## BASE FUNCTIONS

def pad_image(image,target_width,target_height,fill_color='white'):

    width,height = image.size

    if width>target_width or height>target_height:
        raise Exception('Image is too big to be padded')

    left_padding = int((target_width-width)/2)
    right_padding = target_width-left_padding-width
    top_padding = int((target_height-height)/2)
    bottom_padding = target_height-top_padding-height

    border=(left_padding,top_padding,right_padding,bottom_padding)

    return ImageOps.expand(image,border=border,fill=fill_color)


def scale_image(image,target_width,target_height,resample_filter = Image.LANCZOS):
    # It keeps the ratio

    width,height = image.size
    scale_ratio = min(target_width/width,target_height/height)

    new_width = int(width*scale_ratio)
    new_height = int(height*scale_ratio)

    return image.resize((new_width,new_height),resample_filter)


def trim_image(image):
    background = Image.new(image.mode, image.size, image.getpixel((0,0)))
    diff = ImageChops.difference(image, background)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)

########## ADVANCED FUNCTIONS

def scale_and_pad(image,target_width,target_height,resample_filter = Image.LANCZOS,fill_color='white'):
    temp = scale_image(image,target_width,target_height,resample_filter)
    return pad_image(temp,target_width,target_height,fill_color)


def trim_and_scale(image,target_width,target_height,resample_filter = Image.LANCZOS):
    temp = trim_image(image)
    return scale_image(temp,target_width,target_height,resample_filter)


def trim_scale_and_pad(image,target_width,target_height,resample_filter = Image.LANCZOS,fill_color='white'):
    temp = trim_image(image)
    temp = scale_image(temp,target_width,target_height,resample_filter)
    return pad_image(temp,target_width,target_height,fill_color)
