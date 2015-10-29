import random

def main():
	n = 20
	m = 5
	for _ in range(100):
		randlist = [random.random() for _ in range(m)]
		normalized_randlist = [int(n * randlist[i]/sum(randlist)) for i in range(m)]
		print normalized_randlist, sum(normalized_randlist)
	
if __name__=="__main__":
	main()