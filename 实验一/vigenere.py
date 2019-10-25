# -*- coding: cp936 -*-
import string
def guessPossibleKey(subarr):
    visiable_chars=[]
    for x in range(32,126):
        visiable_chars.append(chr(x))
    test_keys=[]
    ans_keys=[]
    for x in range(0x00, 0xFF):
        test_keys.append(x)
        ans_keys.append(x)
    for i in test_keys:
        for s in subarr:
            if chr(s^i) not in visiable_chars:
                ans_keys.remove(i)
                break
    return ans_keys

def guessKeyLength():
    length = 0
    for keylen in range(1,14):
        for index in range(0,keylen):
            subarr=arr[index::keylen]
            ans_keys=guessPossibleKey(subarr)
            if ans_keys:
                length = keylen
    return length

def getKey(subarr):
    visiable_chars=string.ascii_letters+string.digits+','+'.'+' '
    possible_keys=[]
    final_keys=[]
    for x in range(0x00,0xFF):
        possible_keys.append(x)
        final_keys.append(x)
    for i in possible_keys:
        for s in subarr:
            if chr(s^i) not in visiable_chars:
                final_keys.remove(i)
                break
    return final_keys


if __name__ == '__main__':
    enStr = 'F96DE8C227A259C87EE1DA2AED57C93FE5DA36ED4EC87EF2C63AAE5B9A7EFFD673BE4ACF7BE8923CAB1ECE7AF2DA3DA44FCF7AE29235A24C963FF0DF3CA3599A70E5DA36BF1ECE77F8DC34BE129A6CF4D126BF5B9A7CFEDF3EB850D37CF0C63AA2509A76FF9227A55B9A6FE3D720A850D97AB1DD35ED5FCE6BF0D138A84CC931B1F121B44ECE70F6C032BD56C33FF9D320ED5CDF7AFF9226BE5BDE3FF7DD21ED56CF71F5C036A94D963FF8D473A351CE3FE5DA3CB84DDB71F5C17FED51DC3FE8D732BF4D963FF3C727ED4AC87EF5DB27A451D47EFD9230BF47CA6BFEC12ABE4ADF72E29224A84CDF3FF5D720A459D47AF59232A35A9A7AE7D33FB85FCE7AF5923AA31EDB3FF7D33ABF52C33FF0D673A551D93FFCD33DA35BC831B1F43CBF1EDF67F0DF23A15B963FE5DA36ED68D378F4DC36BF5B9A7AFFD121B44ECE76FEDC73BE5DD27AFCD773BA5FC93FE5DA3CB859D26BB1C63CED5CDF3FE2D730B84CDF3FF7DD21ED5ADF7CF0D636BE1EDB79E5D721ED57CE3FE6D320ED57D469F4DC27A85A963FF3C727ED49DF3FFFDD24ED55D470E69E73AC50DE3FE5DA3ABE1EDF67F4C030A44DDF3FF5D73EA250C96BE3D327A84D963FE5DA32B91ED36BB1D132A31ED87AB1D021A255DF71B1C436BF479A7AF0C13AA14794'
    arr=[]
    for x in range(0,len(enStr),2):
        arr.append(int(enStr[x:2+x],16))
    length = guessKeyLength()
    keys=[]
    for index in range(0,length):
        subarr = arr[index::length]
        keys.append(getKey(subarr))
    result = ''
    key = ''
    for i in range(0,len(arr)):
        result = result + chr(arr[i]^keys[i % length][0])
        
    print("明文：" + result)
    print(keys)
