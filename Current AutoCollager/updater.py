import requests
import os
from tkinter import messagebox


class Updater:
  def __init__(self, installation_path):
    self.dest = installation_path
    if not os.path.isdir(self.dest):
      os.mkdir(self.dest)


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
  from pathlib import Path
  from tkinter import filedialog

  update_dest = filedialog.askdirectory(title="Select Update destination...")

  if not os.path.isdir(update_dest):
    update_dest = str(os.path.join(Path.home(), "Downloads\\update"))
    if not os.path.isdir(update_dest):
      os.mkdir(update_dest)

  print("running updater independantly")
  App = Updater(update_dest)
  App.run()
