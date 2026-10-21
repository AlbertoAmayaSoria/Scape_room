"""
ESCAPE ROOM DE PROGRAMACION - SOLUCIONES (SOLO ORGANIZADORES)

Ejecuta este archivo para comprobar toda la cadena de respuestas:
    python3 soluciones_organizadores.py

Cada K se obtiene de la respuesta del problema anterior. Las funciones se
comprueban contra fuerza bruta en casos pequenos (asserts) antes de usarse
con los valores grandes del evento.
"""
import math
from collections import Counter


# ---------------- P1: numeros de 1 a 1000 con suma de digitos = 10
def p1():
    return sum(1 for n in range(1, 1001) if sum(map(int, str(n))) == 10)


# ---------------- P2: tribonacci con modulo, n = K + 30
def t_rec(n):
    return n if n <= 2 else t_rec(n - 1) + t_rec(n - 2) + t_rec(n - 3)


def tmod(n, m=1000):
    if n <= 2:
        return n % m
    a, b, c = 0, 1, 2
    for _ in range(n - 2):
        a, b, c = b, c, (a + b + c) % m
    return c


assert all(tmod(i, 10**9) == t_rec(i) % 10**9 for i in range(22))


def p2(K):
    return tmod(K + 30)


# ---------------- P3: puertas, solo quedan abiertas las de numero cuadrado perfecto
def doors_brute(N):
    d = [False] * (N + 1)
    for i in range(1, N + 1):
        for j in range(i, N + 1, i):
            d[j] = not d[j]
    return sum(d)


assert all(doors_brute(n) == math.isqrt(n) for n in range(1, 300))


def p3(K):
    return math.isqrt(K * 10**9) % 10000


# ---------------- P4: Josefo, sobrevive 2*(N - 2^floor(log2 N)) + 1
def jos_sim(n):
    p = list(range(1, n + 1))
    i = 0
    while len(p) > 1:
        out = (i + 1) % len(p)
        p.pop(out)
        i = out if out < len(p) else 0
    return p[0]


def jos(n):
    return 2 * (n - (1 << (n.bit_length() - 1))) + 1


assert all(jos(n) == jos_sim(n) for n in range(1, 400))
assert [jos(n) for n in range(1, 9)] == [1, 1, 3, 1, 3, 5, 7, 1]


def p4(K):
    return jos(K * 10**12 + 1) % 1000


# ---------------- P5: cambio de monedas (combinaciones, no permutaciones)
COINS = [1, 5, 10, 25, 50, 100]


def ways(A):
    dp = [0] * (A + 1)
    dp[0] = 1
    for c in COINS:
        for a in range(c, A + 1):
            dp[a] += dp[a - c]
    return dp[A]


def ways_rec(A, k=0):
    if A == 0:
        return 1
    if A < 0 or k == len(COINS):
        return 0
    return ways_rec(A - COINS[k], k) + ways_rec(A, k + 1)


assert all(ways(a) == ways_rec(a) for a in range(0, 130))


def p5(K):
    return ways(K * 10) % 10000


# ---------------- P6: trampa de punto flotante
def p6(K):
    M = 10**15 + K
    N = M * M - 1
    wrong = int(math.sqrt(N))      # lo que imprime el codigo del enunciado
    right = math.isqrt(N)          # = M - 1
    assert right == M - 1 and wrong == M
    return right % 10000, wrong % 10000


# ---------------- P7: invertir x -> 7x + 3 (mod p) aplicado K veces
P = 1_000_000_007
N0 = 538129467                      # secreto del autor
INV7 = (P + 1) // 7                 # 142857144, se puede sacar a mano
assert 7 * INV7 % P == 1


def p7_target(K):
    n = N0
    for _ in range(K):
        n = (7 * n + 3) % P
    return n


def p7(K, T):
    n = T
    for _ in range(K):
        n = ((n - 3) * INV7) % P
    return n


