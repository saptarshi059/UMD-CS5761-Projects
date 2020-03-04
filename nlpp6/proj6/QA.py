'''
Program Name: QA.py
Author: SAPTARSHI SENGUPTA
Major: Computer Science / 1st Year / Graduate Student (MS) / University of Minnesota Duluth
Date: 12/05/18

Program Details: This program is a simple Question Answering (QA) system designed to answer 'Who'/'What'/'Where'/'When' type questions. It relies on pattern matching and 
				 Part-Of-Speech (POS) tagging. The answers to the input questions are searched for within their Wikipedia articles. Different strategies are employed to 
				 find the answer such as query reformulation and selecting terms from the article which have the correct POS tags. The answer is generated based on the kind 
				 of question that has been asked. 

				 NOTE:- All outputs were italicized (visible if the terminal supports italics). Else output is printed using default setup.

Code Usage: In order to use this program -
				* A user must have the Python programming language compiler installed.
				
				* The user should type the following command in either command prompt or linux shell i.e. 
				  				python QA.py

				* The user will be prompted to enter their questions. They also have a functionality of clearing the screen by entering 'clear'. In order to exit the program,
				  they should enter either 'exit'/'quit'.

				* A snippet of the program in execution would look like this:
				
					//
					*** This is the QA system designed by Saptarshi Sengupta CS 5761. It will try to answer questions that start with Who, What, When or Where. 
					If you want to clear the screen, enter 'clear'. Enter 'exit' or 'quit' to leave the program. ***
					>who is Linkin Park?
					<Linkin Park is an American rock band from Agoura Hills California.
					>exit
					<Goodbye and Thank You for using this QA program!
					//

Program Algorithm: The program has the following underlying logic -
				 
				//Main Algorithm
				
				1. The program first checks to see whether the user enters 'clear'/'exit'/'quit'. If 'exit'/'quit' has been entered, the program ends else, the screen gets
				   cleared.

				2. If control passes through step 1, the imput question string is checked to see whether it matches the pattern that we are looking for. If the question 
				   doesn't match the required pattern, control goes back again to step 1. Else, it passes on to step 3. The pattern that we are searching for is of the form:
				   '<Type of question i.e. 'Who'/'What'/'Where'/'When'> <helping/auxillary verb> <main part of the question>?'

				3. If the question matches the above pattern, a search is made on Wikipedia using the <main part of the question> and it's page's content (entire page) is retrieved.

				It was assumed that all the questions that would be asked would have a valid Wikipedia entry.

				4. The content string then undergoes several filtering and processing steps as follows:
					4.1 Removal of all '(listen);' terms.
					4.2 Removal of all strings enclosed within paranthesis.
					4.3 Conversion of all double spaces to single spaces.
					4.4 Removal of spaces preceding a period point.
			        4.5 All punctuation marks except period points are removed.
			        4.6 The content string is finally sentence tokenized i.e. split into constituent sentences.
				
				5. The <main part of the question> is tokenized and stored as a list of terms called unigrams.

				6. The program then selects the first sentence from the content collection which contains all the tokens from the unigram list. (The intuition being here is
				   that the answer is most likely to occur in the first place the query terms occur)

				7. If there are no answer strings/sentences in the content collection matching the above criteria, the program responds by saying that it doesn't know the 
				   answer.

				8. If however, the program finds a string from content, it checks for the presence of any Wikipedia 'section' text and filters it out.

				9. Now, the type of question is determined and the appropriate path of action is decided.

					9.1 If the question is a 'Who' type,

							9.1.1 If the question contains as the <helping/auxillary verb> 'is', the sentence that was pulled out from content is printed out verbatim 
								  without any kind of processing. (The intuition here was that 'is' containing questions are usually well formatted and do not require any
								  other kind of string modification)

							9.1.2 For all other cases, the sentence obtained from step 6 is POS tagged and those terms are selected which are proper nouns but do not appear
								  in the <main part of the question> and are not names of months (a filtering process). The output string is generated with the following 
								  structure: <terms selected in this step> + <helping/auxillary verb> + ' ' + <main part of the question> + '.'
					
					9.2 If the question is a 'When' type,

							9.2.1 The sentence (step 6) string is tokenized.

							9.2.2 The program searches for strings in (9.2.1) which are numbers and have either 1/2/4 digits or are the names of months.(The idea here was 
								  that 3 digit numbers would most likely be non-date type numbers)

							9.2.3 If there were 2 or more numbers found in (9.2.2), all spaces between the terms would be replaced with a '-' just to enhance the look of 
								  the output string.

							9.2.4 The output string is generated with the following structure: 
								  <main part of the question> + ' ' + <helping/auxillary verb> + ' ' + <terms selected and formatted(if) in step 9.2.2> + '.'

					9.3 If the question is a 'What' type,

							For these 'What' kind of questions 2 strategies are employed:

							Strategy 1: A rewritten query i.e. the question string being rewritten as, "<main part of the question> + ' ' + <helping/auxillary verb>", lookup is 
										done on the original content string. If this returns a string, it gets printed out as the answer to the question. If there
										are no results, strategy 2 is employed.

							Strategy 2: >The sentence (step 6) string is firstly POS tagged.
										>Those terms are selected which are proper nouns and are not present in the <main part of the question>.
										>The output string is generated with the following  structure: 
										<terms selected in the above step> + ' ' + <helping/auxillary verb> + ' ' + <main part of the question>  + '.'

					9.4 If the question is a 'Where' type,

							9.4.1 The sentence obtained from step 6 is POS tagged and those terms are selected which are proper nouns but do not appear
								  in the <main part of the question> and are not names of months (a filtering process).

							9.4.2 The output string is generated with the following structure:
								  <main part of the question> + ' ' + <helping/auxillary verb> + ' ' + 'in' + ' ' + <terms selected in step 9.4.1> + '.'
'''
import re
import wikipedia #This module provides an implementation of the MediaWiki API.
import nltk #This module provides the Part of Speech Tagging Functionality.
import calendar #Using this module the names of the months of a year are obtained.
import click #This module was used simply to create a function whereby a user can clear the screen.

