n, q = list(map(int, input().split()))
A = list(map(int, input().split()))

for _ in range(q):
    l, r, v = list(map(int, input().split()))

    for i in range(l - 1, r):
        A[i] = A[i] & v

print(" ".join([str(i) for i in A]))