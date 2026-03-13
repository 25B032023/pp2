#1
f = open("demofile.txt")

#2
f = open("demofile.txt")
print(f.read())

#3
f = open("D:\\myfiles\welcome.txt")
print(f.read())

#4
with open("demofile.txt") as f:
    print(f.read())

#5
f = open("demofile.txt")
print(f.readline())
f.close()

#6
with open("demofile.txt") as f:
    print(f.read(5))

#7
with open("demofile.txt") as f:
    print(f.readline())

#8
with open("demofile.txt") as f:
    for x in f:
        print(x)

#9

