#题目要求：给你一个列表，移除这个列表里面重复的元素并输出一个没有重复元素的列表
#解法1：将列表转化成集合，利用集合中没有重复元素的性质，去掉重复元素，再将集合转换回列表
'''
def move_duplicate(x):
	new = set(x)
	return list(new)
a = move_duplicate([1,2,2,3])
print(a)
'''
#错误解析
#我原来这么写的：
'''
def move_duplicate(x):
	new = set(x)
	return list(new)
move_duplicate([1,2,2,3])
print(move_duplicate)
'''
#得到这个结果：
#<function move_duplicate at 0x0000000001D33E18>
#如果不把return的结果赋值给一个变量的话，函数执行完之后是不会保存执行结果的

#解法2：不用集合做
'''
def move_duplicate(x):
	for i, a in enumerate(x):
		for j, b in enumerate(x):
			if a==b and i!=j:
				x.remove(a)
	return(x)
c = move_duplicate([1, 2, 1, 2, 3, 4, 5, 4, 1, 2, 3, 2, 1])
print(c)
'''
#这个程序是错的,我输入[1, 2, 2, 3]还好使，输入这个就不好使了，结果是：[3, 5, 3, 2, 1]


#第一个错误解析，我在if之前把这几个变量都打印出来，逐个分析
'''
def move_duplicate(x):
	for i, a in enumerate(x):
		for j, b in enumerate(x):
			print(a, i, b, j)
			if a==b and i!=j:
				x.remove(a)
				print(x)
	return(x)
c = move_duplicate([1, 2, 1, 2, 3, 4, 5, 4, 1, 2, 3, 2, 1])
'''
#此程序得到如下结果：
'''
1 0 1 0
1 0 2 1
1 0 1 2
[2, 1, 2, 3, 4, 5, 4, 1, 2, 3, 2, 1]
1 0 3 3
1 0 4 4
1 0 5 5
1 0 4 6
1 0 1 7
[2, 2, 3, 4, 5, 4, 1, 2, 3, 2, 1]
1 0 3 8
1 0 2 9
1 0 1 10
[2, 2, 3, 4, 5, 4, 2, 3, 2, 1]
2 1 2 0
[2, 3, 4, 5, 4, 2, 3, 2, 1]
2 1 3 1
2 1 4 2
2 1 5 3
2 1 4 4
2 1 2 5
[3, 4, 5, 4, 2, 3, 2, 1]
2 1 2 6
[3, 4, 5, 4, 3, 2, 1]
5 2 3 0
5 2 4 1
5 2 5 2
5 2 4 3
5 2 3 4
5 2 2 5
5 2 1 6
4 3 3 0
4 3 4 1
[3, 5, 4, 3, 2, 1]
4 3 4 2
[3, 5, 3, 2, 1]
4 3 2 3
4 3 1 4
1 4 3 0
1 4 5 1
1 4 3 2
1 4 2 3
1 4 1 4
[Finished in 0.1s]
'''
#因为列表变了， 但是enumerate的遍历顺序没变，还一直往下走，比如列表变了之后，j是新的列表下标为3的数，所以旧的列表下标为3的数漏了
#按照这个思路一直往下捋，所以最后才两个3

#第二个错误解析
#我最开始这么写的：
'''
def move_duplicate(x):
	for i, a in enumerate(x):
		for j, b in enumerate(x):
			if a==b and i!=j:
				new=x.remove(a)	
	return(new)
c = move_duplicate([1, 2, 2, 3])
print(c)
'''
#结果是none,原因是remove这个函数没有返回值，没把结果传给new,举个例子：
'''
x = [1, 2, 3]
a = x.remove(1)
print(a)
'''
#输出结果是none, 因为x.remove(1)没把结果传给a,但是如果我这么写：
'''
x = [1, 2, 3]
x.remove(1)
print(x)
'''
#结果就是[2, 3]

#正确写法
'''
def move_duplicate(x):
	y = []
	for i in x:
		if i not in y:
			y.append(i)
	return(y)
c = move_duplicate([1, 2, 1, 2, 3, 4, 5, 4, 1, 2, 3, 2, 1])
print(c)
'''

#解法3：用字典解决
'''
def move_duplicate(X):
	Y = []
	D = {}
	for x in X:
		if x not in D:
			Y.append(x)
			D[x] = 1
		else:
			D[x] += 1
	return(Y, D)
result = move_duplicate([1, 2, 2, 3])
print(result)
'''
#相当于把字典当成了列表用，根本不需要else,去掉函数，简化成如下算法：
'''
X = [1, 2, 2, 3]
Y = []
D = {}
for x in X:
	if x not in D:
		Y.append(x)
		D[x] = 1
	else:
		D[x] +=1
print(Y)
'''
#或者这样

X = [1, 2, 2, 3]
Y = []
D = {}
for x in X:
	if x not in D:
		Y.append(x)
		D[x] = 1
print(Y)

	
