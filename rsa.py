'''
rsa.py
Suraj Rampure, surajr@me.com

Generates an RSA public key and private key based off of
random numbers pulled from fetchnumbers.py

This works by first generating two large numbers, which may or may not
be prime to begin with. Then, this breaks the two numbers into their prime factors, and selects a random one of each of their prime factors to be p and q. Eventually, this computes the public key (N, e) and the private key d such that

    N = pq
    e is prime and relatively prime to (p-1)(q-1)
    d is the multiplicative inverse of e in mod (p-1)(q-1)

Referenced a note from the  Probability Theory and Discrete Mathematics class I took last semester, CS 70 at UC Berkeley. http://www.eecs70.org/static/notes/n6.pdf

Created for the unifyID technical challenge.
'''

from fetchnumbers import *
from math import floor

# Helper functions ----
def isPrime(x):
    '''While this could be optimized by using the Sieve of Eratosthenes,
    for our purposes this works just fine.
    '''
    for i in range (2, int(x**0.5) + 1):
        if x % i == 0:
            return False
    return True

def primeFactors(x):
    if isPrime(x):
        return [x]
    else:
        output = []
        for i in range (2, x):
            if isPrime(i) and x % i == 0:
                output.append(i)
        return output

def egcd(x, y):
    if y == 0:
        return (x, 1, 0)
    else:
        (d, a, b) = egcd(y, x % y)
        return (d, b, a - floor(x/y)*b)

# RSA key generating functions ----
def findPQ(lower_bound=100, upper_bound=10000):
    ''' Determines p and q in the RSA scheme. '''

    [x, y] = rand_in_range(lower_bound, upper_bound, 2)

    x_factors = primeFactors(x)
    lenX = len(primeFactors(x))

    y_factors = primeFactors(y)
    lenY = len(primeFactors(y))

    if lenX == 1:
        p = x
    else:
        index = rand_in_range(0, lenX-1)
        p = x_factors[index[0]]

    if lenY == 1:
        q = y
    else:
        index = rand_in_range(0, lenY-1)
        q = y_factors[index[0]]

    return (p, q)

def getPublicKey(p, q):
    ''' Given p and q, this determines N and e in the RSA scheme. '''

    N = p*q
    e = 3
    flag = True
    while flag:
        if isPrime(e) and (p-1)*(q-1) % e != 0:
            flag = False
        else:
            e += 1
    return (N, e)

def getPrivateKey(px, qx, e):
    ''' Given p-1, q-1 and e, this determines d in the RSA scheme. '''

    nx = px*qx
    (a, b, d) = egcd(nx, e)
    return d % nx

def encrypt(x, e, N):
    return x**e % N

def decrypt(y, d, N):
    return y**d % N

# Implementation ----
(p, q) = findPQ()
(N, e) = getPublicKey(p, q)
d = getPrivateKey(p-1, q-1, e)
print("Public key (N, e): ({0}, {1})".format(N, e))
print("Private key d: {0}".format(d))

# Note that decrypt(encrypt(x, e, N), d, N) == x
