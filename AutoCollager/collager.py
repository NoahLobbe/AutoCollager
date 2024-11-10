import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinterdnd2 as tkDnD2
from merger import Merger
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


class Collager:

    def __init__(self, title, version_str):

        self.Root = tkDnD2.Tk()
        self.Root.title(version_str + " - " + title)
        self.Root.resizable(False, False)
        self.Root.withdraw() # so that adjustments can be made subtley

        self.Merger = Merger((1200,630), True)

        #variables
        self.BORDER_THICKNESS_RANGE = [0,50]
        
        self.outerBorderOn_BoolVar = tk.BooleanVar(value=True)


    def centreWindow(self):
        screen_width = self.Root.winfo_screenwidth()
        screen_height = self.Root.winfo_screenheight()
        win_width = self.Root.winfo_width()
        win_height = self.Root.winfo_height()

        x = int((screen_width/2) - (win_width)/2)
        y = int((screen_height/2) - (win_height)/2)
        self.Root.geometry(f"+{x}+{y}")
        self.Root.update()

        print("new window pos:", x, y)


    def makeWidgets(self):
        #file dialog run
        self.TitleLabel = tk.Label(text="Auto Collager",
                                        font=("TkDefaultFont", 16)
                                   )
        self.DescriptorLabel = tk.Label(text="Automatically runs once images have been selected")
        
        self.RunButton = tk.Button(text="Click to choose images \nor \nDrag 'n' Drop \n",
                                   height=10,
                                   command=self.runCollager
                                   )
        self.RunButton.drop_target_register(tkDnD2.DND_ALL)
        self.RunButton.dnd_bind("<<Drop>>", self.dragDropCollager)


        #options
        self.OptionsSeparator = ttk.Separator(self.Root, orient=tk.HORIZONTAL)

        self.OptionsLabel = tk.Label(text="Customisation",
                                     font=("TkDefaultFont", 14)
                                     )

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
        


    def packWidgets(self):
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
        self.AuthorLabel.place(x=0, y=self.Root.winfo_height() - offset)

        self.centreWindow()
        self.Root.deiconify()


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
        
            img_obj_list = self.Merger.openImages(image_files_list)

            filepath = self.getFilepath()
            filename = filepath +  "/" + datetime.today().strftime('%Y-%m-%d %I.%M.%S%p') + " merged.png"
            print("filename:", filename)
            self.Merger.mergeImages(img_obj_list, filename)

            self.Merger.closeImages(img_obj_list)
            
            subprocess.run(["/usr/bin/open","Downloads/"])
        else:
            print("no images selected/cancelled")


    def dragDropCollager(self, event):
        #process drag and drop string
        files_list_str = event.data[1:]
        files_list_str = files_list_str[:len(files_list_str)-1]
        files_list = files_list_str.split("} {")

        for i in files_list:
            print("file dragged and dropped:", i)

        print("running collager...")
        self.runCollager(files_list, True)


    def run(self):
        self.Root.mainloop()
