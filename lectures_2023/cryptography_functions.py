"""
Module name: cryptography_functions
Module contains: number theory and cryptograph functions
Function names: gcd, gcd_ext, modular_inverse, decompose,
                totient_pp, make_mult_func, totient,
                miller_rabin, is_prime, random_prime
                rsa_private_key, rsa_public_key,
                rsa_encrypt, rsa_decrypt
"""

from random import SystemRandom, randint

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

def gcd_ext(a,b):
    """
    Outputs (gcd,x,y) such that gcd=ax+by.
    """
    if not(a%1 == 0 and b%1 == 0):                      # Reject if trying to use for non-integers
        print( "Need to use integers for gcd.")
        return None
    if a == 0:                                          # Base case is when a=0.
        return (abs(b), 0, abs(b)//b)                   # Then gcd =|b| and is 0*a+1*b or 0*a-1*b. Use abs(b)//b
    else:
        quot = b//a                                     # The rule is that g=gcd(a,b)=gcd(b%a,a).
                                                        # Let b=qa+r where r=b%a
        g, x, y = gcd_ext(b%a, a)                       # And if  g=x1*r + y1*a then since r=b-qa
        return (g, y - quot * x, x)                     # We get g = a*(y1-q*x1)+x1*b.
                                                        # So x=y1-q*x1 and y=x1.
    
def modular_inverse(a,b): 
    '''
    Given input (a,b) with a and b integers returns 
    the multiplicative inverse of a modulo b provided 
    gcd(a,b) = 1. Otherwise returns an error message.
    '''
    ic_message = 'The numbers are not comprime'
    (g,x,y) = gcd_ext(a,b)
    if not g == 1: 
        print(ic_message)
        return None
    x = x % b 
    return x 

def decompose(n):
    """
    Generates a dictionary representing the prime decomposition.
    """
    factors = {}
    current_number = n                          # Divide current_number by the factor found found until it reaches 1
    while current_number > 1:
        p=smallest_factor(current_number)
        if p in factors.keys():                 # If p is not a new factor, increase the power
            factors[p] += 1
        else:
            factors[p] = 1                      # If p is a new factor, create a new entry
        current_number = current_number // p
    return factors

def totient_pp(p,e): 
    ''' 
    Given input (p,e) with p being a prime and e  
    a positive integer, returns the totient of p^e 
    '''
    return p**(e-1) * (p - 1) 

def make_mult_func(func_pp): 
    '''
    When a function func_pp(p,e) of two arguments is given as input, 
    make_mult_func outputs a multiplicative function func 
    obtained from func_pp via prime decomposition.
    '''
    def func(n): 
        D = decompose(n)
        result = 1
        for p in D.keys():
            result = result * func_pp(p,D[p])
        return result 
    return func 

# The (full) totient function
#totient = make_mult_func(totient_pp)

def totient(n): 
    ''' 
    Given input n returns the totient of n.
    '''
    # This is the fundamental definition
    totient_fun = make_mult_func(totient_pp)
    return totient_fun(n)

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
    
def random_prime(bit_length):
    '''
    Returns a cryptographically secure random numbber 
    of bit_length many (binary) bits 
    '''
    while True:
        p = SystemRandom().getrandbits(bit_length)  
        if p >= 2**(bit_length-1):
            if is_prime(p):
                return p   

def rsa_private_key(bit_length):
    '''
    Given input bit_length returns a private RSA key (p,q) where 
    both p and q are primes with bit_length number of (binary) bits. 
    '''
    p = random_prime(bit_length)
    q = random_prime(bit_length)
    return (p,q)    # This is a 'tuple'. 

def rsa_public_key(p,q, e = 65537):
    '''
    Given input (p,q,e) returns the RSA public key 
    from the two prime numbers p and q and auxiliary 
    exponent e. If only (p,q) input, e = 65537 is used.
    '''
    N = p*q
    return (N,e)

def rsa_encrypt(m, N, e):  
    '''
    Given input (m,N,E) where m is the numerical 
    encoding of a message, returns the RSA 
    encryption of m using public key (N,e).
    '''
    return pow(m, e, N) 

def rsa_decrypt(c,p,q,N,e): 
    '''
    Given input (c,p,q,N,e) returns the RSA decryption of ciphertext
    c using private key (p,q) and public key (N,e). (We input N as a 
    parameter to avoid having to recompute N = p*q.)
    '''
    totient = N - (p + q) + 1       # This is (p-1)*(q-1)
    f = modular_inverse(e,totient)  # Note: f * e = 1 (mod totient)
    return pow(c,f,N)               # This is c**f (mod N)