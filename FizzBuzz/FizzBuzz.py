"""This is a command line utility that takes in a positive integer `n`,
two positive divisors `a` and `b`, a `fizzword` associated with `a`, and
a `buzzword` associated with `b`. It then runs through all positive integers
between 1 and 100 (inclusive) and prints each integer *unless* it is a multiple
of `a`. In that case, it prints the fizzword instead. If the integer is a
multiple of b, then it prints the buzzword. And if the integer is a multiple
of both a and b, then it prints the concatenation of the fizzword and the
buzzword.

Example Usage:

```
python FizzBuzz.py 100 6 8 "grackle" "crackle"
```
"""

import argparse

def gcd(a, b):
	"""Computes the greatest common divisor of two positive integers.

	This is a straightforward implementation of the Euclidean Algorithm.
	:param a: The first positive integer
	:type param: ``int``
	:param b: The second positive integer
	:type b: ``int``
	:returns: greatest common divisor of `a` and `b`.
	:rtype: ``int``
	"""
	dividend = max(a, b)
	divisor = min(a, b)
	remainder = dividend % divisor
	while remainder > 0:
		dividend = divisor
		divisor = remainder
		remainder = dividend % divisor
	return divisor

def lcm(a, b):
	"""Returns the least common multiple of two integers.

	The least common multiple of any collection of integers is their product
	divided by their greatest common divisor.

	:param a: The first positive integer
	:type param: ``int``
	:param b: The second positive integer
	:type b: ``int``
	:returns: least common multiple of `a` and `b`.
	:rtype: ``int``
	"""
	return (a * b) / gcd(a, b)

def fizzbuzz(n, a, b, fizzword, buzzword):
	"""Prints the range from 1 to `n` with text replacements as described above.

	:returns: None
	"""
	least_common = lcm(a, b)
	for k in range(1, n + 1):
		if k % least_common == 0:
			print fizzword + buzzword
		elif k % a == 0:
			print fizzword
		elif k % b == 0:
			print buzzword
		else:
			print k

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("n", type=int,
		help="highest integer to include in the range")
	parser.add_argument("a", type=int, help="first positive integer")
	parser.add_argument("b", type=int, help="second positive integer")
	parser.add_argument("fizzword", type=str,
		help="word to print when we reach a multiple of a only")
	parser.add_argument("buzzword", type=str,
		help="word to print when we reach a multiple of b only")
	args = parser.parse_args()

	fizzbuzz(args.n, args.a, args.b, args.fizzword, args.buzzword)


# TODO:
# - Add unit tests.
# - Investigate inputing more than two divisors.
# - Investigate handling any list of integers (positive, negative, zero,
#	unsorted, repeats allowed), not just the ordered range from 1 to a
#   positive integer n.
# - Add error handling.



