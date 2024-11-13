from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinterdnd2 as tkDnD2
import math
from datetime import datetime
import os
from pathlib import Path
import subprocess



BORDER_COLORS_DICT = {
    "white": (255,255,255,255),
    "black": (0,0,0,255),
    "transparent": (0,0,0,0)
    }
BORDER_COLORS_KEYS = list(BORDER_COLORS_DICT.keys())


# Functions
def openImages(img_file_list):
    obj_list = []
    for img_file in img_file_list:
        obj_list.append(Image.open(img_file))

    return obj_list

def closeImages(img_obj_list):
    for ImgObj in img_obj_list:
        ImgObj.close()


def getLargestDimension(img_list, isWidth=0):
    max_dim = 0
    for Img in img_list:
        if Img.size[isWidth] > max_dim:
            max_dim = Img.size[isWidth]

    return max_dim


def scaleImagesToWidth(img_list, new_width):
    new_img_list = []
    for Img in img_list:
        scaled_height = int(new_width * (Img.size[1] / Img.size[0]))
        
        new_img_list.append( Img.resize((new_width, scaled_height), Image.Resampling.LANCZOS))

    return new_img_list


def scaleImageToWidth(Img, new_width):
    
    scaled_height = int(new_width * (Img.size[1] / Img.size[0]))
        
    return Img.resize((new_width, scaled_height), Image.Resampling.LANCZOS)