print "\x1B[3m"+"*** This is the QA system designed by Saptarshi Sengupta CS 5761. It will try to answer questions that start with Who, What, When or Where. If you want to clear the screen, enter 'clear'. Enter 'exit' or 'quit' to leave the program. ***"+"\x1B[23m"

question = ''

while question != 'quit':

	question = raw_input('>')

	#Utility to clear the terminal screen if the user wants to.
	if question == 'clear':
		click.clear()

	#Exit the program.
	elif question in ['quit','exit']:
		print "<"+"\x1B[3m"+"Goodbye and Thank You for using this QA program!"+"\x1B[23m"
		break

	else:
		r1 = r'([Ww]ho|[Ww]hat|[Ww]hen|[Ww]here) (\w+) (.*)\?' #The regular expression used to match/validate the question format.

		match_operation = re.match(r1,question)

		if match_operation:
				
			page = wikipedia.page(match_operation.group(3)) #Retrieving the wikipedia article associated with the last part (group 3) of the question string.
			content = page.content.encode('utf-8') #Extracting the content from the page and converting it to a normal string (not a unicode string).

			#The unigram list is the search terms (words) extracted from the last part (group 3) of the question string.
			unigrams = re.findall(r'\w+',match_operation.group(3))
			
			#Processing the content string.			
			content = re.sub(r'\(listen\);','',content) #Removing all occurences of the term (listen); which is often found in wikipedia content for phonetically explaining a word.
			content = re.sub(r'\([^)]*\)', '', content) #Removing all strings between each paranthesis and then deleting the parenthesis themselves. 
			content = re.sub(r'  ',' ',content) #Converting double spaces to a single space.
			content = re.sub(r'\s\.','.',content) #Replacing spaces followed by periods to simply a period. 

			#Replacing all punctuation marks except period. This is because I want to extract only that sentence which contains all
			#the unigrams from the query string's last part. Also the search in the content string should end when a '.' is encountered.
			content = re.sub(r'[\!\@\#\$\%\^\&\*\(\)\[\]\:\'\"\;\?\/\\\`\-\~\_\+\=]',' ',content)
			
			content = re.findall(r'\w+|[.]',content) #Splitting the content string into sentences.
			content.append('.')#Adding a period point to the end of the tokenized content list in order to avoid 'index out of bounds' error in the 'while' loop. 

			#The 'while' loop is checking for those sentences in the content string which contains all the tokens from the unigram list.
			j = 0
			flag = 0
			while j < len(content):
				sentence = []
				while content[j] != '.':
					sentence.append(content[j])
					j = j + 1
				
				j = j + 1 #To account for the period mark's index.
				sentence.append('.')

				matches = 0

				for k in unigrams:
					if k in sentence:
						matches = matches + 1

				if matches == len(unigrams):
					flag = 1
					string = ' '.join(x for x in sentence)
					break

			#If no such sentence is found, the program prints out this message.
			if flag == 0:
				print "<"+"\x1B[3m"+"I'm sorry, I don't know the answer"+"\x1B[23m"
			
			#However, if a sentence is found, the answer is searched for within that sentence depending on the type of question which has been asked.
			else:
				#Removing section text (if any) from the sentence that was retrieved.
				sections = page.sections
				for i in sections:
					s = i.encode('utf-8')
					s = re.sub(r'\W',' ',s) #Removing any non-word characters from the current section string 's'.
					s = re.sub(r'\s+',' ',s) #Replacing multiple spaces with a single space in the current section string 's'.
					s = s.strip() #Removing extra trailing and leading spaces from the current section string 's'.
					if s in string:
						string = string.replace(s, '')
				string = re.sub(r'\s\.','.',string)
				
				#Applying Rules based on the kind of question
				string1 = ''

				#Applying rules for 'Who' questions
				if match_operation.group(1) in ['Who','who']:
					
					#If the second term of the query string is not 'is', the answer string obtained so far is POS tagged so as to home in on the answer.
					if match_operation.group(2) != 'is':
						string_pos_tagged = nltk.pos_tag(string.split())
						
						#Iterating through each POS tuple for the answer string chosen.
						for tup in string_pos_tagged:

							#Choosing only those words which are proper nouns but aren't present in the query string and aren't 'month' names (done to filter out unwanted data).
							if tup[1] == 'NNP' and (tup[0] not in unigrams) and (tup[0] not in calendar.month_name):
								string1 = string1 + tup[0] + ' '

						string1 = re.sub(r'\.','',string1) #Used to remove the period (if any) in string1.
						
						#Formatting the output string to match the proper answer template for 'Who' questions.
						string = string1 + match_operation.group(2) + ' ' + match_operation.group(3) + '.'
						print "<"+"\x1B[3m"+string+"\x1B[23m"
					
					#If the second term of the query string is 'is', the answer string as obtained from the while loop is printed out verbatim without any formatting.
					else:
						print "<"+"\x1B[3m"+string+"\x1B[23m"
					
				#Applying rules for 'When' questions
				elif match_operation.group(1) in ['When','when']:
					
					#The answer string is tokenized and numbers which have either 1/2/4 digits are searched for within it. 
					#Also, month names are searched for within the answer string. When either of these are found, they are appended to a string called string1 
					#which is a component of the final output string.
					for term in re.findall(r'\w+|[.]',string):
						
						if term.isdigit() and len(term) in [1,2,4]:
							string1 = string1 + term + ' '
						
						if term in calendar.month_name:
							string1 = string1 + term + ' '
					
					#Checking string1 for the number of numbers that it has.
					no_of_numbers = 0
					for i in string1.split():
						if i.isdigit():
							no_of_numbers = no_of_numbers + 1

					#If the number of numbers that string1 has are greater than or equal to 2, all the spaces in string1 are 
					#replaced with a '-' just to format the output better.
					if no_of_numbers >= 2:
						string1 = string1.strip()
						string1 = re.sub(r'\s','-',string1)
								
					#Formatting the output string to match the proper answer template for 'When' questions.
					string = match_operation.group(3) + ' ' + match_operation.group(2) + ' ' + string1 + '.'
					string = re.sub(r'\s\.','.',string)

					print "<"+"\x1B[3m"+string+"\x1B[23m"

				#Applying rules for 'What' questions
				elif match_operation.group(1) in ['What','what']:
					
					#This is the first strategy for answering 'What' questions. The question is rewritten as the last part followed by the second word in the question.
					#The content string is then queried using this rewritten query string and a resultant string is obtained.
					rewritten_query = match_operation.group(3) + ' ' + match_operation.group(2)
					res = re.findall(re.escape(rewritten_query) + r'[^.]*\.',' '.join(x for x in content))
					res = ' '.join(x for x in res)

					#if the resultant string is not null, it gets printed out as the answer.
					if res != '':
						print "<"+"\x1B[3m"+res+"\x1B[23m"

					#Backup Strategy Comes into action if the rewritten query search doesn't result in an answer (null string).
					else:
						string_pos_tagged = nltk.pos_tag(re.findall(r'\w+|[.]',string))
						
						#The search strategy is similar to the 'Who' questions's strategy except here 'months' are not searched for.
						for tup in string_pos_tagged:
							if tup[1] == 'NNP' and (tup[0] not in re.findall(r'\w+|[.]',question)):
								string1 = string1 + tup[0] + ' '

						string1 = re.sub(r'\.','',string1)
						
						#Formatting the output string to match the proper answer template for 'What' questions.
						string = string1 + match_operation.group(2) + ' ' + match_operation.group(3) + '.'

						print "<"+"\x1B[3m"+string+"\x1B[23m"
				
				#Applying rules for 'Where' questions
				elif match_operation.group(1) in ['Where','where']:
					
					#The search strategy here is the same as the strategy for 'Who' questions.
					string_pos_tagged = nltk.pos_tag(re.findall(r'\w+|[.]',string))
					for tup in string_pos_tagged:
						if tup[1] == 'NNP' and (tup[0] not in unigrams) and (tup[0] not in calendar.month_name):
							string1 = string1 + tup[0] + ' '

					string1 = re.sub(r'\.','',string1)
					
					#Formatting the output string to match the proper answer template for 'Where' questions.
					string = match_operation.group(3) + ' ' + match_operation.group(2) + ' ' + 'in' + ' ' + string1 + '.'
					string = re.sub(r'\s\.','.',string)

					print "<"+"\x1B[3m"+string+"\x1B[23m"