# ---------------- P8: pares que suman T en un arreglo de 2 millones
def gen(seed, N, R):
    x = seed
    out = []
    for _ in range(N):
        x = (x * 1103515245 + 12345) % 2**31
        out.append(x % R)
    return out


def count_pairs(a, T):
    cnt = Counter()
    pairs = 0
    for v in a:
        pairs += cnt[T - v]
        cnt[v] += 1
    return pairs


def pairs_brute(a, T):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] + a[j] == T)


_a = gen(123, 600, 50)
assert count_pairs(_a, 50) == pairs_brute(_a, 50)
N8, R8, T8 = 2_000_000, 10_000_000, 10_000_000


def p8(seed):
    return count_pairs(gen(seed, N8, R8), T8)


# ---------------- P9: x -> x^2 + 1 (mod M), 10^15 veces: hay un ciclo
M9 = 999983


def p9(K, S=10**15):
    x = K % M9
    seen = {}
    seq = []
    i = 0
    while x not in seen:
        seen[x] = i
        seq.append(x)
        x = (x * x + 1) % M9
        i += 1
    mu = seen[x]
    lam = i - mu
    idx = S if S < mu else mu + (S - mu) % lam
    return seq[idx], mu, lam


def p9_direct(K, S):
    x = K % M9
    for _ in range(S):
        x = (x * x + 1) % M9
    return x


assert all(p9(1234, S)[0] == p9_direct(1234, S) for S in (0, 5, 3000, 100000, 123457))


# ---------------- P10: caminos en cuadricula 40x40 con obstaculos (DP)
SIZE, DENS = 40, 20


def grid(seed, R=SIZE, C=SIZE, dens=DENS):
    x = seed
    blocked = set()
    for i in range(R):
        for j in range(C):
            x = (x * 1103515245 + 12345) % 2**31
            if (i, j) not in ((0, 0), (R - 1, C - 1)) and (x >> 16) % 100 < dens:
                blocked.add((i, j))
    return blocked


def paths(blocked, R, C):
    dp = [[0] * C for _ in range(R)]
    dp[0][0] = 1
    for i in range(R):
        for j in range(C):
            if (i, j) in blocked or (i, j) == (0, 0):
                continue
            dp[i][j] = (dp[i - 1][j] if i else 0) + (dp[i][j - 1] if j else 0)
    return dp[R - 1][C - 1]


def paths_rec(blocked, R, C, i=0, j=0):
    if i >= R or j >= C or (i, j) in blocked:
        return 0
    if (i, j) == (R - 1, C - 1):
        return 1
    return paths_rec(blocked, R, C, i + 1, j) + paths_rec(blocked, R, C, i, j + 1)


for s in (7, 99, 1234):
    b = grid(s, 8, 8)
    assert paths(b, 8, 8) == paths_rec(b, 8, 8)


def p10(seed):
    return paths(grid(seed), SIZE, SIZE)


# ---------------- cadena completa
if __name__ == "__main__":
    K1 = p1()
    K2 = p2(K1)
    K3 = p3(K2)
    K4 = p4(K3)
    K5 = p5(K4)
    K6, codigo_trampa = p6(K5)
    T = p7_target(K6)
    K7 = p7(K6, T) % 10000
    K8 = p8(K7) % 10000
    x9, mu, lam = p9(K8)
    K9 = x9 % 1000
    n10 = p10(K9)
    K10 = n10 % 10000

    print("Problema | Respuesta (entra como K al siguiente)")
    print(f" 1  -> {K1}")
    print(f" 2  -> {K2}")
    print(f" 3  -> {K3}")
    print(f" 4  -> {K4}")
    print(f" 5  -> {K5}")
    print(f" 6  -> {K6}   (el codigo del enunciado imprime {codigo_trampa}: trampa)")
    print(f" 7  -> {K7}   (T impreso en la hoja: {T})")
    print(f" 8  -> {K8}")
    print(f" 9  -> {K9}   (preperiodo {mu}, ciclo {lam})")
    print(f"10  -> {K10:04d}   (total de caminos: {n10})")
