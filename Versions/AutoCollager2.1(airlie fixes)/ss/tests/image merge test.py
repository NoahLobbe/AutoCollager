from PIL import Image

def merge(im1, im2):
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGB", (w, h))

    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))

    return im



if __name__ == "__main__":
    image1_filename = "image1.jpg"
    image2_filename = "image2.jpg"

    with Image.open(image1_filename) as Img1, Image.open(image2_filename) as Img2:
        ResultImg = merge(Img1, Img2)
        ResultImg.save("merged.jpg")
