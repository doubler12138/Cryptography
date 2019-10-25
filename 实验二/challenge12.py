#!/usr/bin/env python2
from helpers import *
from base64 import b64decode
import sys

suffix = b64decode(
    ('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg'
     'aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq'
     'dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg'
     'YnkK'))
key = generateRandomData(32)


def encrypt(plain):
    a = textToByteList(suffix)
    plain.extend(a)
    return encryptECB(pkcs7Padding(plain), key)


def detectBlockSize():
    msglen = len(encrypt([]))
    p1 = p2 = ''
    l1 = l2 = len(encrypt([]))
    while l1 == l2:
        p1 += 'A'
        l2 = len(encrypt(textToByteList(p1 + p2)))
    l1 = l2
    while l1 == l2:
        p2 += 'A'
        l2 = len(encrypt(textToByteList(p1 + p2)))
    return (msglen - len(p1) + 1, len(p1) - 1, len(p2))


def generateCiphertexts(buffer):
    buffers = {}
    for b in xrange(256):
        buffers[b] = encrypt(buffer + [b])
    return buffers.items()


def guessBytes(maxCount, blocksize):
    buffer = [0x41] * (blocksize - 1)
    blockCount = 0  # counts the number of recovered blocks
    recoveredBytes = []
    for i in xrange(maxCount):
        if len(recoveredBytes) > 0 and len(recoveredBytes) % blocksize == 0:
            blockCount += 1
            buffer.extend([0x41] * blocksize)
        ciphertexts = generateCiphertexts(buffer[len(recoveredBytes):] +
                                          recoveredBytes)
        ciphertext = [c for c in chunks(
            encrypt(buffer[len(recoveredBytes):]), 
            blocksize)][blockCount] 

        for plain, cipher in ciphertexts:  
            if [c for c in chunks(cipher, blocksize)][blockCount] \
               == ciphertext:
                recoveredBytes.append(plain)
    return recoveredBytes


def main():
    msglen, _, blocksize = detectBlockSize()  
    print 'Block size: %d, message length: %d' % (blocksize, msglen)

    # check for ECB use
    ciphertext = encrypt([0x41] * 3 * blocksize)
    if not verifyECB(ciphertext, blocksize):
        print 'No ECB usage detected'
        sys.exit(-1)

    # now try to recover the plaintext
    plaintext = guessBytes(msglen, blocksize)
    print 'Length of recovered plaintext: %d\n%s' % (len(plaintext),
                                                     bytesToText(plaintext))


if __name__ == '__main__':
    main()
