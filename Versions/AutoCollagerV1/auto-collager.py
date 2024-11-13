from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import filedialog
import math
from datetime import datetime

BORDER_THICKNESS = 10
ADD_OUTER_BORDER = True
BORDER_COLOR = (255,255,255,255)


def determineLayout(num_images):

    if num_images == 1:
        print("\tonly 1 image..")
        rows = 1
        cols = 1
    
    elif num_images <= 3:
        rows = 1
        cols = num_images

    elif num_images > 3:
        square_root = math.sqrt(num_images)
        if square_root.is_integer():
            rows = int(square_root)
            cols = int(square_root)
            
        else:
            rows = math.isqrt(num_images)
            cols = num_images // rows

            if (rows * cols) != num_images: # left overs go to a new row
                #rows += 1
                cols += 1
            
    return (rows, cols)

def getLargestDimension(img_list, isWidth=0):

    max_dim = 0
    for Img in img_list:
        if Img.size[isWidth] > max_dim:
            max_dim = Img.size[isWidth]

    return max_dim


def scaleImagesToWidth(img_list, width):
    for i in range(len(img_list)):
        scaled_height = int(width * (img_list[i].size[1] / img_list[i].size[0]))
        print("new size", width, scaled_height)
        img_list[i] = img_list[i].resize((width, scaled_height), Image.Resampling.LANCZOS)

    #return img_list
    

def mergeImages(img_list, filename):
    num_images = len(img_list)
    num_rows, num_cols = determineLayout(num_images)
    print(f"\tlayout: ({num_rows}, {num_cols})")
    
    max_img_width = getLargestDimension(img_list,0)

    scaleImagesToWidth(img_list, max_img_width)
    

    
    #determine merged image dimensions
    total_width = num_cols * (BORDER_THICKNESS + max_img_width) - BORDER_THICKNESS + ADD_OUTER_BORDER*2*BORDER_THICKNESS

    total_height = (num_rows - 1 + ADD_OUTER_BORDER*2) * BORDER_THICKNESS
    row_heights = []
    for row in range(num_rows):
        start_index = row * num_cols
        end_index = (row + 1) * num_cols
        if end_index > num_images:
            end_index = num_images
            print("\tend index is num_images")

        print("\tindexes: ", start_index, end_index)
        curr_row = img_list[start_index:end_index]
        row_heights.append(getLargestDimension(curr_row, 1))

        total_height += row_heights[row]

        
    #total_height = num_rows * (BORDER_THICKNESS + max_img_height) - BORDER_THICKNESS
    FinalImg = Image.new("RGBA", (total_width, total_height), BORDER_COLOR)

    
    print(f"\tnew max img width after scaling: {max_img_width}")    
    print(f"\tfinal size: ({total_width}, {total_height})")


    break_loop = False
    y_pos = ADD_OUTER_BORDER * BORDER_THICKNESS
    for row in range(num_rows):
        y_pos += (row > 0) * (row_heights[row-1] + BORDER_THICKNESS)
        for col in range(num_cols):
            i = row * num_cols + col
            x_pos = col * (max_img_width + BORDER_THICKNESS) + ADD_OUTER_BORDER * BORDER_THICKNESS
            
            if i >= num_images:
                pass
                """
                topleft = (x_pos, y_pos)
                bottomright = (x_pos + max_img_width, y_pos + row_heights[row])
                
                draw = ImageDraw.Draw(FinalImg)
                draw.rectangle( [topleft, bottomright], fill=(0,0,0,0))
                """
            else:
                Img = img_list[i]
                centring_offset = int((max_img_width - Img.size[0]) / 2)
                x_pos += centring_offset
                

                print(f"\trow: {row}")
                print(f"\tcentring offset: {centring_offset}")
                print(f"current pos for image {i} of width {Img.size[0]} is ({x_pos}, {y_pos})")

                FinalImg.paste(Img, (x_pos, y_pos))


    FinalImg.save(filename)

            


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

    filename = datetime.today().strftime('%Y-%m-%d %I.%M.%S%p') + " merged.png"
    
    mergeImages(img_obj_list, filename)

    closeImages(img_obj_list)
