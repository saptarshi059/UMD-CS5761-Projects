'''
Program Name: ELIZA Mini
Author: SAPTARSHI SENGUPTA
Major: Computer Science / 1st Year / Graduate Student (MS) / University of Minnesota Duluth
Date: 09/21/18

Program Details: The program written here is a miniaturised version of the original ELIZA program written by Joseph Weizenbaum.
				 The code written here is in the Python programming language. 
				 ELIZA uses pattern matching operations (done by invoking regular expressions) to carry out conversations with users 
				 i.e. generate a proper output phrase given an input sequence (sentence). In simple terms, ELIZA is a very basic 
				 chatbot/conversational agent program.

Code Usage: In order to use this program -
				* A user must have the Python programming language compiler installed.
				* The user should type the following command in either command prompt or linux shell i.e. python Eliza.py.
				* An input would be of the form - "<It's nice to meet you too!" (Please type without quotation marks).
				* The output would be of the sort- ">I concur!".

Program Algorithm: The program operates in a very simple way -
				* At first, an opening dialog ensues in which ELIZA comes to know your name.
				* The program then continues to loop unitl the user either says "bye" or else they are forcefully kicked out for having
				  used too many slang phrases.
				* In each run of the loop, 
					* If a slang phrase or an apology statement is found in the input, an appropriate action is taken and the loop ends
					  for that turn.
					* Else, the input is scanned for a certain pattern (pattern matching) using regular expressions. If a match is found,
					  an appropriate reply is generated.
					* There is finally a case which comes into play when none of the patterns match and then the default case 
					  reply is given out. 

'''

import re 	#The only major module required for this code i.e. the regular expressions package.

def checkforslang(ip):
	global count
	flag=0
	collection = ['hell', 'moron', 'stupid', 'idiot', 'fool']	#List of slang phrases to be checked.

	if "sorry" in ip.split():	#A check to see if "sorry" is present in the input sentence 
		print ">It's okay. Just remember to use appropriate language from next time!"
		return True

	for i in ip.split():
		if i in collection:
			if count<= 1:
				print ">Mind your language!"
				count = count + 1
				return True
			else:
				#The case when a user gets kicked out of the loop for using too many slangs.
				print ">I had warned you before not to speak like this! Go away now!" 
				exit()
			
	return False	#The slang checking function.

def applytransformation(ip): #The transformation rule application function.
	
	if ip == "bye": #"Bye" has to have the highest priority as it is an exit program keyword!
		print ">Goodbye! It was nice talking to you! Have a great day!"
		return

	#From here onwards to the end of the function, the input is scanned with each of these patterns. If a pattern match occurs, the 
	#appropriate transformation rule is applied to the input phrase.
	
	if re.search(r'drop|dropping out',ip):
		print ">That is a big decision. Are you sure you have thought this through?"
		return #2nd highest priority becuase dropping out from college or a class is a big decision.

	#The remainder of the patterns have been arranged by intuition.
	if re.match(r'(.*)I(.*)right(.*)by(.*)', ip):
		ip = re.sub(r'you', 'me' ,ip)
		p1=re.match(r'(.*)I(.*)right(.*)by(.*)', ip)
		if "don't" in p1.group(1).split():
			print ">What makes you say that you made a wrong" + p1.group(3) + "by" + p1.group(4) + "?"
		else:
			print ">What makes you say that you" + p1.group(2) + "right" + p1.group(3) + "by" + p1.group(4) + "?"
		return

	p2 = re.match(r'(\w.*) (credits*)(.*) do I (\w.*)' ,ip)
	if p2:
		print ">" + p2.group(1) + " " + p2.group(2) + p2.group(3) +" do you think you think you " + p2.group(4)
		return

	if re.match(r'.*(nice).*', ip):
		print ">I concur!"
		return

	if re.match(r'(.*)don\'t(.*)', ip):
		p4=re.match(r'(.*)don\'t(.*)', ip)
		if p4:
			print ">Why don't you" + p4.group(2) + "?"
		return

	p5 =  re.match(r'.*(hard|difficult).*', ip)
	if p5:
		print ">I know college is " + p5.group(1) + " but you can do it! trust me!"
		return

	p6=re.match(r'.*plans*.*', ip)
	if p6:
		if re.search(r'[Cc]ould',ip):
			print ">Sure, tell me about them."
		else:
			print ">How so?"
		return

	if re.match(r'.*help*.*', ip):
		print ">I'm glad to help!"
		return

	p7= re.match(r'.*(scared*)(.*)',ip)
	if p7:
		print ">Why are you scared" + p7.group(2) + "?"
		return

	if re.match(r'.*\byo*\b.*' , ip) or re.search(r'whatever',ip):
		print ">My my! thats a snazzy attitude you got there! you might want to remember who you are talking to!"
		return	

	if re.search(r'\bhaha*\b',ip):
		print ">I'm glad you are amused. Now can we become serious again?"
		return

	if re.match(r'I (was|am) (.*)' , ip):
		ip=re.sub(r'my' , 'your' , ip)
		p8= re.match(r'I (was|am) (.*)' , ip)
		print ">Wow that's great! why are you " + p8.group(2) + "?"
		return
 
	p9=re.match(r'(.*)(believe*)(.*)',ip)
	if p9:
		if re.search(r'me',ip):
			ip=re.sub(r'me','you',ip)
		if re.search(r'my',ip):
			ip=re.sub(r'my','your',ip)
		p9=re.match(r'(.*)(believe*)(.*)',ip)
		print ">Why has " + p9.group(1) + p9.group(2) + p9.group(3) + "?"
		return

	if re.match(r'\bhm+\b|\bum+\b',ip):
		print ">So " + name + ", what else do you want to talk about?"
		return
	else:
		print ">Interesting! tell me more..." 	#Case for when Eilza wants to know more about the current topic of discussion. (default case)
		return

#Opening Dialogues.
print ">Hi! My name is Eliza and I am your academic advisor here. What is your name?"
name = raw_input("<")
print ">Hi " + name + ", it's nice to meet you!"
count = 0 #Count of the number of times the user has typed a slang phrase.

#Main Loop.
while input != "bye":
	input=raw_input("<") #The user input is taken here.
	if checkforslang(input):	#If the user has entered a slang, no other transformation rule will be applied. The loop ends for this turn.
		continue
	applytransformation(input)