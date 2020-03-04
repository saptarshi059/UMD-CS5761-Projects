import re

ip=raw_input(">")


r1=r'.*\bThomas J\. Hill\b.*'
m1=re.match(r1,ip)

if m1:
	print re.sub(r'\bThomas J. Hill\b',"Tommy Hill",ip)
else:
	print "NO MATCH 1"


'''
r2=r'.*[\.?,!\'].*'
m2=re.match(r2, ip)

if m2:
	print re.sub(r'[\.?,!\']', "X", ip)
else:
	print "NO MATCH 2"
'''

'''
r3=r'(.*\bbear\b.*\bcat\b.*)|(.*\bcat\b.*\bbear\b.*)'
m3=re.match(r3,ip)
if m3:
	print ip
else:
	print "NO MATCH 3"
'''

'''
r4=r'.*\d.*'
m4=re.match(r4,ip)

if m4:
	print re.sub(r'^\d+|\d+$',"INT",ip)
else:
	print ip
'''
