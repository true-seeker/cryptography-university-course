x = 87
m = 101
c = 5
a = 7
COUNT = 10000
frequency = {}

for i in range(COUNT):
    x = (a * x + c) % m
    if frequency.get(x) is None:
        frequency[x] = 1
    else:
        frequency[x] += 1

for key in frequency:
    print(key, frequency[key])
