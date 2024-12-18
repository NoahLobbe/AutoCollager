import os
import sys
import platform
from tkinter import messagebox
import subprocess
import importlib.util


class Updater:

  def __init__(self, installation_path):
    self.dest = installation_path
    self.virtual_env_name = ".venv"
    self.virtual_env_path  = self.dest + "/" + self.virtual_env_name
    
    #make sure its real
    if not os.path.isdir(self.dest):
      self._errorWindow("Update installation path failed; it doesn't exist!")

    #check there is a virtual env
    if not os.path.isdir(self.virtual_env_path):
      print(self.virtual_env_path)
      self._errorWindow(f"Update installation path invalid; virtual environment folder ({self.virtual_env_name}) doesn't exist!") 

    #check that non standard modules are installed
    requests_spec = importlib.util.find_spec("requests")
    print("checking requests,", requests_spec)
    if requests_spec is None:
      print("installing 'requests'...")
      subprocess.call([sys.executable, "-m", "pip", "install", "requests"]) #needs to be blocking
      
    global requests
    import requests


  def _errorWindow(self, msg, title="Uh oh!", _quit=True):
    messagebox.showinfo(title=title, message=title, detail=msg)
    if _quit:
      quit()


  def run(self):
    #download source code
    RepoResponse = requests.get("https://api.github.com/repos/NoahLobbe/AutoCollager/releases/latest")

    if RepoResponse.status_code != 200:
      print("failed response to repo...check internet connection?")
      self._errorWindow("Failed to connect to code repository. Please check internet connection.")

    else:
      print("repo status code is 200!")

    for i, asset_dict in enumerate(RepoResponse.json()["assets"]):
      
      AssetResponse = requests.get(asset_dict["url"], headers={"accept": "application/octet-stream"})
      file = self.dest + "/" + asset_dict["name"]

      print(f"asset {i}: status code {AssetResponse.status_code}, asset file {file}")
      with open(file, "wb") as f:
        f.write(AssetResponse.content)


    #install modules
    python_path = self.virtual_env_path
    if platform.system() == "Darwin":
        python_path += "/bin/python"
    elif platform.system() == "Windows":
        python_path += "/Scripts/python"
    
    print("python path:", python_path)
    #f = open(self.dest+"\\lol.txt", "w")
    subprocess.call([python_path, "-m", "pip", "install", "-r", self.dest + "/requirements.txt"])
    #subprocess.call([python_path, "-m", "pip", "freeze"], stdout=f, stderr=f)


if __name__ == "__main__":

  from pathlib import Path
  from tkinter import filedialog


  update_dest = filedialog.askdirectory(title="Select Update destination...")
  '''
  if not os.path.isdir(update_dest):
    update_dest = str(os.path.join(Path.home(), "Documents\\AutoCollager"))
    if not os.path.isdir(update_dest):
      os.mkdir(update_dest)
  '''

  print("running updater independantly")
  App = Updater(update_dest)
  App.run()
