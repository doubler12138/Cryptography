# -*- coding: utf-8 -*-
import set3
import os
import linecache

def main():
	contents=linecache.getlines('4.txt')
	candidate=[]
	for string in contents:
		hexString=string[:-1].decode('hex')
		candidate.append(set3.traversalSinglechar(hexString))
	print sorted(candidate,key=lambda c:c['score'])[-1]['plaintext']


if __name__ == '__main__':
	main()
