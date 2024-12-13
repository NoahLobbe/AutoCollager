import requests
import os
from pathlib import Path
import subprocess
import sys



def func(*args):
  print(args)

  print("killing caller script")
  #subprocess.Popen.terminate(["main.py"])

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


if __name__ == "__main__":
  func()