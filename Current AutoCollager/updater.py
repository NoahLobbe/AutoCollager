import requests
import os
from pathlib import Path
import subprocess
import signal
import sys
import ctypes
import platform
from tkinter import messagebox
from tkinter import filedialog


def func(*args):
  #print(args)

  print("killing caller script")
  print("child? PID", os.getpid())
  URL = "https://api.github.com/repos/NoahLobbe/AutoCollager/releases/latest"
  R = requests.get(URL)

  print(
    R.json()["name"],
    R.json()["tag_name"],
    R.json()["assets_url"]
    )

  downloads_path = str(os.path.join(Path.home(), "Downloads"))
  target_path = downloads_path + "\\assets"
  if not os.path.exists(target_path):
    os.mkdir(target_path)
  print("made folder", target_path)


  for i, dic in enumerate(R.json()["assets"]):
    print(i, dic["name"], dic["url"])

    file = target_path + "\\" + dic["name"]
    asset_response = requests.get(dic["url"], headers={"accept": "application/octet-stream"})
    print(asset_response.status_code)

    with open(file, "wb") as f:
      f.write(asset_response.content)

  print("\n\ndone updating...")







class Updater:
  def __init__(self, installation_path):
    self.dest = installation_path
    #self.Root = tk.Tk()

  def run(self):
    
    RepoResponse = requests.get("https://api.github.com/repos/NoahLobbe/AutoCollager/releases/latest")

    if RepoResponse.status_code != 200:
      print("failed response to repo...check internet connection?")
      messagebox.showinfo(
        title="Uh oh!", 
        message="Uh oh!", 
        detail="Failed to connect to code repository. Please check internet connection. "
        )
      quit()
    else:
      print("repo status code is 200!")

    for i, asset_dict in enumerate(RepoResponse.json()["assets"]):
      
      AssetResponse = requests.get(asset_dict["url"], headers={"accept": "application/octet-stream"})
      file = self.dest + "\\" + asset_dict["name"]

      print(f"asset {i}: status code {AssetResponse.status_code}, asset file {file}")
      with open(file, "wb") as f:
        f.write(AssetResponse.content)



if __name__ == "__main__":
  update_dest = filedialog.askdirectory(title="Select Update destination...")

  if not os.path.isdir(update_dest):
    update_dest = str(os.path.join(Path.home(), "Downloads\\update"))
    if not os.path.isdir(update_dest):
      os.mkdir(update_dest)

  print("running updater independantly")
  App = Updater(update_dest)
  App.run()
