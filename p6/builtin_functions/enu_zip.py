# 1
fruits = ["apple", "banana", "orange"]

for i, f in enumerate(fruits):
    print(i, f)


# 2
names = ["Ali", "Dana", "Aruzhan"]

for i, n in enumerate(names, start=1):
    print(i, n)


# 3
names = ["Ali", "Dana"]
scores = [90, 95]

res = list(zip(names, scores))
print(res)


# 4
names = ["A", "B", "C"]
scores = [10, 20, 30]

for n, s in zip(names, scores):
    print(n, s)


# 5
keys = ["name", "age", "city"]
values = ["Ali", 20, "Almaty"]

d = dict(zip(keys, values))
print(d)