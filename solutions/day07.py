from cli import filepath

with open(filepath) as inp:
	lines = inp.read().splitlines()

hands = [l.split(' ')[0] for l in lines]
bids = [int(l.split(' ')[1]) for l in lines]

def transform(hand, bid, labels, upgrade=False):
	count = [0] * len(labels)
	for c in hand:
		count[labels.index(c)] += 1
	print(count)
	if upgrade and 'J' in hand:
		j_count = count[0]
		max_count = count[1:].index(max(count[1:])) + 1
		count[max_count] += j_count
		count[0] = 0
		if hand == 'JJJJJ':
			sorted_count = [0] * len(labels)
	sorted_count = sorted(count, reverse=True)
	return (sorted_count, hand, bid)

print(transform(hands[0], bids[0], ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']))

def compare(c, n, labels):
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

labels = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
counts = [transform(h, bids[idx], labels) for idx, h in enumerate(hands)]
bubble_sort(counts, key=lambda x,y: compare(x, y, labels))
ans = 0
for idx, sc in enumerate(counts, 1):
    ans += ((idx)* sc[2])

print(ans)

labels = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
counts = [transform(h, bids[idx], labels, True) for idx, h in enumerate(hands)]
bubble_sort(counts, key=lambda x,y: compare(x, y, labels))

ans = 0
for idx, sc in enumerate(counts, 1):
    ans += ((idx)* sc[2])

print(ans)