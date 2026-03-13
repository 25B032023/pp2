from functools import reduce

#1 
nums = [1, 2, 3, 4]
res = list(map(lambda x: x*x, nums))
print(res)   # [1, 4, 9, 16]


#2
words = ["python", "java", "c++"]
res = list(map(str.upper, words))
print(res)   # ['PYTHON', 'JAVA', 'C++']


#3
nums = [1,2,3,4,5,6]
res = list(filter(lambda x: x % 2 == 0, nums))
print(res)   # [2,4,6]


#4  
words = ["cat", "elephant", "dog", "tiger"]
res = list(filter(lambda x: len(x) > 4, words))
print(res)


# 5
nums = [1,2,3,4]
res = reduce(lambda a,b: a*b, nums)
print(res)   # 24