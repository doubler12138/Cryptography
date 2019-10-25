import itertools
import linecache
import set5
import set3


def hammingDistance(strA,strB):
	dist=0
	for x, y in zip(strA,strB):
		b = bin(ord(x) ^ ord(y)) 
		dist += b.count('1')
	return dist

def guessKeySize(string):
	normals = []
	for keySize in range(2,40):
		blocks = []
		cnt = 0
		distance = 0
		for i in range(0, len(string), keySize):
			cnt += 1
			blocks.append(string[i:i+keySize])
			if cnt == 4:
				break
		pairs = itertools.combinations(blocks,2)
		for (x, y) in pairs:
			distance += hammingDistance(x, y)
		distance = distance / (6.0)
		normalDistance= distance / keySize
		key={
			'keysize':	keySize,
			'distance': normalDistance
		}
		normals.append(key)
	candidateKeySize=sorted(normals,key=lambda c:c['distance'])[0:3]
	return candidateKeySize

def guessKey(keySize,string):
	nowStr = ''
	key = ''
	for i in range(keySize):
		nowStr=''
		for index, ch in enumerate(string):
			if index % keySize == i:
				nowStr += ch
		
		key += chr(set3.traversalSinglechar(nowStr)['key'])
	return key

def getPlaint(string):
	keySizeList = guessKeySize(string)
	candidateKey = []
	possiblePlaints = []
	for keySize in keySizeList:
		key = guessKey(keySize['keysize'], string)
		possiblePlaints.append((set5.repeatKeyXor(key, string), key))	
	return sorted(possiblePlaints,key=lambda c:set3.getScore(c[0]))[-1]

def main():
	assert hammingDistance('this is a test', 'wokka wokka!!!') == 37
	contents=open('6.txt').read()
	string=str(contents).decode('base64')
	result=getPlaint(string)
	print result[0]
	print result[1]

if __name__ == '__main__':
	main()
