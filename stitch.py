import numpy as np
from skimage import img_as_ubyte
from skimage.io import imread, imsave
from skimage.transform import resize


def stitch_images(images, border=24, bottom=2*100, scale=0.5):
    # Resize the images.
    images = [img_as_ubyte(resize(i, (scale*i.shape[0], scale*i.shape[1])))
              for i in images]

    width = int(images[0].shape[1])
    full_width = 3 * border + 2 * width
    # full_height = 3 * border + bottom + 2 * height
    full_height = int(full_width//1.5)
    height = int(0.5 * (full_height - bottom - 3 * border))
    delta = int(0.5 * (images[0].shape[0] - height))

    # full_image = 255 + np.zeros((full_height, full_width, 3),
    #                             dtype=images[0].dtype)
    full_image = imread("static/template-full.jpg")

    for i, img in enumerate(images[:4]):
        xi = border + (i // 2) * (border + height)
        yi = border + (i % 2) * (border + width)
        full_image[xi:xi+height, yi:yi+width] = img[delta:delta+height]

    return (full_image,
            full_image[border:-border, border:-border],
            full_image[:3*border+2*height, :3*border+2*width])


if __name__ == "__main__":
    import glob
    full, img, twt = stitch_images(list(map(imread, glob.glob("scratch/*.jpg"))))
    imsave("full.jpg", full)
    imsave("face.jpg", img)
    imsave("face-twitter.jpg", twt)
