import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinterdnd2 as tkDnD2
from merger import Merger
from datetime import datetime
import os
from pathlib import Path
import subprocess
import platform


BORDER_COLORS_DICT = {
    "white": (255,255,255,255),
    "black": (0,0,0,255),
    "transparent": (0,0,0,0)
    }
BORDER_COLORS_KEYS = list(BORDER_COLORS_DICT.keys())


class Collager:

    def __init__(self, title, version_str):

        self.Root = tkDnD2.Tk()
        self.Root.title(title + " " + version_str)
        self.Root.resizable(False, False)
        self.Root.withdraw() # so that adjustments can be made subtley

        self.Merger = Merger((1200,630), True)

        #variables
        self.BORDER_THICKNESS_RANGE = [0,50]
        self.DISP_TEXT_LENGTH = 100
        self.FILE_FORMAT= ".png"
        self.filename = datetime.today().strftime('%Y-%m-%d %I.%M.%S%p') + " merged"
        self.save_directory = str(os.path.join(Path.home(), "Downloads"))
        
        self.outerBorderOn_BoolVar = tk.BooleanVar(value=True)
        self.filename_StrVar = tk.StringVar(value = self.filename)
        self.saveDir_StrVar = tk.StringVar(value = self.save_directory)

        self.filename_StrVar.trace_add("write", self.updateFilename)
        self.saveDir_StrVar.trace_add("write", self.updateSaveDir)


        
        

        self.makeWidgets()
        self.packWidgets()
        self.updateFilename()
        self.updateSaveDir()


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
        
        self.filenameLabel = tk.Label(text="Image name: ")
        self.filenameEntry = tk.Entry(textvariable=self.filename_StrVar)
        #self.filenameEntry.bind("<Button-1>", self.updateFilename)
        #self.filenameUpdateButton = tk.Button(text="Update", command=self.updateFilename)

        self.SaveDirLabel = tk.Label(text="Save to: ")
        self.SaveDirEntry = tk.Entry(textvariable=self.saveDir_StrVar)
        self.SaveDirDialogButton = tk.Button(text="...", command=self.updateSaveDirDialog)

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


    def packWidgets(self):
        self.Root.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        
        self.TitleLabel.grid(row=0, column=1, columnspan=3)
        self.DescriptorLabel.grid(row=1, column=1, columnspan=3)
        self.RunButton.grid(pady=5, row=2, column=1, columnspan=3, sticky="NSEW")

        
        self.OptionsSeparator.grid(pady=5, row=3, column=0, columnspan=5, sticky="EW")
        self.OptionsLabel.grid(pady=5, row=3, column=1, columnspan=3)

        self.filenameLabel.grid(pady=5, row=4, column=1, sticky="E")
        self.filenameEntry.grid(pady=5, row=4, column=2, sticky="EW")
        #self.filenameUpdateButton.grid(pady=5, row=4, column=3, sticky="W")

        self.SaveDirLabel.grid(pady=5, row=5, column=1, sticky="E")
        self.SaveDirEntry.grid(pady=5, row=5, column=2, sticky="EW")
        self.SaveDirDialogButton.grid(pady=5, row=5, column=3, sticky="W")
        
        self.BorderthicknessLabel.grid(pady=5, row=6, column=1, sticky="E")
        self.BorderthicknessSpinBox.grid(row=6, column=2, sticky="W")
        
        self.BordercolorLabel.grid(pady=5, row=7, column=1, sticky="E")
        self.BordercolorCombobox.grid(row=7, column=2, sticky="W")

        self.BorderOuterlabel.grid(pady=5, row=8, column=1, sticky="E")
        self.BorderOuterCheckbutton.grid(row=8, column=2, sticky="W")

        self.Root.update()
        self.centreWindow()
        self.Root.deiconify()


    def updateBorderColor(self):
        option_menu_value = self.BordercolorCombobox.get()
        self.border_color = BORDER_COLORS_DICT[option_menu_value]
        print("updated border color,", self.border_color)
        return self.border_color

    def updateBorderThickness(self):
        option_menu_value = self.BorderthicknessSpinBox.get()
        self.border_thickness = int(option_menu_value)
        print("updated border thickness,", self.border_thickness)
        return self.border_thickness

    def updateBorderOutside(self):
        self.outer_border_on = self.outerBorderOn_BoolVar.get()
        print("updated border along outside,", self.outer_border_on)
        return self.outer_border_on
    
    def updateSaveDir(self,*args):
        print("args:", args)
        path = self.saveDir_StrVar.get()
            
        if os.path.isdir(path):
            self.save_directory = path
            self.saveDir_StrVar.set(self.save_directory)

            if len(self.save_directory) < self.DISP_TEXT_LENGTH:
                self.SaveDirEntry['width'] = len(self.save_directory)
        print("path is now:", self.save_directory, self.saveDir_StrVar.get())
        
    def updateSaveDirDialog(self):
        new_dir = filedialog.askdirectory()
        if os.path.isdir(new_dir):
            print("updating save dir")
            self.saveDir_StrVar.set(os.path.normpath(new_dir))
            
        else:
            print("\tfiledialog was given empty save directory str")


    def updateFilename(self, *args):
        print("args:", args)
        name = self.filename_StrVar.get()
        if True: #later add name validation
            self.filename = name
            if len(self.filename) < self.DISP_TEXT_LENGTH:
                print("len()", len(self.filename))
                self.filenameEntry['width'] = len(self.filename)
            #self.filenameEntry.insert(0, self.filename)

        print("filename is now: ", self.filename)


    def runCollager(self, image_files_list=None, dragged_dropped=False):
        print("passed params:", image_files_list, dragged_dropped)

        #update varaibels
        color = self.updateBorderColor()
        border_thickness = self.updateBorderThickness()
        is_border = self.updateBorderOutside()
        outer_border_thickness = is_border *  border_thickness

        #get images
        if (image_files_list == None) and not dragged_dropped:
            files_str = filedialog.askopenfilenames(title="Select images")
            image_files_list = self.Root.tk.splitlist(files_str)

            for i in image_files_list:
                print("file selected:", i)

        if len(image_files_list) > 1:
        
            img_obj_list = self.Merger.openImages(image_files_list)

            self.updateSaveDir()
            self.updateFilename()
            filename = self.save_directory +  "/" + self.filename + self.FILE_FORMAT
            print("filename:", filename)

            self.Merger.mergeImages(img_obj_list, filename, color, border_thickness, outer_border_thickness)

            self.Merger.closeImages(img_obj_list)

            if platform.system() == "Darwin":
                subprocess.run(["/usr/bin/open","Downloads/"])
            elif platform.system() == "Windows":
                os.startfile(filename)
                
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
