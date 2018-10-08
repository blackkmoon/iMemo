
def rounders(value):
	n = [int(i) for i in str(value)[::-1]]
	for k in range(len(n)-1):
		if n[k] >= 5:
			if n[k+1] == 9:
				pass
			n[k+1] +=1 
			n[k] = 0
		if n[k] <5:
			n[k] = 0
	print(n)
	int(n)

rounders(9)