# App Object
class Collager:

    def __init__(self, win_size, title):

        self.Root = tkDnD2.Tk()
        self.Root.title(title)
        self.Root.resizable(False, False)
        #self.Root.iconphoto(True, tk.Image("photo", file="icon.png"))
        self.Root.withdraw() # so that adjustments can be made subtley


        #variables
        self.BORDER_THICKNESS_RANGE = [0,50]
        
        self.outerBorderOn_BoolVar = tk.BooleanVar(value=True)


        ##widgets
        #file dialog run
        self.TitleLabel = tk.Label(text="Auto Collager",
                                        font=("TkDefaultFont", 16))
        self.DescriptorLabel = tk.Label(text="Automatically runs once images have been selected")
        
        self.RunButton = tk.Button(text="Click to choose images \nor \nDrag 'n' Drop \n",
                                   height=10,
                                   command=self.runCollager)
        self.RunButton.drop_target_register(tkDnD2.DND_ALL)
        self.RunButton.dnd_bind("<<Drop>>", self.dragDropCollager)


        #options
        self.OptionsSeparator = ttk.Separator(self.Root, orient=tk.HORIZONTAL)

        self.OptionsLabel = tk.Label(text="Customisation",
                                     font=("TkDefaultFont", 14))

        self.BorderthicknessLabel = tk.Label(text="Border thickness: ")        
        self.BorderthicknessSpinBox = ttk.Spinbox(
            self.Root,
            from_=self.BORDER_THICKNESS_RANGE[0],
            to=self.BORDER_THICKNESS_RANGE[1],
            width=5
            )
        self.BorderthicknessSpinBox.insert(0,10)

        
        self.BordercolorLabel = tk.Label(text="Border color: ")
        self.BordercolorCombobox = ttk.Combobox(
            self.Root,
            width=15,
            values=BORDER_COLORS_KEYS
            )
        self.BordercolorCombobox.current(0)


        self.BorderOuterlabel = tk.Label(text="Border along outside: ")
        self.BorderOuterCheckbutton = tk.Checkbutton(
            self.Root,
            onvalue=True,
            offvalue=False,
            variable=self.outerBorderOn_BoolVar,
            command=self.updateBorderOutside
            )


        #other
        self.AuthorLabel = tk.Label(text="Noah Lobbe 2024", font=("TkDefaultFont", 7))
        

        #packing
        self.Root.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.TitleLabel.grid(row=0, column=1, columnspan=2)
        self.DescriptorLabel.grid(row=1, column=1, columnspan=2)
        self.RunButton.grid(pady=5, row=2, column=1, columnspan=2, sticky="NSEW")

        
      
        self.OptionsSeparator.grid(pady=5, row=4, column=0, columnspan=4, sticky="EW")

        self.OptionsLabel.grid(pady=5, row=4, column=1, columnspan=2)
        
        self.BorderthicknessLabel.grid(pady=5, row=5, column=1, sticky="E")
        self.BorderthicknessSpinBox.grid(row=5, column=2, sticky="W")
        
        self.BordercolorLabel.grid(pady=5, row=6, column=1, sticky="E")
        self.BordercolorCombobox.grid(row=6, column=2, sticky="W")

        self.BorderOuterlabel.grid(pady=5, row=7, column=1, sticky="E")
        self.BorderOuterCheckbutton.grid(row=7, column=2, sticky="W")

        self.Root.update()
        print("Window height after widgets:", self.Root.winfo_height())

        offset = 14
        new_height = self.Root.winfo_height() + offset
        width = self.Root.winfo_width()
        self.Root.geometry(f"{width}x{new_height}")
        self.Root.update()
        
        print("Window height adjusted for author label:", self.Root.winfo_height())
        self.AuthorLabel.place(x=0, y=self.Root.winfo_height()-offset)

        self.centreWindow()
        self.Root.deiconify()
        
        
    def centreWindow(self):
        screen_width = self.Root.winfo_screenwidth()
        screen_height = self.Root.winfo_screenheight()
        win_width = self.Root.winfo_width()
        win_height = self.Root.winfo_height()

        x = int((screen_width/2) - (win_width)/2)
        y = int((screen_height/2) - (win_height)/2)

        print("new window pos:", x, y)

        self.Root.geometry(f"+{x}+{y}")
        self.Root.update()
    

    def updateBorderColor(self):
        option_menu_value = self.BordercolorCombobox.get()
        self.border_color = BORDER_COLORS_DICT[option_menu_value]
        print("updated border color,", self.border_color)

    def updateBorderThickness(self):
        option_menu_value = self.BorderthicknessSpinBox.get()
        self.border_thickness = int(option_menu_value)
        print("updated border thickness,", self.border_thickness)

    def updateBorderOutside(self):
        self.outer_border_on = self.outerBorderOn_BoolVar.get()
        print("updated border along outside,", self.outer_border_on)

    def getFilepath(self):
        return str(os.path.join(Path.home(), "Downloads"))


    def determineLayout(self, num_images):

        if num_images == 1:
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
                cols = math.isqrt(num_images)
                rows = num_images // cols

                if (rows * cols) != num_images: # left overs go to a new row
                    rows += 1 #temporary fix as individual images are rotated after merge
                
        return (rows, cols)

    def mergeImages(self, img_list, filename):
        self.outer_border_on = self.outerBorderOn_BoolVar.get()
        num_images = len(img_list)
        num_rows, num_cols = self.determineLayout(num_images)
        
        print(f"\tlayout: ({num_rows}, {num_cols})")
        
        max_img_width = getLargestDimension(img_list,0)

        img_list = scaleImagesToWidth(img_list, max_img_width)
        

        #determine final image dimensions
        total_width = num_cols * (self.border_thickness + max_img_width) - self.border_thickness + self.outer_border_on*2*self.border_thickness 

        total_height = (num_rows - 1 + self.outer_border_on*2) * self.border_thickness
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
        
        FinalImg = Image.new("RGBA", (total_width, total_height), self.border_color)
        
        print(f"\tnew max img width after scaling: {max_img_width}")    
        print(f"\tfinal size: ({total_width}, {total_height})")
        
        y_pos = self.outer_border_on * self.border_thickness
        for row in range(num_rows):
            y_pos += (row > 0) * (row_heights[row-1] + self.border_thickness)
            for col in range(num_cols):
                i = row * num_cols + col
                x_pos = col * (max_img_width + self.border_thickness) + self.outer_border_on * self.border_thickness
                
                if i < num_images:
                    Img = img_list[i]
                    centring_offset = int((max_img_width - Img.size[0]) / 2)
                    x_pos += centring_offset
                    
                    print(f"\trow: {row}")
                    print(f"\tcentring offset: {centring_offset}")
                    print(f"current pos for image {i} of width {Img.size[0]} is ({x_pos}, {y_pos})")

                    FinalImg.paste(Img, (x_pos, y_pos))

                    
        #rescale image to be nice to facebook
        FinalImg = scaleImageToWidth(FinalImg, 1200)
        FinalImg = FinalImg.rotate(-90, expand=1)
        FinalImg.save(filename)


    def runCollager(self, image_files_list=None, dragged_dropped=False):
        print("passed params:", image_files_list, dragged_dropped)

        #update varaibels
        self.updateBorderColor()
        self.updateBorderThickness()

        #get images
        if (image_files_list == None) and not dragged_dropped:
            files_str = filedialog.askopenfilenames(title="Select images")
            image_files_list = self.Root.tk.splitlist(files_str)

            for i in image_files_list:
                print("file selected:", i)

        if len(image_files_list) > 1:
        
            img_obj_list = openImages(image_files_list)

            filepath = self.getFilepath()
            filename = filepath +  "/" + datetime.today().strftime('%Y-%m-%d %I.%M.%S%p') + " merged.png"
            print("filename:", filename)
            self.mergeImages(img_obj_list, filename)

            closeImages(img_obj_list)
            
            subprocess.run(["/usr/bin/open","Downloads/"])
        else:
            print("no images selected/cancelled")



    def dragDropCollager(self, event):
        print("Type is:", type(event.data), event.data)
        #process drag and drop string
        print("First char is:", event.data[0])
        files_list_str = event.data[1:]
        files_list_str = files_list_str[:len(files_list_str)-1]
        files_list = files_list_str.split("} {")

        for i in files_list:
            print("file dragged and dropped:", i)

        print("running collager...")
        self.runCollager(files_list, True)


    def run(self):
        self.Root.mainloop()
