import base64
import json
import random
import itertools
import cryptography


def split_base64_randomly(encoded_str, max_length=10):
    chunks = []
    i = 0
    while i < len(encoded_str):
        random_length = random.randint(1, max_length)
        end = i + random_length
        chunks.append(encoded_str[i:end])
        i = end
    return chunks

def fisher_yates_shuffle(original, seed):
    '''
    List/Array mischen anhang Zahl (seed)
    '''
    arr = original.copy()
    random.seed(seed)
    
    for i in range(len(arr) - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    
    return arr

def inverse_fisher_yates_shuffle(shuffled, seed):
    '''gemischte list/array wiederherstellen anhang Zahl (seed)'''
    arr = shuffled.copy()
    random.seed(seed)
    swaps = []
    
    for i in range(len(arr) - 1, 0, -1):
        j = random.randint(0, i)
        swaps.append((i, j))
    
    for swap in reversed(swaps):
        arr[swap[0]], arr[swap[1]] = arr[swap[1]], arr[swap[0]]
    
    return arr


def encb64(data, mode):
    '''Encode String zu base64 und mischen 
    oder gemischter string wiederherstellen
    data = string, mode = encode or decode'''
    if mode == 'encode':
        dd = base64.b64encode(data.encode())
        hh = dd.split(b'==')[0]
        l = len(hh)
        arr = split_base64_randomly(hh,l)

        shuffled = fisher_yates_shuffle(arr,l+len(arr)-1)
        cc = b'.'.join(shuffled)
        return cc
    elif mode == 'decode':
        if isinstance(data, str):
            data = data.encode()
        l2 = len(data)
        bb2= data.split(b'.')
        inversed = inverse_fisher_yates_shuffle(bb2, l2)
        cc2 = b''.join(inversed)
        final = base64.b64decode(cc2+b'==')
        return final
    else:
        return 'error'
    

def xor_cypher(input_string, key):
    encrypted = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(input_string, itertools.cycle(key)))
    return encrypted

def encrypt(input_string, key):
    encrypted = xor_cypher(input_string, key)
    return base64.b64encode(encrypted.encode()).decode()

def decrypt(encrypted_string, key):
    encrypted = base64.b64decode(encrypted_string.encode()).decode()
    return xor_cypher(encrypted, key)


# secret="gB9VefH78g9ZFgVGk9dC6qfyze"
# print(encrypt("cf2dfe1ad6acdb3a6bad1ce70f504c8d0f611bbc", secret))