#1
import os

#2
# папка жасау
os.mkdir("my_folder")

#3
# барлық папкаларды көрсету
dirs = os.listdir()

print("Directories:")
for d in dirs:
    print(d)

#4
# папка өшіру
import os

os.rmdir("my_folder")

print("Directory removed")