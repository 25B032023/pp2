#1
import shutil

shutil.move("file1.txt", "folder/file1.txt")

print("File moved")
#сонда:
#file1.txt ->>> folder/file1.txt


#2

import shutil

shutil.copy("file.txt", "copy.txt")

print("Copied")

#3
#папка барма тексеру
import os

if os.path.exists("folder"):
    print("Exists")
else:
    print("Not found")