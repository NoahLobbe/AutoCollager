from PIL import Image, ExifTags
import os

img_path = "C:\\Users\\Administrator\\Documents\\Noah-Lobbe-files\\Projects\\010 - Auto Collager for ma\\test images\\iphone images"
img_list = os.listdir(img_path)
print(img_list)

print("finding relavant tag key...")

for orientation in ExifTags.TAGS.keys():
  print("Key:", orientation)
  if ExifTags.TAGS[orientation]=='Orientation':
    print("found the tag key! It is:", orientation)
    break


print("exif data for each image...")

for i in img_list:
  img = Image.open(img_path + "\\" + i)
  exif_data = img._getexif()

  print(f"{i}:\n\t{exif_data[orientation]}\n")

  img.close()
