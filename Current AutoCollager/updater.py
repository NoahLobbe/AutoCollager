import requests
import os
from pathlib import Path

URL = "https://api.github.com/repos/NoahLobbe/AutoCollager/releases/latest"
R = requests.get(URL)

print(
  R.json()["name"],
  R.json()["tag_name"],
  R.json()["assets_url"],
  len(R.json()["assets"])
      )



save_directory = str(os.path.join(Path.home(), "Downloads"))
headers = {"accept": "application/octet-stream"}

print("downloading files...")

for i,dic in enumerate(R.json()["assets"]):
  print(i, dic["url"], dic["name"])

  AssetResponse = requests.get(dic["url"]) #, headers=headers)
  filepath = save_directory + "\\" + dic["name"]
  with open(filepath, "wb") as file:
    file.write(AssetResponse.content)







'''
Z = requests.get(R.json()["zipball_url"])
print(Z.status_code)
with open(file, "wb") as fd:
    fd.write(Z.content)
'''