def maxscore(array):
	if len(array) == 1:
		return array[0] 
	count = 0
	while len(array) > 2:
		b = array[1:-1]
		c = min(b)
		d = array.index(c)
		count += array[d-1]*array[d]*array[d+1]
		b.remove(c)
		array = [array[0]] + b + [array[-1]]
	if array[0] >= array[1]:
		count += array[0]*array[1]
		array.remove(array[1])
	else:
		count += array[0]*array[1]
		array.remove(array[0])
	count += array[0]
	return count
result = maxscore([3, 1, 5, 8])
print(result)