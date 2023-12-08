from operator import itemgetter
from cli import filepath

with open(filepath) as inp:
	lines = inp.read().splitlines()

hands = [l.split(' ')[0] for l in lines]
bids = [int(l.split(' ')[1]) for l in lines]

# A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2
labels = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

def transform(hand, bid):
	count = [0] * len(labels)
	for c in hand:
		count[labels.index(c)] += 1
	return (sorted(count, reverse=True), hand, bid)

def compare(c, n):
	if c[0] == n[0]:
		h1 = c[1]
		h2 = n[1]
		for idx, char in enumerate(h1):
			if char == h2[idx]:
				continue
			return labels.index(char) > labels.index(h2[idx])
	return c[0] > n[0]

def bubble_sort(arr, key=None):
	if not key:
		key = lambda x: x
	for i in range(len(arr)):
		for j in range(len(arr) - 1 -i):
			if key(arr[j], arr[j + 1]):
				tmp = arr[j]
				arr[j] = arr[j + 1]
				arr[j + 1] = tmp
	return arr

counts = [transform(h, bids[idx]) for idx, h in enumerate(hands)]
bubble_sort(counts, key=compare)
ans = 0
for idx, sc in enumerate(counts):
    ans += ((idx + 1)* sc[2])

print(ans)