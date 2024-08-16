import requests
from openai import OpenAI
import os
import webbrowser
import random
import re
from colorama import Fore, Back, Style, init

init(autoreset=True)

client = OpenAI(
    api_key=''
)

user_prompt = input("> ")

response = client.images.generate(
  model="",
  prompt=user_prompt,
  size="",
  quality="",
  n=1,
)

image_url = response.data[0].url
image_data = requests.get(image_url).content

def downloader(base_path, filename):
    try:
        path1 = os.path.join(base_path, "generations")
        if not os.path.exists(path1):
            os.makedirs(path1)

        path2 = os.path.join(path1, "HaxiboMini")
        if not os.path.exists(path2):
            os.makedirs(path2)

        imagepath = os.path.join(path2, filename)

        with open(imagepath, 'wb') as file:
            file.write(image_data)
        print(f"The image has been generated!")
        print(f"You can find the generated images in {path2}")
        webbrowser.open(imagepath)
        return True

    except PermissionError as e:
        print(f"Unable to get image data on disk: {e}")
        return False

def g_filename(prompt):
    words = prompt.split()
    if len(words[0]) <= 3 and len(words) > 1:
        key_word = words[1]
    else:
        key_word = words[0]
    
    key_word = re.sub(r'\W+', '', key_word)
    
    randon = str(random.randint(10000, 99999))
    stringd = f"HaxiboMINI_{key_word}_{randon}.png"
    return stringd

fname = g_filename(user_prompt)

paths = [
    os.path.join(os.path.expanduser("~"), "Desktop"),
    os.path.join(os.path.expanduser("~"), "Downloads"),
    os.path.join(os.path.expanduser("~"), "Documents")
]

saved = False
for path in paths:
    if downloader(path, fname):
        saved = True
        break

if not saved:
    print("Unable to save image on the disk. You can get the image from this URL:")
    print(image_url)
