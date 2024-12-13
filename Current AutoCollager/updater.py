import requests
import os
from pathlib import Path

URL = "https://api.github.com/repos/NoahLobbe/AutoCollager/releases/latest"
R = requests.get(URL)

print(
  R.json()["name"],
  R.json()["tag_name"],
  R.json()["assets_url"],
  R.json()["zipball_url"]
      )

save_directory = str(os.path.join(Path.home(), "Downloads"))
file = save_directory + "\\" + "output.zip"

Z = requests.get(R.json()["zipball_url"])
print(Z.status_code)
with open(file, "wb") as fd:
    fd.write(Z.content)