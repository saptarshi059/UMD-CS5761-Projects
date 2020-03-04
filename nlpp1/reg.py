import re

print ">Hi.How are you?"

while input != ("exit"):
	input = raw_input("<").lower()
	p1=re.match(r'(i) (\w*) (my) (\w*)', input)
	p2=re.match(r'(you) (\w*) (me) (\w*)', input)
	p3=re.match(r'(she) (\w*) (me) (\w*)', input)
	p4=re.match(r'(he) (\w*) (me) (\w*)', input)

	if p1:
		print '>What makes you say you ' + p1.group(2) + ' your ' + p1.group(4)
	elif p2:
		print '>Why do you say I ' + p2.group(2) + ' you ' + p2.group(4)
	elif p3:
		print '>What makes you say she ' + p3.group(2) + ' you ' + p3.group(4)
	elif p4:
		print '>What makes you say he ' + p4.group(2) + ' you ' + p4.group(4)
	else:
		print ">tell me more."