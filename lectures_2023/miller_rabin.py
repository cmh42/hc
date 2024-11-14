# -*- coding: utf-8 -*-
"""
The miller_rabin module containing the functions: 
miller_rabin, is_prime, gcd
Last edited 22/04/21
"""

from random import randint 

def miller_rabin(p,base): 
    '''
    Partially tests whether p is prime using the given base.
    Uses the ROO and FLT tests combined with Pingalas algorithm. 
    If False is output then  p is definitely not prime. 
    It True is output then p MIGHT be prime. 
    This test is far from perfect.
    '''
    n = 1
    exponent = p-1
    modulus = p
    bin_string = bin(exponent)[2:]        # Get 'exponent' in binary without the first '0b'
    
    for bit in bin_string:               # Iterate through the '0' and '1' of binstring
        n_squared = n * n % modulus      # We need this below
        
        if  n_squared == 1:              # Case when n * n = 1 mod p. 
            if (n != 1) and (n != p-1):  # Case when is neither 1 nor -1 mod p
                return False             # So ROO violated and False is output
        
        if bit == '1': 
            n = (n_squared * base) % modulus
        if bit == '0':
            n = n_squared 
    
    if n != 1:                          # I.e. base**(p-1) not = 1 mod p
        return False                    # FLT violated in this case and False is output

    return True                         # No FLT or ROO violation. p might be prime. 




def is_prime(p,num_wit=50): 
    ''' 
    Tests whether a positive integer p is prime.
    For p <= 37 p is prime iff p is in [2,3,5,7,11,13,17,19,23,29,31,37].
    For p > 37, if p is even then it is not prime, otherwise... 
    For p <= 2^64 the Miller-Rabin test is applied using the witnesses 
    in [2,3,5,7,11,13,17,19,23,29,31,37].
    For p > 2^64 the Miller-Rabin test is applied using 
    num_wit many randomly chosen witnesses. 
    '''
 
    # We need a direct test on numbers {0,1,...,37} 
    first_primes = [2,3,5,7,11,13,17,19,23,29,31,37]
    if p < 38:
        return p in first_primes
    
    # If p is even and greater than 37 then p is not prime.  
    if p % 2 == 0: 
        return False

    # For 37 < p <= 2**64 we apply the miller_rabin test 
    # using as witnesess the prime numbers in first_primes
    if p <= 2**64: 
        verdict = True 
        for witness in first_primes: 
            if miller_rabin(p,witness) == False:
                return False
        return True      
    
    # For p > 2**64 we apply the miller_rabin test using
    # a sample of wit_num many randomly chosen witnesses
    else: 
        num_trials = 0
        while num_trials < num_wit: 
            num_trials = num_trials + 1
            witness = randint(2,p-2)
            if miller_rabin(p,witness) == False: 
                return False
        return True 
    
    
def gcd(a,b):
    """
    Returns the greatest common divisor of integers a and b using Euclid's algorithm.
    The order of a and b does not matter and nor do the signs.
    """
    if not (a % 1 == 0 and b % 1 == 0):
        print( "Need to use integers for gcd.")
        return None
    if b == 0:
        # The gcd is the absolute value of the present value of a.
        return abs(a)                  
    else:
        return gcd(b,a % b)


