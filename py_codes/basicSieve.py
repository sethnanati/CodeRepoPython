sieve = [True] * 101
print(sieve)
for i in range(2, 100):
    if sieve[i]:
        print(i)
        print(range(i*i, 100, i))
        for j in range(i*i, 100, i):
            sieve[j] = False

            