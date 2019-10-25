# -*- coding: utf-8 -*-
characterFrequency = {
    'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
    'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
    'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
    'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
}

#获得概率分数
def getScore(string):
	score=0
	for char in string:
		char=char.lower()
		if char in characterFrequency:
			score += characterFrequency[char]
	return score


#将hex的每个字符与可能的密钥进行xor
def singleCharacterXor(key,hexString):
	result=""
	for i in hexString:
		b = chr(key ^ ord(i))
		result += b
	return result

#遍历备选密钥
def traversalSinglechar(hexString):
	#结果数组
	candidate=[]
	for key in range(256):
		plaintext = singleCharacterXor(key,hexString)
		score = getScore(plaintext)
		result = {
			'score': score,
			'plaintext': plaintext,
			'key': key
		}
		candidate.append(result)
	#使用sorted函数对结果数组进行升序排序，以score为比较元素，选择最后一个结果为解密结果返回
	return sorted(candidate,key=lambda c:c['score'])[-1]

def main():
	string='1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
	hexString=string.decode('hex')
	result=traversalSinglechar(hexString)['plaintext']
	key=chr(traversalSinglechar(hexString)['key'])
	print result
	print key


if __name__ == '__main__':
	main()
