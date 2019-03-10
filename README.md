# crypto
Encrypt, decrypt, and decipher affine ciphers from the command line

## to encrypt txt file from command line using key (3, 7)
python affine.py encrypt file.txt encrypted.txt 3 7

## to decrypt file with key (3, 7)
python affine.py decrypt encrypted.txt decrypted.txt 3 7

## to brute force decipher an encrypted file and finds key that returns the most words that appear in a dictionary
python affine.py decipher encrypted.txt decrypted.txt dictionary.txt
