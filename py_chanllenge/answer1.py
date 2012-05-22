#!/usr/bin/python
# coding:utf-8

def wordmap(word):
    chars = []
    charmap = lambda c: chr((ord(c) - 94) % 26 + 96)
    
    for c in word:
        n = ord(c)
        if n > 96 and n < 123:
            c = charmap(c)
        chars.append(c)
    
    return ''.join(chars)

s = '''
g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj.
'''

words = s.split()

print words

words = [wordmap(w) for w in words]

print ' '.join(words)

print wordmap('map')
