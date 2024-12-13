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
    "red": (255,0,0,255),
    "blue": (0,255,0,255),
    "green": (0,0,255,255),
    "yellow": (255,255,0,255),
    "cyan": (0,255,255,255),
    "magenta": (255,0,255,255),
    "purple": (128,0,128,255),
    "transparent": (0,0,0,0)
    }
BORDER_COLORS_KEYS = list(BORDER_COLORS_DICT.keys())


class Collager:

    def __init__(self, title, version_str):
        self.DEV_FRAME_BG_ON = False
        self.DEV_FRAME_COLORS = ["red", "blue", "green", "yellow", "cyan", "magenta", "purple"]

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
        self.filenames_list = []
        self.filenames_widgets_list = []
        self.file_list_frame_parent_widget_index = None
        
        self.outerBorderOn_BoolVar = tk.BooleanVar(value=True)
        self.filename_StrVar = tk.StringVar(value = self.filename_default)
        self.saveDir_StrVar = tk.StringVar(value = self.save_directory)
        self.autoOpenFile_BoolVar = tk.BooleanVar(value=True)
        self.autoOrient_BoolVar = tk.BooleanVar(value=True)

        self.filename_StrVar.trace_add("write", self.updateFilename)
        self.saveDir_StrVar.trace_add("write", self.updateSaveDir)

        self.widget_list = []
        self.widget_packing_list = []


        """
        ---------------------
        |       frame       |
        --------------------
        |       frame       |
        ---------------------
        |       frame       |
        ---------------------
        |       frame       |
        ---------------------
        | frame   | frame   |
        ---------------------
        """
        self.layout_dict =  {
            "top running":{
             "frame": tk.Frame(master=self.Root),
             "frame_grid":{"row":0, "column":0, "columnspan":self.NUM_COLS, "sticky":"EW", "padx":self.PAD, "pady":self.PAD},
             "widgets": [],
             "widgets_grid_params":[]
             },
            "file list":{
             "frame": tk.Frame(master=self.Root),
             "frame_grid":{"row":1, "column":0, "columnspan":self.NUM_COLS, "sticky":"EW", "padx":self.PAD, "pady":self.PAD},
             "widgets": [],
             "widgets_grid_params":[]
             },
             "run button":{
             "frame": tk.Frame(master=self.Root),
             "frame_grid":{"row":2, "column":0, "columnspan":self.NUM_COLS, "sticky":"EW", "padx":self.PAD, "pady":self.PAD},
             "widgets": [],
             "widgets_grid_params":[]
             },
            "top options":{
             "frame": tk.Frame(master=self.Root),
             "frame_grid":{"row":3, "column":0, "columnspan":2, "sticky":"EW", "padx":self.PAD, "pady":self.PAD},
             "widgets": [],
             "widgets_grid_params":[]
             }
             ,
            "left options":{
             "frame": tk.Frame(master=self.Root),
             "frame_grid":{"row":4, "column":0, "sticky":"NW", "padx":self.PAD, "pady":self.PAD},
             "widgets": [],
             "widgets_grid_params":[]
             },
            "right options":{
             "frame": tk.Frame(master=self.Root),
             "frame_grid":{"row":4, "column":1, "sticky":"NE", "padx":self.PAD, "pady":self.PAD},
             "widgets": [],
             "widgets_grid_params":[]
             }
        }
        

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
        ##frame 0
        #title
        self.TitleLabel = tk.Label(
            master=self.layout_dict["top running"]["frame"],
            text="Auto Collager",
            font=("TkDefaultFont", 16)
            )
        self.layout_dict["top running"]["widgets"].append(self.TitleLabel)
        self.layout_dict["top running"]["widgets_grid_params"].append({"row":0, "column":0, "columnspan":self.NUM_COLS, "sticky":"EW"})


        #file select button button
        self.SelectFilesButton = tk.Button(
            master=self.layout_dict["top running"]["frame"],
            text="Click to choose images \nor \nDrag 'n' Drop \n",
            relief=tk.GROOVE,
            height=10,
            command=self.getFilesWithDialog
            )
        self.SelectFilesButton.drop_target_register(tkDnD2.DND_ALL)
        self.SelectFilesButton.dnd_bind("<<Drop>>", self.dragDropFiles)

        self.layout_dict["top running"]["widgets"].append(self.SelectFilesButton)
        self.layout_dict["top running"]["widgets_grid_params"].append({"row":1, "column":0, "columnspan":self.NUM_COLS, "sticky":"NSEW"})

        #filelist label
        '''
        self.FilesListLabel = tk.Label(
            master=self.layout_dict["file list"]["frame"],
            text="Files:"
            )
        self.layout_dict["file list"]["widgets"].append(self.FilesListLabel)
        self.layout_dict["file list"]["widgets_grid_params"].append({"row":0, "column":0, "sticky":"EW"})
        '''

        ##run button frame
        self.RunButton = tk.Button(
            master=self.layout_dict["run button"]["frame"],
            text="Run",
            bg="light green",
            command=self.runCollager
        )
        self.layout_dict["run button"]["widgets"].append(self.RunButton)
        self.layout_dict["run button"]["widgets_grid_params"].append({"row":4, "column":2, "columnspan":1, "sticky":"EW"})


        ##frame 
        #options
        self.OptionsSeparator = ttk.Separator(master=self.layout_dict["top options"]["frame"], orient=tk.HORIZONTAL)   
        self.OptionsLabel = tk.Label(
            master=self.layout_dict["top options"]["frame"],
            text="Customisation",
            font=("TkDefaultFont", 14)
            )
        self.layout_dict["top options"]["widgets"].extend([self.OptionsSeparator, self.OptionsLabel])
        self.layout_dict["top options"]["widgets_grid_params"].extend(
            [{"row":0, "column":0, "columnspan":self.NUM_COLS, "sticky":"EW"},
             {"row":0, "column":0, "columnspan":self.NUM_COLS}]
            )


        #filename
        self.FilenameLabel = tk.Label(master=self.layout_dict["top options"]["frame"], text="Image name ")
        self.FilenameEntry = tk.Entry(master=self.layout_dict["top options"]["frame"], textvariable=self.filename_StrVar)
        
        self.layout_dict["top options"]["widgets"].extend([self.FilenameLabel, self.FilenameEntry])
        self.layout_dict["top options"]["widgets_grid_params"].extend(
            [{"row":2, "column":0, "sticky":"E"},
             {"row":2, "column":1, "sticky":"W"}]
            )

        #save directory
        self.SaveDirLabel = tk.Label(master=self.layout_dict["top options"]["frame"], text="Save to ")
        self.SaveDirEntry = tk.Entry(master=self.layout_dict["top options"]["frame"], textvariable=self.saveDir_StrVar)
        self.SaveDirDialogButton = tk.Button(master=self.layout_dict["top options"]["frame"], text="browse", command=self.updateSaveDirDialog)

        self.layout_dict["top options"]["widgets"].extend([self.SaveDirLabel, self.SaveDirEntry, self.SaveDirDialogButton])
        self.layout_dict["top options"]["widgets_grid_params"].extend(
            [{"row":3, "column":0, "columnspan":1, "sticky":"E"},
             {"row":3, "column":1, "columnspan":1, "sticky":"EW"},
             {"row":3, "column":2, "columnspan":1, "sticky":"W"}]
            )
        

        ##frame 
        #auto open file
        self.AutoOpenFilelabel = tk.Label(master=self.layout_dict["left options"]["frame"], text="Open image afterwards")
        self.AutoOpenFileCheckbutton = tk.Checkbutton(
            master=self.layout_dict["left options"]["frame"],
            onvalue=True,
            offvalue=False,
            variable=self.autoOpenFile_BoolVar
            )
        self.layout_dict["left options"]["widgets"].extend([self.AutoOpenFilelabel, self.AutoOpenFileCheckbutton])
        self.layout_dict["left options"]["widgets_grid_params"].extend(
            [{"row":4, "column":1, "columnspan":1, "sticky":"E"},
             {"row":4, "column":2, "columnspan":1, "sticky":"W"}]
            )
        
        #auto orientation (EXIF)
        self.AutoOrientlabel = tk.Label(master=self.layout_dict["left options"]["frame"], text="Auto orient images (recommended)")
        self.AutoOrientCheckbutton = tk.Checkbutton(
            master=self.layout_dict["left options"]["frame"],
            onvalue=True,
            offvalue=False,
            variable=self.autoOrient_BoolVar
            )
        self.layout_dict["left options"]["widgets"].extend([self.AutoOrientlabel, self.AutoOrientCheckbutton])
        self.layout_dict["left options"]["widgets_grid_params"].extend(
            [{"row":5, "column":1, "columnspan":1, "sticky":"E"},
             {"row":5, "column":2, "columnspan":1, "sticky":"W"}]
            )


        ##frame 
        #border thickness
        self.BorderthicknessLabel = tk.Label(master=self.layout_dict["right options"]["frame"], text="Border thickness ")        
        self.BorderthicknessSpinBox = ttk.Spinbox(
            master=self.layout_dict["right options"]["frame"],
            from_=self.BORDER_THICKNESS_RANGE[0],
            to=self.BORDER_THICKNESS_RANGE[1],
            width=5
            )
        self.BorderthicknessSpinBox.insert(0,10)

        self.layout_dict["right options"]["widgets"].extend([self.BorderthicknessLabel, self.BorderthicknessSpinBox])
        self.layout_dict["right options"]["widgets_grid_params"].extend(
            [{"row":7, "column":1, "columnspan":1, "sticky":"E"},
             {"row":7, "column":2, "columnspan":1, "sticky":"W"}]
            )

        #border color
        self.BordercolorLabel = tk.Label(master=self.layout_dict["right options"]["frame"], text="Border color ")
        self.BordercolorCombobox = ttk.Combobox(
            master=self.layout_dict["right options"]["frame"],
            width=15,
            values=BORDER_COLORS_KEYS
            )
        self.BordercolorCombobox.current(0)

        self.layout_dict["right options"]["widgets"].extend([self.BordercolorLabel, self.BordercolorCombobox])
        self.layout_dict["right options"]["widgets_grid_params"].extend(
            [{"row":8, "column":1, "columnspan":1, "sticky":"E"},
             {"row":8, "column":2, "columnspan":1, "sticky":"W"}]
            )

        #outer border
        self.BorderOuterlabel = tk.Label(master=self.layout_dict["right options"]["frame"],text="Outside border")
        self.BorderOuterCheckbutton = tk.Checkbutton(
            master=self.layout_dict["right options"]["frame"],
            onvalue=True,
            offvalue=False,
            variable=self.outerBorderOn_BoolVar,
            command=self.updateBorderOutside
            )
        
        self.layout_dict["right options"]["widgets"].extend([self.BorderOuterlabel, self.BorderOuterCheckbutton])
        self.layout_dict["right options"]["widgets_grid_params"].extend(
            [{"row":9, "column":1, "columnspan":1, "sticky":"E"},
             {"row":9, "column":2, "columnspan":1, "sticky":"W"}]
            )


    def packWidgets(self):
        #configs
        self.Root.columnconfigure(tk.ALL, weight=1)
        for key,dic in self.layout_dict.items():
            dic["frame"].columnconfigure(list(range(self.NUM_COLS)), weight=1)

        #packing
        f = 0
        for key,frame_dic in self.layout_dict.items():
            if self.DEV_FRAME_BG_ON:
                frame_dic["frame"]["bg"] = self.DEV_FRAME_COLORS[f]
                f += 1
            
            frame_dic["frame"].grid(**frame_dic["frame_grid"])

            for i,widget in enumerate(frame_dic["widgets"]):
                widget.grid(**frame_dic["widgets_grid_params"][i],pady = self.PAD)

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


    def updateFileList(self):
        print("cycling through...")

        #clear widgets
        for widget in self.filenames_widgets_list:
            widget.destroy()

        #add widgets
        for i, filepath in enumerate(self.filenames_list):
            _, filename = os.path.split(filepath)
            
            print("\twidget for", filename)

            fileWidget = tk.Entry(
                    master=self.layout_dict["file list"]["frame"]
                )
            fileWidget.configure(disabledbackground="light gray", disabledforeground="black")
            fileWidget.insert(0, filename)
            fileWidget.grid(row=i, column=0, columnspan=self.NUM_COLS-1, sticky="WE")
            fileWidget["state"] = "disabled"

            self.filenames_widgets_list.append(fileWidget)

        self.Root.update()

    
    def getFilesWithDialog(self):
        files_str = filedialog.askopenfilenames(title="Select images")
        image_files_list = self.Root.tk.splitlist(files_str)

        for i in image_files_list:
            print("file selected:", i)
        
        self.filenames_list = image_files_list

        print("updaying file list widgets")
        self.updateFileList()

    def dragDropFiles(self, event):
        #process drag and drop string
        files_list_str = event.data[1:]
        files_list_str = files_list_str[:len(files_list_str)-1]
        files_list = files_list_str.split("} {")

        for i in files_list:
            print("file dragged and dropped:", i)

        self.filenames_list = files_list
        #print("running collager...")
        #self.runCollager(files_list, True)
        print("updaying file list widgets")
        self.updateFileList()


    def runCollager(self):

        #update varaibels
        color = self.updateBorderColor()
        border_thickness = self.updateBorderThickness()
        is_border = self.outerBorderOn_BoolVar.get() #self.updateBorderOutside()
        outer_border_thickness = is_border *  border_thickness
        auto_orient = self.autoOrient_BoolVar.get()

        '''
        #get images
        if (image_files_list == None) and not dragged_dropped:
            files_str = filedialog.askopenfilenames(title="Select images")
            image_files_list = self.Root.tk.splitlist(files_str)

            for i in image_files_list:
                print("file selected:", i)
        '''
        
        if len(self.filenames_list) > 1:
        
            img_obj_list = self.Merger.openImages(self.filenames_list, auto_orient)

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



    def run(self):
        
        self.Root.mainloop()