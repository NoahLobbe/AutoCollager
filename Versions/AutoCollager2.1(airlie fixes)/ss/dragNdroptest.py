from tkinter import TOP, Entry, Label, StringVar
import tkinterdnd2 as tkDnD2


def get_path(event):
    pathLabel.configure(text = event.data)
    
    filelist = event.data.split("} {")

    for file in filelist:
        print(file)
    

root = tkDnD2.Tk()
root.geometry("350x100")
root.title("Get file path")

nameVar = StringVar()

entryWidget = Entry(root)
entryWidget.pack(side=TOP, padx=5, pady=5)

pathLabel = Label(root, text="Drag and drop file in the entry box")
pathLabel.pack(side=TOP)

entryWidget.drop_target_register(tkDnD2.DND_ALL)
entryWidget.dnd_bind("<<Drop>>", get_path)

root.mainloop()
