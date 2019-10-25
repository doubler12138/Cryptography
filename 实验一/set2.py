def stringXor(stringX,stringY):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(stringX, stringY))


string1='1c0111001f010100061a024b53535009181c'
string2='686974207468652062756c6c277320657965'
hexString1=string1.decode('hex')
hexString2=string2.decode('hex')
result=stringXor(hexString1,hexString2).encode('hex')
print result
