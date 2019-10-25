def pkcs7_pad(s, length):
    pad = length - len(s) % length
    return s + chr(pad) * pad

if __name__=='__main__':
    padded_msg = pkcs7_pad('YELLOW SUBMARINE', 20)
    print len(padded_msg), padded_msg, padded_msg.encode('hex')
