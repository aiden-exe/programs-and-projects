import random
import math

#To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]


# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False


#pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)


#pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)


# return appropriate N that satisfies the error bounds
def findN(eps,m):
	if m/eps < 3:
		# For small m/eps, our expression is less than required, so putting it to a
		# appropriately big number manually
		N = 100
	else:
		N = int(100*(m/eps)*math.log(m/eps))	# Space - O(log(m/eps))
	return N

	'''To find N, we know that given q, the probability of error is <= eps
	probability of q being a particular prime (for eg, prob(q=5)) = 1/PI(N)
	
	Given two substrings with f value a and b (not same), error occurs if
	q is a prime factor of |a-b|. i.e., probability = p(d)/PI(N) where p(d) is number of 
	prime factors of d. 
	putting p(d) <= log d <= log(26^m), we get

	prob(error) <= c. m . log N/N, where c is a constant around 9-10. Putting this <= eps,
	we get N/log N >= c. (m/eps). Taken N satisfies this relation.
	'''


def place(char):
	'''Returns the place of character char in alphabet
	A is 0, B is 1 etc'''
	return ord(char) - 65

def powerModq(a, b, q):
	# Calculates a ^ b mod q, making sure working space complexity is minimized
	# a,b, q are positive integers
	# Time - O(log b), Space - O(log q)

	if b == 0:
		return 1 % q

	if b % 2 == 0:
		return (powerModq(a, b//2, q) * powerModq(a, b//2, q)) % q

	else:
		return (powerModq(a, b//2, q) * powerModq(a, b//2, q)*a) % q

# Return sorted list of starting indices where p matches x
def modPatternMatch(q,p,x):
	m = len(p)
	n = len(x)

	matches = [] # list containing index in x where pattern p appears

	HashedPattern = 0	# f(p)
	HashedSubStr = 0	# f(x[i, i+1....i+m])

	# Uses log q space to avoid computing 26**m (taking O(log m) time) multiple times
	MostSignificantPlace = powerModq(26, m-1, q)

	i = 0
	while i < m:
		HashedPattern = (HashedPattern * 26 + place(p[i])) % q
		HashedSubStr = (HashedSubStr * 26 + place(x[i])) % q

		i += 1

	print(HashedPattern)
	print(HashedSubStr)

	# there are m iterations, each a combination of basic arithmetic, Takes O(m log q) time 

	i = 0

	if HashedPattern == HashedSubStr:
		matches.append(i)
	while i+m < n:
		# We already know hash of [i, i+1, i+2... i+m-1], so to calculate hash of [i+1, i+2....i+m]
		# We simply remove i from beginning and add i+m at end, with appropriate arithmetic
		HashedSubStr = ((HashedSubStr - place(x[i])*MostSignificantPlace)*26 + place(x[i+m])) % q
		i += 1

		if HashedPattern == HashedSubStr:
			matches.append(i)
		# Each iteration is combination of basic arithmetic, so takes O(log q) time
		
	return matches

	# Total time O(m log q) + O(n log q) = O((m+n)log q) = O(n log q) since m <= n
	# Space used: m, n, i - O(log n); HashedPattern, HashedSubStr, MostSignificantPlace - O(log q); matches - O(k)
	#Therefore total space complexity is O(log n + log q)
	

# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q,p,x):
	m = len(p)	# O(log m) = O(log n)
	n = len(x)	# O(log n)
	
	WildCardIndex = 0	# O(log m) = O(log n)
	WildCardPlace = 0	# Place value of the index of Wildcard, O(log q)

	HashedPattern = 0	# O(log q)
	HashedSubStr = 0	# O(log q)

	MostSignificantPlace = powerModq(26, m-1, q)	# O(log q)

	i = 0				# O(log n)
	matches = []		#O(k)
	#Thus space complexity is O(log n + log q + k)

	# Hash function used will be similar to modPatternMatch, except the place of wildcard is hashed to 0
	# So if for eg wildcard is at place 3, in f(p) or f(substr), the value at place 26**3 will be 0 
	while i < m:
		if p[i] == "?":
			WildCardIndex = i
			WildCardPlace = powerModq(26, m-i-2, q)
			HashedPattern = HashedPattern * 26
			HashedSubStr = HashedSubStr * 26

		else:
			HashedPattern = (HashedPattern * 26 + place(p[i])) % q
			HashedSubStr = (HashedSubStr * 26 + place(x[i])) % q
		
		i += 1
	# Above loop takes O(log m. log q) (for exponent) + m * O(log q) = O(m log q)
	i = 0


	if HashedPattern == HashedSubStr:
		matches.append(i)

	while i+m < n:
		if WildCardIndex == m-1:
			HashedSubStr = (HashedSubStr - place(x[i])*MostSignificantPlace+place(x[i+m-1]))*26 % q

		else:
			HashedSubStr = ((HashedSubStr - place(x[i])*MostSignificantPlace %q	# Removing ith char
							 - place(x[i+WildCardIndex+1])*WildCardPlace % q	# Removing the wildcard index of next window
							 + place(x[i+WildCardIndex])*WildCardPlace*26) * 26 + place(x[i+m])) %q	# Adding previous wildcard and i+m
		
		i += 1

		if HashedPattern == HashedSubStr:
			matches.append(i)
		# Each iteration is basic arithmetic operation, thus O(log q) time
	
	return matches
	# Total time complexity - O((m+n)log q)
# print(modPatternMatch(100007, "AA", "AAGRDAADEAEFAAF"))

if __name__ ==  "__main__":
	print(modPatternMatchWildcard(100007, "?DEW", "FDEWKHFKDEW"))