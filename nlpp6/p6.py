import re
import wikipedia #This module provides an implementation of the MediaWiki API.
import nltk
import calendar

question = ''

while question != 'quit':

	question = raw_input('>')

	if question == 'quit':
		break

	r1 = r'([Ww]ho|[Ww]hat|[Ww]hen|[Ww]here) (\w+) (.*)\?'

	match_operation = re.match(r1,question)

	if match_operation:
			
		page = wikipedia.page(match_operation.group(3))
		content = page.content.encode('utf-8') #Convert to a normal string

		unigrams = re.findall(r'\w+',match_operation.group(3))

		content = re.sub(r'\(listen\);','',content)
		content = re.sub(r'\([^)]*\)', '', content)
		content = re.sub(r'  ',' ',content)
		content = re.sub(r'\s\.','.',content)

		#Replacing all punctuation marks except period. This is because I want to extract only that sentence which contains all
		#the unigrams from the query string's target. Also the search in the content string should end when a '.' is encountered.
		content = re.sub(r'[\!\@\#\$\%\^\&\*\(\)\[\]\:\'\"\;\?\/\\\`\-\~\_\+\=]',' ',content)
		
		content = re.findall(r'\w+|[.]',content)
		content.append('.')

		j = 0
		flag = 0
		while j < len(content):
			sentence = []
			
			while content[j] != '.':
				sentence.append(content[j])
				j = j + 1
			
			j = j + 1
			sentence.append('.')

			matches = 0

			for k in unigrams:
				if k in sentence:
					matches = matches + 1

			if matches == len(unigrams):
				flag = 1
				string = ' '.join(x for x in sentence)
				break

		if flag == 0:
			print "<I'm sorry, I don't know the answer"
		else:
			#Removing section text (if any) from the resultant answer string 
			sections = page.sections

			for i in sections:
				s = i.encode('utf-8')
				s = re.sub(r'\W',' ',s)
				s = re.sub(r'\s+',' ',s)
				s = s.strip()
				if s in string:
					string = string.replace(s, '')
			
			string = re.sub(r'\s\.','.',string)
			final_string = ''
			#Applying Rules based on the kind of question
			
			#Applying rules for 'Who' questions
			if match_operation.group(1) in ['Who','who']:
				if match_operation.group(2) != 'is':
					string_pos_tagged = nltk.pos_tag(string.split())
					for tup in string_pos_tagged:
						if tup[1] == 'NNP' and (tup[0] not in unigrams) and (tup[0] not in calendar.month_name):
							final_string = final_string + tup[0] + ' '

					final_string = re.sub(r'\.','',final_string)
					string = final_string + match_operation.group(2) + ' ' + match_operation.group(3) + '.'
					print "<"+string
				else:
					print "<"+string
				
			#Applying rules for 'When' questions
			elif match_operation.group(1) in ['When','when']:
				for term in re.findall(r'\w+|[.]',string):
					if term.isdigit() and len(term) in [1,2,4]:
						final_string = final_string + term + ' '
					if term in calendar.month_name:
						final_string = final_string + term + ' '
				
				no_of_numbers = 0
				for i in final_string.split():
					if i.isdigit():
						no_of_numbers = no_of_numbers + 1

				if no_of_numbers >= 2:
					final_string = final_string.strip()
					final_string = re.sub(r'\s','-',final_string)
							
				string = match_operation.group(3) + ' ' + match_operation.group(2) + ' ' + final_string + '.'
				string = re.sub(r'\s\.','.',string)

				print "<"+string

			#Applying rules for 'What' questions
			elif match_operation.group(1) in ['What','what']:
				string_pos_tagged = nltk.pos_tag(re.findall(r'\w+|[.]',string))
				for tup in string_pos_tagged:
					if tup[1] == 'NNP' and (tup[0] not in re.findall(r'\w+|[.]',question)):
						final_string = final_string + tup[0] + ' '

				final_string = re.sub(r'\.','',final_string)
				string = final_string + match_operation.group(2) + ' ' + match_operation.group(3) + '.'

				print "<"+string
			
			#Applying rules for 'Where' questions
			elif match_operation.group(1) in ['Where','where']:
				string_pos_tagged = nltk.pos_tag(re.findall(r'\w+|[.]',string))
				for tup in string_pos_tagged:
					if tup[1] == 'NNP' and (tup[0] not in unigrams) and (tup[0] not in calendar.month_name):
						final_string = final_string + tup[0] + ' '

				final_string = re.sub(r'\.','',final_string)
				string = match_operation.group(3) + ' ' + match_operation.group(2) + ' ' + 'in' + ' ' + final_string + '.'
				string = re.sub(r'\s\.','.',string)

				print "<"+string