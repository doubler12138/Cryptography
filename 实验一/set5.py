# -*- coding: utf-8 -*-

def repeatKeyXor(key,string):
	keyLen=len(key)
	result=''
	strResult=''
	for index, ch in enumerate(string):
		n=index % keyLen
		b=chr(ord(key[n]) ^ ord(ch))
		strResult += b
	return strResult


def main():
	string1='Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal'
	key='ICE'
	print repeatKeyXor(key, string1).encode('hex')



if __name__ == '__main__':
	main()
