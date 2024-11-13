from PIL import Image
import tkinter as tk
from tkinter import filedialog
import math

BORDER_THICKNESS = 10
BORDER_COLOR = (255,255,0)


def determinePattern(img_list):
    
    num_img = len(img_list)

    if num_img == 1:
        pattern_size = [1,1]
    
    elif num_img <= 3:
        pattern_size = [num_img,1]

    elif num_img > 3:
        square_root = math.sqrt(num_img)
        if square_root.is_integer():
            pattern_size = [square_root, square_root]
            
        elif (num_img % 2) == 0: #even numbers...
            num_across = num_img / 2
            num_high = 2
        
        else: #odd numbers
            num_across = math.floor(num_img/2)
    return pattern_size


def mergeImages(img_list):
    num_images = len(img_list)
    
    total_width = (num_images - 1) * BORDER_THICKNESS
    total_height = img_list[0].size[1]
    
    for Img in img_list:
        total_width += Img.size[0]
        print(f"current size: (%d, %d)", total_width, total_height)

    # make object for final merge
    FinalImg = Image.new("RGB", (total_width, total_height), BORDER_COLOR)

    # add the other images
    x_pos = 0
    FinalImg.paste(img_list[0], (x_pos,0))
    for i in range(1,num_images):
        x_pos += img_list[i-1].size[0] + BORDER_THICKNESS
        y_pos = 0
        FinalImg.paste(img_list[i], (x_pos, y_pos))

    FinalImg.save("merged.jpg")
    
    

def openImages(img_file_list):
    obj_list = []

    for img_file in img_file_list:
        obj_list.append(Image.open(img_file))

    return obj_list


def closeImages(img_obj_list):
    
    for ImgObj in img_obj_list:
        ImgObj.close()



if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    files_str = filedialog.askopenfilenames(title="Choose images")
    image_files_list = root.tk.splitlist(files_str)
    
    img_obj_list = openImages(image_files_list)

    mergeImages(img_obj_list)

    closeImages(img_obj_list)
