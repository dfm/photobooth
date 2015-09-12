import numpy as np
from skimage.io import imread, imsave
from skimage.transform import resize


def stitch_images(images, border=16, bottom=100):
    height = images[0].shape[0]
    full_height = 3*border + bottom + 2*height
    full_width = int(full_height*1.5)
    width = int(0.5 * (full_width - 3*border))
    full_image = imread("static/template.jpg")
    delta = int(0.5 * (images[0].shape[1] - width))

    for i, img in enumerate(images[:4]):
        xi = border + (i // 2) * (border + height)
        yi = border + (i % 2) * (border + width)
        full_image[xi:xi+height, yi:yi+width] = img[:, delta:delta+width]

    return (full_image[border:-border, border:-border],
            full_image[:3*border+2*height, :3*border+2*width])


if __name__ == "__main__":
    import glob
    img, twt = stitch_images(list(map(imread, glob.glob("scratch/*.jpg"))))
    imsave("face.jpg", img)
    imsave("face-twitter.jpg", twt)
