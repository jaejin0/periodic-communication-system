import random

''' configuration '''
size = 17
min_val = 0.02
max_val = 0.06
precision = 10

res = []
    
while True:
    n = random.random()
    if n > min_val and n < max_val:
        res.append(round(n, precision))

    if len(res) == size:
        break

print(res)
