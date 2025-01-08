import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinterdnd2 as tkDnD2
from datetime import datetime
import os
import platform
from pathlib import Path
import subprocess
import threading

from merger import Merger
from updater import Updater


DEV_MODE = True

BORDER_COLORS_DICT = {
    "white": (255,255,255,255),
    "black": (0,0,0,255),
    "red": (255,0,0,255),
    "blue": (0,0,255,255),
    "green": (0,255,0,255),
    "yellow": (255,255,0,255),
    "cyan": (0,255,255,255),
    "magenta": (255,0,255,255),
    "purple": (128,0,128,255),
    "transparent": (0,0,0,0)
    }
BORDER_COLORS_KEYS = list(BORDER_COLORS_DICT.keys())

MAX_IMAGE_DIMENSION = 5000
SIZE_PRESET_DICT = {
    "facebook": (1200, 630),
    "3000 wide": (3000,3000),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "1440p":(2560,1440),
    "3K": (3072, 1620)
}
SIZE_PRESET_KEYS = list(SIZE_PRESET_DICT.keys())


class Collager:

    def __init__(self, title, version_str):
        self.DEV_FRAME_BG_ON = False
        self.DEV_FRAME_COLORS = ["red", "blue", "green", "yellow", "cyan", "magenta", "purple"]

        self.Root = tkDnD2.Tk()
        self.Root.title(title + " " + version_str)
        self.Root.resizable(False, False)
        self.Root.withdraw() # so that adjustments can be made subtley

        

        #variables
        self.PAD = 5
        self.NUM_COLS = 6
        self.MAX_NUM_COLS = 50
        self.MAX_NUM_ROWS = 50 
        self.SPINBOX_WIDTH = 5
        self.COMBOBOX_WIDTH = 10
        self.BORDER_THICKNESS_RANGE = [0,50]
        self.DISP_TEXT_LENGTH = 100
        self.FILE_FORMAT= ".png"

        self.file_size = SIZE_PRESET_DICT[SIZE_PRESET_KEYS[0]]
        self.Merger = Merger(self.file_size, True)
        self.filename_default = datetime.today().strftime('%Y-%m-%d %I.%M.%S%p') + " merged"
        self.filename = ""
        self.file_count = 0
        self.save_directory = os.path.join(Path.home(), "Downloads")
        self.filenames_list = []
        self.filenames_widgets_list = []
        
        
        self.outerBorderOn_BoolVar = tk.BooleanVar(value=False)
        self.filename_StrVar = tk.StringVar(value = self.filename_default)
        self.saveDir_StrVar = tk.StringVar(value = self.save_directory)
        self.filenamesList_StrVar = tk.StringVar(value=self.filenames_list)
        self.autoOpenFile_BoolVar = tk.BooleanVar(value=True)
        self.autoOrient_BoolVar = tk.BooleanVar(value=True)

        self.filename_StrVar.trace_add("write", self.updateFilename)
        self.saveDir_StrVar.trace_add("write", self.updateSaveDir)


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
             "frame_grid":{"row":3, "column":0, "columnspan":self.NUM_COLS, "sticky":"EW", "padx":self.PAD, "pady":self.PAD},
             "widgets": [],
             "widgets_grid_params":[]
             }
             ,
            "left options":{
             "frame": tk.Frame(master=self.Root),
             "frame_grid":{"row":4, "column":0, "sticky":"NW", "padx":2*self.PAD, "pady":self.PAD},
             "widgets": [],
             "widgets_grid_params":[]
             },
            "right options":{
             "frame": tk.Frame(master=self.Root),
             "frame_grid":{"row":4, "column":1, "sticky":"NE", "padx":2*self.PAD, "pady":self.PAD},
             "widgets": [],
             "widgets_grid_params":[]
             }
        }
        
        
        self.makeMenubar()
        self.makeWidgets()
        self.packWidgets()
        self.updateFilename()
        print("updating save dir...")
        self.updateSaveDir()

    

    #-- Tkinter/GUI functions

    def makeMenubar(self):
        self.MenuBar = tk.Menu(self.Root)
        self.Root.config(menu=self.MenuBar)

        #file menu
        self.FileMenu = tk.Menu(self.MenuBar, tearoff=0)
        self.MenuBar.add_cascade(menu=self.FileMenu, label="File")
        self.FileMenu.add_command(label="Choose images...", command=self.getFilesWithDialog)
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label="Quit", command=self.quitApp)

        #run menu
        self.RunMenu = tk.Menu(self.MenuBar, tearoff=0)
        self.MenuBar.add_cascade(menu=self.RunMenu, label="Run")
        self.RunMenu.add_command(label="Run with current images", command=self.runCollager)

        #update menu
        self.UpdateMenu = tk.Menu(self.MenuBar, tearoff=0)
        self.MenuBar.add_cascade(menu=self.UpdateMenu, label="Update")
        self.UpdateMenu.add_command(label="Get Latest Update", command=self.getUpdate)
        


    def placeWindow(self):
        screen_width = self.Root.winfo_screenwidth()
        win_width = self.Root.winfo_width()

        x = int((screen_width/2) - (win_width)/2)
        y = 10 
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
        self.FilesListBox = tk.Listbox(
            master=self.layout_dict["file list"]["frame"],
            listvariable=self.filenamesList_StrVar,
            height=5 # # lines listed prior to being scrolled
            )
        self.FilesListBox.bind("<<ListboxSelect>>", self.getCurrentSelectedFile)
        
        self.layout_dict["file list"]["widgets"].append(self.FilesListBox)
        self.layout_dict["file list"]["widgets_grid_params"].append({"row":1, "column":0, "columnspan":self.NUM_COLS, "sticky":"NSEW"})

        # vertical scroll bar
        self.FileslistVertScrollbar = ttk.Scrollbar(
            master=self.layout_dict["file list"]["frame"],
            orient=tk.VERTICAL,
            command=self.FilesListBox.yview
        )
        self.FilesListBox.configure(yscrollcommand=self.FileslistVertScrollbar.set)
        self.layout_dict["file list"]["widgets"].append(self.FileslistVertScrollbar)
        self.layout_dict["file list"]["widgets_grid_params"].append({"row":1, "column":self.NUM_COLS, "sticky":"NS"})

        # horizontal scroll bar
        self.FileslistHoriScrollbar = ttk.Scrollbar(
            master=self.layout_dict["file list"]["frame"],
            orient=tk.HORIZONTAL,
            command=self.FilesListBox.xview
        )
        self.FilesListBox.configure(xscrollcommand=self.FileslistHoriScrollbar.set)
        self.layout_dict["file list"]["widgets"].append(self.FileslistHoriScrollbar)
        self.layout_dict["file list"]["widgets_grid_params"].append({"row":2, "column":0, "columnspan":self.NUM_COLS, "sticky":"NEW"})

        # clear all button
        self.ClearFilesButton = tk.Button(
            master=self.layout_dict["file list"]["frame"],
            text="Remove all",
            bg="salmon",
            command=self.clearFilesList
        )
        self.layout_dict["file list"]["widgets"].append(self.ClearFilesButton)
        self.layout_dict["file list"]["widgets_grid_params"].append({"row":3, "column":0, "sticky":"EW"})

        #remove selected button
        self.RemoveSelectedFileButton = tk.Button(
            master=self.layout_dict["file list"]["frame"],
            text="Remove selected",
            bg="salmon",
            command=self.clearSelectedFile
        )
        self.layout_dict["file list"]["widgets"].append(self.RemoveSelectedFileButton)
        self.layout_dict["file list"]["widgets_grid_params"].append({"row":3, "column":1, "sticky":"W"})

        # move up button
        self.FileUpButton = tk.Button(
            master=self.layout_dict["file list"]["frame"],
            text="File Up",
            command=self.moveFileUpList
        )
        self.layout_dict["file list"]["widgets"].append(self.FileUpButton)
        self.layout_dict["file list"]["widgets_grid_params"].append({"row":3, "column":self.NUM_COLS-2, "sticky":"EW"})

        # move down button
        self.FileDownButton = tk.Button(
            master=self.layout_dict["file list"]["frame"],
            text="File Down",
            command=self.moveFileDownList
        )
        self.layout_dict["file list"]["widgets"].append(self.FileDownButton)
        self.layout_dict["file list"]["widgets_grid_params"].append({"row":3, "column":self.NUM_COLS-1, "sticky":"EW"})


        ## run button frame
        self.RunButton = tk.Button(
            master=self.layout_dict["run button"]["frame"],
            text="Run",
            bg="light green",
            command=self.runCollager
        )
        self.layout_dict["run button"]["widgets"].append(self.RunButton)
        self.layout_dict["run button"]["widgets_grid_params"].append({"row":4, "column":round(self.NUM_COLS/2)-1, "columnspan":2, "sticky":"EW"})



        ### left options frame
        #separator/title
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


        # filename
        self.FilenameLabel = tk.Label(master=self.layout_dict["left options"]["frame"], text="Image name ")
        self.FilenameEntry = tk.Entry(master=self.layout_dict["left options"]["frame"], textvariable=self.filename_StrVar)
        
        self.layout_dict["left options"]["widgets"].extend([self.FilenameLabel, self.FilenameEntry])
        self.layout_dict["left options"]["widgets_grid_params"].extend(
            [{"row":1, "column":0, "sticky":"E"},
             {"row":1, "column":1, "sticky":"W"}]
            )
        

        # save directory
        self.SaveDirLabel = tk.Label(master=self.layout_dict["left options"]["frame"], text="Save to ")
        self.SaveDirEntry = tk.Entry(master=self.layout_dict["left options"]["frame"], textvariable=self.saveDir_StrVar)
        self.SaveDirDialogButton = tk.Button(master=self.layout_dict["left options"]["frame"], text="browse", command=self.updateSaveDirDialog)

        self.layout_dict["left options"]["widgets"].extend([self.SaveDirLabel, self.SaveDirEntry, self.SaveDirDialogButton])
        self.layout_dict["left options"]["widgets_grid_params"].extend(
            [{"row":2, "column":0, "columnspan":1, "sticky":"E"},
             {"row":2, "column":1, "columnspan":1, "sticky":"EW"},
             {"row":2, "column":2, "columnspan":1, "sticky":"W"}]
            )
    

        # auto open file
        self.AutoOpenFilelabel = tk.Label(master=self.layout_dict["left options"]["frame"], text="Open image afterwards")
        self.AutoOpenFileCheckbutton = tk.Checkbutton(
            master=self.layout_dict["left options"]["frame"],
            onvalue=True,
            offvalue=False,
            variable=self.autoOpenFile_BoolVar
            )
        self.layout_dict["left options"]["widgets"].extend([self.AutoOpenFilelabel, self.AutoOpenFileCheckbutton])
        self.layout_dict["left options"]["widgets_grid_params"].extend(
            [{"row":3, "column":1, "columnspan":1, "sticky":"E"},
             {"row":3, "column":2, "columnspan":1, "sticky":"W"}]
            )
        

        # auto orientation (EXIF)
        self.AutoOrientlabel = tk.Label(master=self.layout_dict["left options"]["frame"], text="Auto orient images (recommended)")
        self.AutoOrientCheckbutton = tk.Checkbutton(
            master=self.layout_dict["left options"]["frame"],
            onvalue=True,
            offvalue=False,
            variable=self.autoOrient_BoolVar
            )
        self.layout_dict["left options"]["widgets"].extend([self.AutoOrientlabel, self.AutoOrientCheckbutton])
        self.layout_dict["left options"]["widgets_grid_params"].extend(
            [{"row":4, "column":1, "columnspan":1, "sticky":"E"},
             {"row":4, "column":2, "columnspan":1, "sticky":"W"}]
            )
        


        ##right options
        ## separator
        self.CentreSeparator = ttk.Separator(master=self.layout_dict["right options"]["frame"], orient=tk.VERTICAL)
        self.layout_dict["right options"]["widgets"].append(self.CentreSeparator)
        self.layout_dict["right options"]["widgets_grid_params"].append(
            {"row":0, "column":0, "rowspan":9, "sticky":"NS", "padx":(0,2*self.PAD)}
            )
    
        # Set rows 
        self.SetRowsLabel = tk.Label(master=self.layout_dict["right options"]["frame"], text="Rows ")        
        self.SetRowsSpinBox = ttk.Spinbox(
            master=self.layout_dict["right options"]["frame"],
            from_=1,
            to_=self.MAX_NUM_ROWS,
            width=self.SPINBOX_WIDTH
            )
        self.SetRowsSpinBox.insert(0,1)

        self.layout_dict["right options"]["widgets"].extend([self.SetRowsLabel, self.SetRowsSpinBox])
        self.layout_dict["right options"]["widgets_grid_params"].extend(
            [{"row":0, "column":1, "columnspan":1, "sticky":"E"},
             {"row":0, "column":3, "columnspan":1, "sticky":"W"}]
            )

        # set cols
        self.SetColumnsLabel = tk.Label(master=self.layout_dict["right options"]["frame"], text="Columns ")        
        self.SetColumnsSpinBox = ttk.Spinbox(
            master=self.layout_dict["right options"]["frame"],
            from_=1,
            to_=self.MAX_NUM_COLS,
            width=self.SPINBOX_WIDTH
            )
        self.SetColumnsSpinBox.insert(0,1)

        self.layout_dict["right options"]["widgets"].extend([self.SetColumnsLabel, self.SetColumnsSpinBox])
        self.layout_dict["right options"]["widgets_grid_params"].extend(
            [{"row":1, "column":1, "columnspan":1, "sticky":"E"},
             {"row":1, "column":3, "columnspan":1, "sticky":"W"}]
            )
        
        ## Auto layout button
        self.AutoLayoutButton = tk.Button(
            master=self.layout_dict["right options"]["frame"],
            text="Auto layout",
            command=self.autoLayout
        )
        self.layout_dict["right options"]["widgets"].append(self.AutoLayoutButton)
        self.layout_dict["right options"]["widgets_grid_params"].append(
            {"row":0, "column":4, "rowspan":2, "sticky":"NS"}
            )




        #output size limit -------------------------------------------------------------------------------------------------------------------

        self.OutputSizeLabel = tk.Label(master=self.layout_dict["right options"]["frame"], text="Output \nimage size ")
        self.layout_dict["right options"]["widgets"].extend([self.OutputSizeLabel])
        self.layout_dict["right options"]["widgets_grid_params"].extend(
            [{"row":2, "column":1, "rowspan":3, "sticky":"E"}]
            )
        
        self.OutputSizeSeparator = ttk.Separator(master=self.layout_dict["right options"]["frame"], orient=tk.VERTICAL)
        self.layout_dict["right options"]["widgets"].append(self.OutputSizeSeparator)
        self.layout_dict["right options"]["widgets_grid_params"].append(
            {"row":2, "column":2, "rowspan":3, "sticky":"NS"}
            )
        
        self.SizeXLabel = tk.Label(master=self.layout_dict["right options"]["frame"], text="width (px) ")
        self.SizeXSpinBox = ttk.Spinbox(
            master=self.layout_dict["right options"]["frame"],
            from_=1,
            to_=MAX_IMAGE_DIMENSION,
            width=self.SPINBOX_WIDTH
            )
        self.SizeXSpinBox.insert(0,1)

        self.layout_dict["right options"]["widgets"].extend([self.SizeXLabel, self.SizeXSpinBox])
        self.layout_dict["right options"]["widgets_grid_params"].extend(
            [{"row":2, "column":3, "sticky":"E"},
             {"row":2, "column":4, "sticky":"W"}]
            )
        
        self.SizeYLabel = tk.Label(master=self.layout_dict["right options"]["frame"], text="height (px) ")
        self.SizeYSpinBox = ttk.Spinbox(
            master=self.layout_dict["right options"]["frame"],
            from_=1,
            to_=MAX_IMAGE_DIMENSION,
            width=self.SPINBOX_WIDTH
            )
        self.SizeYSpinBox.insert(0,1)

        self.layout_dict["right options"]["widgets"].extend([self.SizeYLabel, self.SizeYSpinBox])
        self.layout_dict["right options"]["widgets_grid_params"].extend(
            [{"row":3, "column":3, "sticky":"E"},
             {"row":3, "column":4, "sticky":"W"}]
            )
        

        # size presets
        self.SizePresetLabel = tk.Label(master=self.layout_dict["right options"]["frame"], text="Size Presets: ")
        self.SizePresetCombobox = ttk.Combobox(
            master=self.layout_dict["right options"]["frame"],
            width=self.COMBOBOX_WIDTH,
            values=SIZE_PRESET_KEYS
            )
        self.SizePresetCombobox.current(0)

        self.layout_dict["right options"]["widgets"].extend([self.SizePresetLabel, self.SizePresetCombobox])
        self.layout_dict["right options"]["widgets_grid_params"].extend(
            [{"row":4, "column":3, "sticky":"E"},
             {"row":4, "column":4, "sticky":"W"}]
            )
        


        #border thickness
        self.BorderthicknessLabel = tk.Label(master=self.layout_dict["right options"]["frame"], text="Border thickness ")        
        self.BorderthicknessSpinBox = ttk.Spinbox(
            master=self.layout_dict["right options"]["frame"],
            from_=self.BORDER_THICKNESS_RANGE[0],
            to=self.BORDER_THICKNESS_RANGE[1],
            width=self.SPINBOX_WIDTH
            )
        self.BorderthicknessSpinBox.insert(0,10)

        self.layout_dict["right options"]["widgets"].extend([self.BorderthicknessLabel, self.BorderthicknessSpinBox])
        self.layout_dict["right options"]["widgets_grid_params"].extend(
            [{"row":5, "column":1, "columnspan":1, "sticky":"E"},
             {"row":5, "column":3, "columnspan":1, "sticky":"W"}]
            )

        #border color
        self.BordercolorLabel = tk.Label(master=self.layout_dict["right options"]["frame"], text="Border color ")
        self.BordercolorCombobox = ttk.Combobox(
            master=self.layout_dict["right options"]["frame"],
            width=self.COMBOBOX_WIDTH,
            values=BORDER_COLORS_KEYS
            )
        self.BordercolorCombobox.current(0)

        self.layout_dict["right options"]["widgets"].extend([self.BordercolorLabel, self.BordercolorCombobox])
        self.layout_dict["right options"]["widgets_grid_params"].extend(
            [{"row":6, "column":1, "columnspan":1, "sticky":"E"},
             {"row":6, "column":3, "columnspan":2, "sticky":"W"}]
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
            [{"row":7, "column":1, "columnspan":1, "sticky":"E"},
             {"row":7, "column":3, "columnspan":1, "sticky":"W"}]
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
        self.placeWindow()
        self.Root.deiconify()



    #-- Sub process functions

    def getUpdate(self):
        msg_box_answer = tk.messagebox.askyesno(
            master=self.Root,
            title="Start update?",
            message="Start update?",
            detail="This will close the program. Do you want to proceed?",
            default="no"
            )
        
        if msg_box_answer:
            print("getting update")
            if DEV_MODE:
                updater_dest_path = os.path.join(Path.home(), "Downloads") + "\\update"
                if not os.path.isdir(updater_dest_path):
                    os.mkdir(updater_dest_path)
                UpdaterObj = Updater(updater_dest_path)
            else:
                UpdaterObj = Updater(os.getcwd())
            threading.Thread(target=UpdaterObj.run, daemon=False).start()
            self.quitApp()



    #-- Customization Variables

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


    def getLayout(self):
        rows = self.SetRowsSpinBox.get()
        cols = self.SetColumnsSpinBox.get()

        if rows.isdigit() and cols.isdigit():
            return int(rows), int(cols)


    def autoLayout(self):
        num_images = len(self.filenames_list)
        r, c = self.Merger.determineLayout(num_images)
        print("autolayout:", r, c)

        self.SetRowsSpinBox.set(r)
        self.SetColumnsSpinBox.set(c)



    #-- file list functions

    def getCurrentSelectedFile(self, event=None):
        file = self.FilesListBox.curselection()
        print("current file selected in image list is:", file)
        return file

    def updateFilesList(self, new_files):
        for f in new_files:
            if f not in self.filenames_list:
                self.filenames_list.append(f)
        self.filenamesList_StrVar.set(self.filenames_list)

    def getFilesWithDialog(self):
        files_str = filedialog.askopenfilenames(title="Select images")
        image_files_list = self.Root.tk.splitlist(files_str)

        for i in image_files_list:
            print("file selected:", i)
        
        self.updateFilesList(image_files_list)

    def dragDropFiles(self, event):
        #process drag and drop string
        files_list_str = event.data[1:]
        files_list_str = files_list_str[:len(files_list_str)-1]
        files_list = files_list_str.split("} {")

        for i in files_list:
            print("file dragged and dropped:", i)

        self.updateFilesList(files_list)

    def clearFilesList(self):
        print("clearing file list")
        self.filenames_list = []
        self.filenamesList_StrVar.set(self.filenames_list)

    def clearSelectedFile(self):
        print("clearing selected file")
        selected = self.getCurrentSelectedFile()
        print("selected:", selected)
        self.filenames_list.pop(selected[0])
        self.filenamesList_StrVar.set(self.filenames_list)

    def moveFileInList(self, direction="up"):
        selection = self.FilesListBox.curselection()
        if len(selection) != 0:
            index = selection[0]
            print(f"i: {selection}, file: {self.filenames_list[index]}")

            if direction == "up":
                switch_index = index - 1
            elif direction == "down":
                switch_index = index + 1

            if (switch_index >= 0) and (switch_index < len(self.filenames_list)):
                #switch
                self.filenames_list[switch_index], self.filenames_list[index] = self.filenames_list[index], self.filenames_list[switch_index]
                self.updateFilesList([]) #not adding any files
                
                #make it so that when the user moves it, the selection stays on the same file
                self.FilesListBox.selection_clear(first=index)
                self.FilesListBox.selection_set(switch_index)
                self.FilesListBox.see(switch_index)

    def moveFileUpList(self):
        self.moveFileInList("up")

    def moveFileDownList(self):
        self.moveFileInList("down")


    
    #-- Program Operation functions

    def quitApp(self):
        print("quiting " + self.Root.title())
        self.Root.destroy()
        exit()

    def runCollager(self):

        #update varaibels
        color = self.updateBorderColor()
        border_thickness = self.updateBorderThickness()
        is_border = self.outerBorderOn_BoolVar.get() #self.updateBorderOutside()
        outer_border_thickness = is_border *  border_thickness


        auto_orient = self.autoOrient_BoolVar.get()
        layout = self.getLayout()
        print("raw layout:", layout)

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

            filename = self.save_directory +  "/" + self.filename + self.FILE_FORMAT
            print("filename:", filename)

            self.Merger.mergeImages(img_obj_list, layout, filename, color, border_thickness, outer_border_thickness)

            self.Merger.closeImages(img_obj_list)

            print("auto open checkbox value:", self.autoOpenFile_BoolVar.get())
            if self.autoOpenFile_BoolVar.get():
                if platform.system() == "Darwin":
                    subprocess.run(["/usr/bin/open", filename])
                elif platform.system() == "Windows":
                    os.startfile(filename)
                
        else:
            print("no images selected/cancelled")


    def run(self):
        self.Root.mainloop()
