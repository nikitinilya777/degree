from random import randint, random
from gmpy2 import mpz

e, d, n = 0, 0, 0


def MesToCode(mes):
    M = ""
    for i in range(len(mes)):
        symbol = str(ord(mes[i]))
        symbol = '0' * (4 - len(symbol)) + symbol
        M = M + symbol
    return M


def CodeToMes(num):
    a = str(num)
    mes = ""
    while len(a) % 4 != 0:
        a = '0' + a
    for i in range(0, len(a), 4):
        mes += chr(int(a[i] + a[i + 1] + a[i + 2] + a[i + 3]))
    return (mes)


def CodeToBlocks(code, module):
    blocks = []
    length_module = len(str(module))
    length_block = length_module - length_module % 4
    while len(code) > 0:
        blocks.append(code[: length_block])
        code = code[length_block:]
    return blocks


def convert_to_bin(dec):
    bin = ""
    while dec > 0:
        bin = str(dec % 2) + bin
        dec //= 2
    return bin


def pow_mod(a, x, p):
    y = 1
    x = convert_to_bin(x)
    for bit in reversed(x):
        if bit == '1':
            y = y * a % p
        a = a * a % p
    return y


def НОД(a: int, b: int) -> int:
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return a + b


def extended_euclid(a, b):
    U = [a, 1, 0]
    V = [b, 0, 1]
    while V[0] != 0:
        q = U[0] // V[0]
        T = [U[0] % V[0], U[1] - q * V[1], U[2] - q * V[2]]
        U = V
        V = T
    return U


def GetPrime(t):
    q = 9973  # простое число для генерации
    t = mpz(t)
    ξ = random()  # число от 0 до 1
    N = mpz((10 ** (t - 1) // q) + (10 ** (t - 1) * ξ // q))
    if N % 2 == 1:
        N += 1
    u = 0
    while True:
        p = mpz((N + u) * q + 1)
        if pow(2, p - 1, p) == 1 and pow(2, N + u, p):
            res = p
            break
        u += 2
    return res


def gen_key():
    global e
    global d
    global n
    p = GetPrime(250)  # простое число 250 знаков
    q = GetPrime(250)  # простое число 250 знаков
    n = p * q
    φ = (p - 1) * (q - 1)
    while True:
        e = randint(2, φ - 1)
        if НОД(e, φ) == 1:
            break
    _, d, _ = extended_euclid(e, φ)
    d %= φ



def encrypted(mes, e1, n1):
    code = MesToCode(mes)
    blocks = CodeToBlocks(code, n1)

    encrypted_codes = []
    for block in blocks:
        encrypted_code_block = pow_mod(int(block), e1, n1)
        encrypted_codes.append(encrypted_code_block)

    return encrypted_codes


def decrypted(encrypted_codes):
    global d
    global n
    decrypted_mes = ""

    blocks = encrypted_codes
    for block in blocks:
        decrypted_code_block = pow_mod(int(block), d, n)
        decrypted_block = CodeToMes(decrypted_code_block)
        decrypted_mes += decrypted_block

    '''
    decrypted_M = pow_mod(encrypted_M, d, n) 
    decrypted_mes = Int_to_mes(decrypted_M)
    '''

    return decrypted_mes

