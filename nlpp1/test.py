import re
'''
ip = "I plan to be a pilot"

p1=re.match(r'.*plans*.*', ip)

[\s|\,|\!](\w*|\,|\!)(\s|\,|\!)(\w*|\,|\!)

print p1

p = r'\w+|[,!.]'

ip = "Tom is a boy who, plays football."

p1 = re.findall(p,ip)

trigrams = []
i = 0

while i < len(p1) - 2:
	trigrams.append((p1[i] , p1[i+1] , p1[i+2]))
	i = i + 1

for i in trigrams:
	print i
'''

ip = 'tom is a boy, who used to play football for manchester united but now, he plays for everton. everton is not really high ranked in the premier league.'

L = re.findall(r'(\w+)\s(\w+)',ip)

print L

for i in range(1,len(L)):
	L.insert(i,(L[i-1][1] , L[i][0]))

print L