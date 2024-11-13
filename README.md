# AutoCollager

## Installation
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


## To Do list
- [ ] User able to change file name of image
- [ ] User able to change file save destination
- [ ] Run button instead of automatically running
- [ ] File input list. E.g. user can add files one by one if neccessary, which adds a widget with the file name
- [ ] (Low priority) Figure out how to change task/tool bar icon for program. For Version 2.1 using Apple's Automator to run the program does **NOT** allow `tkinter` to change the icon
- [ ] Make an installer


## Versions
Version number is `x.y`, where
- `x` is the major number, which increases when a feature is added
- `y` is the update number, increases when a fix has been issued or it has been re-written to optimise or clean up code

Current version is always `AutoCollager`, and past versions are in `SS`.

### Version 1
very rough quick version

### Version 2.0
Really big leap, works a lot better.

### Version 2.1
Temporary fix for images that requiring reading EXIF data to orient image properly. Bug was found on Mac.
Fix was to always rotate the final image. Also, rescaled the image to have a width of 1200px so that the image is a reasonable size (not *cough* 215MB...)

### Version 3 (current)
