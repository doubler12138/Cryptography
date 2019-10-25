#!/usr/bin/env python2
from helpers import *
import challenge12 as c12
import random


prefix = generateRandomData(random.randint(2, 32))
print 'Length of random prefix: %d' % len(prefix)
suffix = c12.suffix
key = generateRandomData()


def encrypt(plain):
    s = textToByteList(suffix)
    p = plain + s
    return encryptECB(pkcs7Padding(prefix + p), key)


def detectBlockSize():

    msglen = len(encrypt([]))
    p1 = p2 = ''
    l1 = l2 = msglen
    while l1 == l2:
        p1 += 'A'
        l2 = len(encrypt(textToByteList(p1)))
    l1 = l2
    # now that the preceding block is full
    while l1 == l2:
        p2 += 'A'
        l2 = len(encrypt(textToByteList(p1 + p2)))
    
    paddingsize = len(p1) - 1
    blocksize = len(p2)
    foundDouble = False
    buf = [0x41] * blocksize * 2
    while (not foundDouble) and len(buf) < 4 * blocksize:
        ciphertext = encrypt(buf)
        ctblocks = [c for c in chunks(ciphertext, blocksize)]
        for i in xrange(len(ctblocks) - 1):
            if ctblocks[i] == ctblocks[i + 1]:
                foundDouble = True
                break
        if not foundDouble:
            buf.append(0x41)
    padcount = len(buf) - 2 * blocksize  
    return (msglen - paddingsize, paddingsize, blocksize, padcount)


def determineBlockOffset(blocksize):
    ciphertext = encrypt([0x41] * 3 * blocksize)
    ciphertexts = [c for c in chunks(ciphertext, blocksize)]
    for off in xrange(len(ciphertexts) - 1):
        if ciphertexts[off] == ciphertexts[off + 1]:
            return off
    return -1


def generateCiphertexts(buffer):
    buffers = {}
    for b in xrange(256):
        buffers[b] = encrypt(buffer + [b])
    return buffers.items()


def guessBytes(maxCount, blocksize, blockOffset, prefixFill):
    buffer = [0x41] * (blocksize - 1 + prefixFill)
    blockCount = 0  
    recoveredBytes = []
    for i in xrange(maxCount):
        if len(recoveredBytes) > 0 and len(recoveredBytes) % blocksize == 0:
            
            blockCount += 1
            buffer.extend([0x41] * blocksize)

        
        ciphertexts = generateCiphertexts(buffer[len(recoveredBytes):] +
                                          recoveredBytes)
        
        ciphertext = [c for c in chunks(  
            encrypt(buffer[len(recoveredBytes):]),  
                    blocksize)][blockCount + blockOffset]  

        for plain, cipher in ciphertexts:  
            if [c for c in chunks(cipher, blocksize)][blockCount + blockOffset] == ciphertext:
                recoveredBytes.append(plain)
    return recoveredBytes


def main():
    msglen, padlen, blocksize, prefixCount = detectBlockSize()
    print 'Block size: %d, message length: %d, padlen: %d, prefixCount: %d' % \
          (blocksize, msglen, padlen, prefixCount)

    ciphertext = encrypt([0x41] * 3 * blocksize)
    if not verifyECB(ciphertext, blocksize):
        print 'No ECB usage detected'
        sys.exit(-1)
    blockOffset = determineBlockOffset(blocksize)
    print 'Repeating block at pos. %d' % blockOffset
    plaintext = guessBytes(msglen, blocksize, blockOffset, prefixCount)
    print 'Length of recovered plaintext: %d\n%s' % (len(plaintext),
                                                     bytesToText(plaintext))


if __name__ == '__main__':
    main()
