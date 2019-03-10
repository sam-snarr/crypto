# affine cipher
import sys
import re

def encrypt(infile, a, b, outfile):
    '''function that encrypts file with key a, b'''
    #gets values of inverse, gcd, etc
    dat = egcd(max(a, 128), min(a, 128)) 
    print(dat)
    if dat[0] != 1:
        print('Your key combination ({},{}) is not valid'.format(a, b))
        return None
    
    #reads in file to encrypt
    file = open(infile, 'r')
    text = file.read()
    file.close()
    
    #string of the text that is encrypted
    etext = '' 
    for char in text:
        #encrypts each char using affine cypher
        newChar = chr((ord(char)*a + b) % 128)
        etext= etext + newChar
        
    #writes this encrypted text to file
    efile = open(outfile, 'w+')
    efile.write(etext)
    efile.close()

def egcd(a, b):
    '''function that returns gcd, s, t using extended euclidean algorithm'''
    s=1
    t=0
    u=0
    v=1
    while b != 0:
        q = a//b #must do floor division (int)
        a, b = b, a%b
        s, t, u, v = u, v, s-u*q, t-v*q
    d = a 
    return d, s, t

def decrypt(infile, a, b, outfile):
    ''' function that decrypts file given a, b'''
    dat = egcd(max(a, 128), min(a, 128))
    aInverse = dat[2]

    if dat[0] != 1:
        print('Your key combination ({},{}) is not valid'.format(a, b))
        return None
    
    #reads in text file that is encrypted
    file = open(infile, 'r')
    ctext = file.read()
    file.close()
    
    dtext = ''
    for char in ctext:
        
        #decrypts each char in encrypted file
        newChar = chr((aInverse*(ord(char)-b))%128)
        dtext = dtext + newChar
    
    #writes decrypted text to file
    dfile = open(outfile, 'w+')
    dfile.write(dtext)
    dfile.close()
    
    
def decipher(infile, outfile, dict):
    '''Function that takes in file, dictionary, and tries to find key pair that returns most words'''
    
    #reads in file of ciphertext
    file = open(infile, 'r')
    ctext = file.read()
    file.close()
    
    #reads in dictionary and creates a hash table for faster search
    dict = open(dict, 'r').read().lower().splitlines()
    dict = set(dict)
    
    maxA = 0
    maxB = 0
    maxCount = 0
    count = 0
    bestDecrypt = ''
    secondBest = ''
    
    for a in range(128):
        dat = egcd(max(a, 128), min(a, 128))
        aInverse = dat[2]
        if dat[0] == 1: #tests to make sure a, b pair are valid
            for b in range(128):
                
                dtext = ''
                for char in ctext:
                    #decrypts using a, b
                    newChar = chr((aInverse*(ord(char)-b))%128)
                    dtext = dtext + newChar
                
                count = 0
                #looks for words in decrypted text
                for word in re.split('\W+', dtext):
                    if len(word)>=4: #helps with false positives
                        if word.lower() in dict:
                            count += 1
                            
                #print(a, b, count)
                if count>maxCount: #tests to see if new best decipher
                    maxCount=count
                    maxA = a
                    maxB = b
                    secondBest = bestDecrypt
                    bestDecrypt = dtext
    
    #outputs file with deciphered text
    dfile = open(outfile, 'w')
    dfile.write('{}, {}\nDeciphered Message\n'.format(maxA,maxB))
    dfile.write( bestDecrypt)
    dfile.close()
    
    #print('With {} matched words(length greater than 3) using key pair ({}, {}) the best decryption is \n\n{} '.format(maxCount, maxA, maxB, bestDecrypt))

#command line functionality
#print(sys.argv)
if sys.argv[1] == 'encrypt':
    infile=sys.argv[2]
    a=int(sys.argv[4])
    b=int(sys.argv[5])
    outfile=sys.argv[3]
    encrypt(infile, a, b, outfile)
elif sys.argv[1] == 'decrypt':
    infile=sys.argv[2]
    a=int(sys.argv[4])
    b=int(sys.argv[5])
    outfile=sys.argv[3]
    decrypt(infile, a, b, outfile)
elif sys.argv[1] == 'decipher':
    infile=sys.argv[2]
    outfile=sys.argv[3]
    dict=sys.argv[4]
    decipher(infile, outfile, dict)
else:
    print('Invalid command line entry')
    