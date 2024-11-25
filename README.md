# AutoCollager

## Installation
Note: dependencies can be seen in [`requirements.txt`](AutoCollager/requirements.txt).
1. Install Python
2. Download this package
3. Setup virtual environment
   - Windows
     - `> py -m venv .venv`
     - `> call .venv/Scripts/activate`
     - `(.venv) C:\path\to\directory> pip install requirements.txt`
   - Mac
     - `$ python3 -m venv .venv`
     - `$ source .venv/bin/activate`
     - `(.venv) path/to/directory/$ pip install requirements.txt`

## Useage
### Windows
Haven't done yet...

### Mac
Create an Automator file to activate the virtual environment, run `main.py`, and then deactivate the virtual environment when finished.


## Versions
Version number is `x.y`, where
- `x` is the major number, which increases when a feature is added
- `y` is the update number, increases when a fix has been issued or it has been re-written to optimise or clean up code

Current version is always [`AutoCollager`](AutoCollager/).

### Version 1
very rough quick version

### Version 2.0
Really big leap, works a lot better.

### Version 2.1
Temporary fix for images that requiring reading EXIF data to orient image properly. Bug was found on Mac.
Fix was to always rotate the final image. Also, rescaled the image to have a width of 1200px so that the image is a reasonable size (not *cough* 215MB...)

### Version 3 (current)

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
- [ ] Run button instead of automatically running
- [ ] Change text for file select button to be more descriptive and list acceptable file types
  - [ ] add file type checking so that won't try to use images that PIL can't
- [ ] File input list. E.g. user can add files one by one if neccessary, which adds a widget with the file name
- [ ] (Low priority) Figure out how to change task/tool bar icon for program. For Version 2.1 using Apple's Automator to run the program does **NOT** allow `tkinter` to change the icon
- [ ] Make an installer