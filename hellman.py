import chilkat2
import random
import string
import secrets
import time
import pickle
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

crypt = chilkat2.Crypt2()

crypt.HashAlgorithm = "ripemd320"
crypt.EncodingMode = "hex"
n = 32
def hash_message(data: bytes, n):
    hashed = crypt.HashStringENC(data)
    return hashed[-int(n / 4):]

def to_bytes(str_hex):
    return bytes.fromhex(str_hex)

def generate_hex(bits):
    return format(secrets.randbits(bits), f'0{bits//4}x')

def R(x, n, r):
    s = r + x
    return str(s)

def convert_hex_to_bin(hex_str, n):
    bin_str = bin(int(hex_str, 16))[2:]
    k = int(len(hex_str) * n / 4)
    return "0" * (k - len(bin_str)) + bin_str

def build_table_entry(i, L, n, r):
    xi0 = generate_hex(n)
    xij = xi0
    for j in range(L):
        xij = hash_message(to_bytes(R(xij, n, r)), n)
    return xi0, xij

def build_table_precalculation_entry(i, L, n):
    return build_table_entry(i, L, n, generate_hex(128 - n))

def build_table_precalculation(K, L, n):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(build_table_precalculation_entry, range(K), [L] * K, [n] * K))

    return np.array(results, dtype=object)

def build_attack(table, index_dict, ha, L, K, n, r):
    y = ha
    for j in range(L):
        if y in index_dict:
            i = index_dict[y]
            x = table[i][0]
            for m in range(L - j - 1):
                x1 = x
                x = hash_message(to_bytes(R(x, n, r)), n)
                k = hash_message(to_bytes(R(x1, n, r)), n)
                if hash_message(to_bytes(R(x, n, r)), n) == ha:
                    return R(x, n, r)
            return "PROBLEMS"
        y = hash_message(to_bytes(R(y, n, r)), n)
    return "PROBLEMS"

def build_and_save(K, L, n):
    start_time = timeit.default_timer()
    table = build_table_precalculation(K, L, n)
    end_time = timeit.default_timer()
    execution_time = end_time - start_time
    return table

def results(table, K, L, n, r):
    index_dict = {table[i][1]: i for i in range(K)}
    s = 0
    for _ in range(10_000):
        random_hash = hash_message(to_bytes(generate_hex(256)), n)
        x = build_attack(table, index_dict, random_hash, L, K, n, r)
        if x != "PROBLEMS" and random_hash == hash_message(to_bytes(x), n):
            s += 1
            print("peremoh")

    print(f"кількість успіхів: {s}, Pr:{s / 10000}")
    print(f"кількість невдач: {10000 - s}")
