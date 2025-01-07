# AutoCollager

## Installation
1. Install [Python](https://www.python.org/)
2. Setup virtual environment in desired location.
   - Windows
     - `> py -m venv .venv`
   - Mac
     - `$ python3 -m venv .venv`
3. Download [`updater.py`](https://github.com/NoahLobbe/AutoCollager/releases/latest/download/updater.py)
4. Run `updater.py` using IDLE or from terminal. Automatically installs `requests` if not in main python installation, and then installs `requirements.txt` in virtual environment (`.venv`)
    - Windows Command line
      - `py updater.py`
    - Mac Terminal
      - Will probably have some popups asking for permissions to folders or use of terminal
      - `python3 updater.py`
5. Make/use a quick launcher
    - Mac
      - Automator
      - `cd Documents/AutoCollager`
      - `source .venv/bin/activate`
      - `python main.py`
      - `source deactivate`
      - `echo "AutoCollager closed` (not neccessary)


## Versions
Version number is `x.y`, where
- `x` is the major number, which increases when a feature is added
- `y` is the update number, increases when a fix has been issued or it has been re-written to optimise or clean up code


### Version 1
very rough quick version

### Version 2.0
Really big leap, works a lot better.

### Version 2.1
Temporary fix for images that requiring reading EXIF data to orient image properly. Bug was found on Mac.
Fix was to always rotate the final image. Also, rescaled the image to have a width of 1200px so that the image is a reasonable size (not *cough* 215MB...)

### Release v3.0

#### To Do list
- [x] User able to change file name of image 
- [x] User able to change file save destination 
- [x] Counter to adjust file name for each generation if left on default name
- [x] Checkbox that controls whether the image is automatically opened after generation
- [x] Make `requirements.txt`
- [x] Put all widgets into a list so that when a widget is added all the row numbers (for packing) don't need to be changed. In fact, make the row numbers based on the objects' position in the list. All the packing (using `grid()`) info will be in a parrallel list
- [x] Make 2 separate `frame`s, one for the actually frequent interacting widgets, and then the second one is for the customisation/options widgets
- [x] Read EXIF data on images to rotate images to correct orientation. However, the program is not smart enough to detect whether a book's orientation is contridicting the EXIf data or not, and fix it. Thanks to `jdhao` for his page on the values for EXIF orientation [JPEG Image Orientation and Exif](https://web.archive.org/web/20241110203841/https://jdhao.github.io/2019/07/31/image_rotation_exif_info/)
- [x] Make checkbox for EXIF (auto orientation), default on
- [x] Run button instead of automatically running
- [x] Make a widget for each filename so that the user can seen them listed
- [x] Make an updater menubar and script that pulls latest release from Github
- [ ] Change filename list to a single Text widget with scroll bar so that the App window doesn't get super long
- [ ] Add Button to clear selected files
- [ ] Change text for file select button to be more descriptive and list acceptable file types
  - [ ] add file type checking so that won't try to use images that PIL can't
- [ ] File input list. E.g. user can add files one by one if neccessary, which adds a widget with the file name
- [ ] (Low priority) Figure out how to change task/tool bar icon for program. For Version 2.1 using Apple's Automator to run the program does **NOT** allow `tkinter` to change the icon
- [ ] Make an installer script so that it downloads and runs everything

### Release v3.1
Some debugging on Mac

### Release v3.2 
#### To Do list
- [x] User can now add files one by one. Just had to append new files to current file list, not overwrite! :D
- [x] Change filename list to a single Text widget with scroll bar so that the App window doesn't get super long
  - Used Tkinter Listbox and scrollbars (SO COOL!)
- [x] Add Button to clear selected files

### Current Development
#### To Do list (Updater)
- [ ] Cleanup code
- [ ] Have a simple GUI so that user can see what is going on and knows when it is finished

#### To Do list (Main program)
- [ ] Add proper logging so that i just read text files instead of having to open everything in debug mode
- [ ] background colors of buttons doesn't show up on Mac
- [ ] Icon for windows
- [ ] in file list, just show file names, not whole path as it is harder to read.
- [ ] Add button to get remove currently selected file
- [ ] maybe add a widget that subtley (NO POPUPS!) that there is an updater available. Maybe upper right corner???
- [ ] Some sort of preview of placement? Maybe just a grid with filenames instead of actual images. To get preview maybe make a Toplevel window?
- [ ] Add a configuration file for some basic customisations. Can also be an easier way for the updater to updater a version str which is passed to the program title
