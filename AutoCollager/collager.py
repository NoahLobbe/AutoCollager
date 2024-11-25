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
        self.PAD = 5
        self.NUM_COLS = 5
        self.BORDER_THICKNESS_RANGE = [0,50]
        self.DISP_TEXT_LENGTH = 100
        self.FILE_FORMAT= ".png"
        self.filename_default = datetime.today().strftime('%Y-%m-%d %I.%M.%S%p') + " merged"
        self.filename = ""
        self.file_count = 0
        self.save_directory = str(os.path.join(Path.home(), "Downloads"))
        
        self.outerBorderOn_BoolVar = tk.BooleanVar(value=True)
        self.filename_StrVar = tk.StringVar(value = self.filename_default)
        self.saveDir_StrVar = tk.StringVar(value = self.save_directory)
        self.autoOpenFile_BoolVar = tk.BooleanVar(value=True)

        self.filename_StrVar.trace_add("write", self.updateFilename)
        self.saveDir_StrVar.trace_add("write", self.updateSaveDir)

        self.widget_list = []
        self.widget_packing_list = []

        self.layout_list =  [
            {
             "frame": tk.Frame(master=self.Root),
             "frame_grid":{"row":0, "column":0, "sticky":"EW", "padx":self.PAD},
             "widgets": [],
             "widgets_grid_params":[]
             },
            {
             "frame": tk.Frame(master=self.Root),
             "frame_grid":{"row":1, "column":0, "padx":self.PAD},
             "widgets": [],
             "widgets_grid_params":[]
             }
        ]
        
        

        self.makeWidgets()
        self.packWidgets()
        self.updateFilename()
        print("updating save dir...")
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
        ##frame 1
        #title
        self.TitleLabel = tk.Label(
            master=self.layout_list[0]["frame"],
            text="Auto Collager",
            font=("TkDefaultFont", 16)
            )
        self.layout_list[0]["widgets"].append(self.TitleLabel)
        self.layout_list[0]["widgets_grid_params"].append({"row":0, "column":0, "columnspan":3, "sticky":""})


        #run button
        self.RunButton = tk.Button(
            master=self.layout_list[0]["frame"],
            text="Click to choose images \nor \nDrag 'n' Drop \n",
            relief=tk.GROOVE,
            height=10,
            command=self.runCollager
            )
        self.RunButton.drop_target_register(tkDnD2.DND_ALL)
        self.RunButton.dnd_bind("<<Drop>>", self.dragDropCollager)

        self.layout_list[0]["widgets"].append(self.RunButton)
        self.layout_list[0]["widgets_grid_params"].append({"row":1, "column":0, "sticky":"NSEW"})

        ##frame 2
        #options
        self.OptionsSeparator = ttk.Separator(master=self.layout_list[1]["frame"], orient=tk.HORIZONTAL)   
        self.OptionsLabel = tk.Label(
            master=self.layout_list[1]["frame"],
            text="Customisation",
            font=("TkDefaultFont", 14)
            )
        self.layout_list[1]["widgets"].extend([self.OptionsSeparator, self.OptionsLabel])
        self.layout_list[1]["widgets_grid_params"].extend(
            [{"row":1, "column":0, "columnspan":self.NUM_COLS, "sticky":"EW"},
             {"row":1, "column":1, "columnspan":3, "sticky":""}]
            )


        #filename
        self.FilenameLabel = tk.Label(master=self.layout_list[1]["frame"], text="Image name: ")
        self.FilenameEntry = tk.Entry(master=self.layout_list[1]["frame"], textvariable=self.filename_StrVar)
        
        self.layout_list[1]["widgets"].extend([self.FilenameLabel, self.FilenameEntry])
        self.layout_list[1]["widgets_grid_params"].extend(
            [{"row":4, "column":1, "columnspan":1, "sticky":"E"},
             {"row":4, "column":2, "columnspan":1, "sticky":"W"}]
            )

        #save directory
        self.SaveDirLabel = tk.Label(master=self.layout_list[1]["frame"], text="Save to: ")
        self.SaveDirEntry = tk.Entry(master=self.layout_list[1]["frame"], textvariable=self.saveDir_StrVar)
        self.SaveDirDialogButton = tk.Button(master=self.layout_list[1]["frame"], text="...", command=self.updateSaveDirDialog)

        self.layout_list[1]["widgets"].extend([self.SaveDirLabel, self.SaveDirEntry, self.SaveDirDialogButton])
        self.layout_list[1]["widgets_grid_params"].extend(
            [{"row":5, "column":1, "columnspan":1, "sticky":"E"},
             {"row":5, "column":2, "columnspan":1, "sticky":"EW"},
             {"row":5, "column":3, "columnspan":1, "sticky":"W"}]
            )
        
        #auto open file
        self.AutoOpenFilelabel = tk.Label(master=self.layout_list[1]["frame"], text="Open file once generated: ")
        self.AutoOpenFileCheckbutton = tk.Checkbutton(
            master=self.layout_list[1]["frame"],
            onvalue=True,
            offvalue=False,
            variable=self.autoOpenFile_BoolVar
            )
        self.layout_list[1]["widgets"].extend([self.AutoOpenFilelabel, self.AutoOpenFileCheckbutton])
        self.layout_list[1]["widgets_grid_params"].extend(
            [{"row":6, "column":1, "columnspan":1, "sticky":"E"},
             {"row":6, "column":2, "columnspan":1, "sticky":"W"}]
            )

        #border thickness
        self.BorderthicknessLabel = tk.Label(master=self.layout_list[1]["frame"], text="Border thickness: ")        
        self.BorderthicknessSpinBox = ttk.Spinbox(
            master=self.layout_list[1]["frame"],
            from_=self.BORDER_THICKNESS_RANGE[0],
            to=self.BORDER_THICKNESS_RANGE[1],
            width=5
            )
        self.BorderthicknessSpinBox.insert(0,10)

        self.layout_list[1]["widgets"].extend([self.BorderthicknessLabel, self.BorderthicknessSpinBox])
        self.layout_list[1]["widgets_grid_params"].extend(
            [{"row":7, "column":1, "columnspan":1, "sticky":"E"},
             {"row":7, "column":2, "columnspan":1, "sticky":"W"}]
            )

        #border color
        self.BordercolorLabel = tk.Label(master=self.layout_list[1]["frame"], text="Border color: ")
        self.BordercolorCombobox = ttk.Combobox(
            master=self.layout_list[1]["frame"],
            width=15,
            values=BORDER_COLORS_KEYS
            )
        self.BordercolorCombobox.current(0)

        self.layout_list[1]["widgets"].extend([self.BordercolorLabel, self.BordercolorCombobox])
        self.layout_list[1]["widgets_grid_params"].extend(
            [{"row":8, "column":1, "columnspan":1, "sticky":"E"},
             {"row":8, "column":2, "columnspan":1, "sticky":"W"}]
            )

        #outer border
        self.BorderOuterlabel = tk.Label(master=self.layout_list[1]["frame"],text="Border along outside: ")
        self.BorderOuterCheckbutton = tk.Checkbutton(
            master=self.layout_list[1]["frame"],
            onvalue=True,
            offvalue=False,
            variable=self.outerBorderOn_BoolVar,
            command=self.updateBorderOutside
            )
        
        self.layout_list[1]["widgets"].extend([self.BorderOuterlabel, self.BorderOuterCheckbutton])
        self.layout_list[1]["widgets_grid_params"].extend(
            [{"row":9, "column":1, "columnspan":1, "sticky":"E"},
             {"row":9, "column":2, "columnspan":1, "sticky":"W"}]
            )


    def packWidgets(self):
        self.Root.grid_columnconfigure(tk.ALL, weight=1)
        self.layout_list[0]["frame"].columnconfigure(0, weight=1)
        self.layout_list[1]["frame"].columnconfigure(tk.ALL, weight=1)

        for f,frame_dic in enumerate(self.layout_list):
            print("frame:", f)
            frame_dic["frame"].grid(**frame_dic["frame_grid"])

            for i,widget in enumerate(frame_dic["widgets"]):
                print("\twidget:", i)
                widget.grid(
                    **frame_dic["widgets_grid_params"][i],
                    pady = self.PAD
                    )

            

        """
        # new way
        for i,widget in enumerate(self.widget_list):
            widget.grid(
                pady = self.PAD,
                row = self.widget_packing_list[i]["row"],
                column = self.widget_packing_list[i]["col"],
                columnspan = self.widget_packing_list[i]["colspan"],
                sticky = self.widget_packing_list[i]["sticky"]
                )
        """
        """
        
        self.TitleLabel.grid(row=0, column=1, columnspan=3)
        self.DescriptorLabel.grid(row=1, column=1, columnspan=3)
        self.RunButton.grid(pady=5, row=2, column=1, columnspan=3, sticky="NSEW")

        
        self.OptionsSeparator.grid(pady=5, row=3, column=0, columnspan=5, sticky="EW")
        self.OptionsLabel.grid(pady=5, row=3, column=1, columnspan=3)

        self.filenameLabel.grid(pady=5, row=4, column=1, sticky="E")
        self.filenameEntry.grid(pady=5, row=4, column=2, sticky="EW")

        self.SaveDirLabel.grid(pady=5, row=5, column=1, sticky="E")
        self.SaveDirEntry.grid(pady=5, row=5, column=2, sticky="EW")
        self.SaveDirDialogButton.grid(pady=5, row=5, column=3, sticky="W")

        self.AutoOpenFilelabel.grid(pady=5, row=6, column=1, sticky="E")
        self.AutoOpenFileCheckbutton.grid(pady=5, row=6, column=2, sticky="W")
        
        self.BorderthicknessLabel.grid(pady=5, row=7, column=1, sticky="E")
        self.BorderthicknessSpinBox.grid(row=7, column=2, sticky="W")
        
        self.BordercolorLabel.grid(pady=5, row=8, column=1, sticky="E")
        self.BordercolorCombobox.grid(row=8, column=2, sticky="W")

        self.BorderOuterlabel.grid(pady=5, row=9, column=1, sticky="E")
        self.BorderOuterCheckbutton.grid(row=9, column=2, sticky="W")
        """

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

            if len(self.save_directory) < self.DISP_TEXT_LENGTH:
                self.SaveDirEntry['width'] = len(self.save_directory)
        print(len(self.save_directory), "path is now:", self.save_directory, self.saveDir_StrVar.get())
        
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
                self.FilenameEntry['width'] = len(self.filename)

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

            if (self.filename == "") or (self.filename == self.filename_default):
                print("using default filename...")
                self.filename = self.filename_default + (f" ({self.file_count})" * (self.file_count > 0))
                self.file_count += 1

            filename = self.save_directory +  "\\" + self.filename + self.FILE_FORMAT
            print("filename:", filename)

            self.Merger.mergeImages(img_obj_list, filename, color, border_thickness, outer_border_thickness)

            self.Merger.closeImages(img_obj_list)

            print("auto open checkbox value:", self.autoOpenFile_BoolVar.get())
            if self.autoOpenFile_BoolVar.get():
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
