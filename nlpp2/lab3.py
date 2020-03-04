from __future__ import division
import os
import re
from collections import Counter
a=[]
for file in os.listdir('/Users/babun/Desktop/NLP_LAB3/'):
	if file.endswith(".txt"):
		a.append(file)

for j in a:

	file = open(j, "r")
	s=[]
	s1=[]
	s2=[]
	s3=[]
	for line in file:
		s.append(line)

	p1 = r'\d|[._;\"--,:#$%^&*()-]|[\?]|[\!]'
	
	for i in s:
		if re.search(p1,i):
			s1.append(re.sub(p1," ",i))

	for i in s1:
		s2.append(i.split())

	for i in s2:
		s3 = s3 + i

	counter_of_terms = Counter(s3)
	types = len(counter_of_terms.keys())
	tokens = sum(counter_of_terms.values())

	print j,"Tokens = ",tokens," Types = ", types , "Token/Type =" , tokens/types