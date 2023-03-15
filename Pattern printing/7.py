def pattern(n):
	for i in range(n):
		for j in range(n):
			if i + j == 2 or i - j == 2 or i + j == 6 or j - i == 2 :
				print("*", end = "")
			else:
				print(end = " ")
		print()
	

pattern(5)


#  *  
# * * 
#*   *
# * * 
#  * 