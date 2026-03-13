#1
with open("demofile.txt", "a") as f:
    f.write("Now the file has more content!")

#open and read the file after the appending:
with open("demofile.txt") as f:
    print(f.read())

#2
with open("demofile.txt", "w") as f:
    f.write("Woops! I have deleted the content!")

#open and read the file after the overwriting:
with open("demofile.txt") as f:
    print(f.read())

#3
with open("file1.txt", "w") as f:
    f.write("Hello Python")

with open("file1.txt") as f:
    print(f.read())

#4
with open("file2.txt", "w") as f:
    f.write("Line 1\n")
    f.write("Line 2\n")
    f.write("Line 3")

with open("file2.txt") as f:
    print(f.read())